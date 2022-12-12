import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow.compat.v1 as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

tf.disable_v2_behavior()

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("NeuralNetClient/models/research/object_detection")
from utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')

from utils import label_map_util
from utils import visualization_utils as vis_util

class NeuralNetClient():
    def __init__(self, config:dict):
        self.config = config
        self.FROZEN_GRAPH = 'NeuralNetClient/frozen_inference_graph.pb'
        self.PATH_TO_LABELS = 'NeuralNetClient/models/research/object_detection/training/mscoco_label_map.pbtxt'

        self.PATH_TO_TEST_IMAGES_DIR = 'NeuralNetClient/plate_image'
        self.TEST_IMAGE_PATHS = self.absoluteFilePaths(self.PATH_TO_TEST_IMAGES_DIR)

        # Size, in inches, of the output images.
        self.IMAGE_SIZE = (12, 8)

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.io.gfile.GFile(self.FROZEN_GRAPH, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
    
        self.category_index = label_map_util.create_category_index_from_labelmap(
            self.PATH_TO_LABELS, use_display_name=True)

    def get_locations(self, full_path_filename:str):
        return self.process_single_file(full_path_filename)

    def process_single_file(self, image_path):

        image = Image.open(image_path)
        image = self.crop_image(image)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = self.load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        output_dict = self.run_inference_for_single_image(image_np_expanded, self.detection_graph)
        # Visualization of the results of a detection.

        centre_points = []
        for i, score in enumerate(output_dict['detection_scores']):
            if float(score) > 0.5:
                box = output_dict['detection_boxes'][i]
                centre_points.append([(box[0]+box[2])/2, (box[1]+box[3])/2])

        return centre_points

    def process_all_files(self):
        c = 0

        for image_path in self.TEST_IMAGE_PATHS:
            image = Image.open(image_path)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
            image_np = self.load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
            output_dict = self.run_inference_for_single_image(image_np_expanded, self.detection_graph)
        # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            self.category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=4)
            #print(os.getcwd())
            plt.figure(figsize=self.IMAGE_SIZE)
            plt.imshow(image_np)
            plt.savefig('NeuralNetClient/processed/{0}.jpg'.format(c))
            np.savetxt('NeuralNetClient/processed/boxes{0}.csv'.format(c),
                        output_dict['detection_boxes'], delimiter=",")
            np.savetxt('NeuralNetClient/processed/scores{0}.csv'.format(c),
                    output_dict['detection_scores'], delimiter=",")
            c += 1

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def absoluteFilePaths(self, directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))
    
    def crop_image(self, image:Image): 
        width, height = image.size 
        crop_details = self.config[ "man_in_the_middle"]["crop_details"]

        #Crop Box Positions 
        left = width*float(crop_details["left"]) 
        top = height*float(crop_details["top"])
        right = width - width*float(crop_details["right"])
        bottom = height - height*float(crop_details["bottom"])

        return image.crop((left, top, right, bottom)) 
    
    def run_inference_for_single_image(self, image, graph):
        with graph.as_default():
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)

                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(
                        tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [
                                            real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [
                                            real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[1], image.shape[2])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                        feed_dict={image_tensor: image})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.int64)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

        return output_dict

    def calculate_centre_points(self):
        colony_i = []
        with open('NeuralNetClient/processed/scores0.csv') as scores:
            for i, score in enumerate(scores):
                if float(score) > 0.5:
                    colony_i.append(i)
                if float(score) < 0.5:
                        break

        all_boxes = []
        colony_boxes = []
        with open('NeuralNetClient/processed/boxes0.csv') as boxes:
            for box in boxes:
                all_boxes.append(box.strip().split('\n'))
            for i  in colony_i: colony_boxes.append(all_boxes[i]) 

        for i, box in enumerate(colony_boxes):
            for coords in box: colony_boxes[i] = coords.split(',')
        for box in colony_boxes:
            for i, coords in enumerate(box): box[i] = float(coords)
            
        # coordinates stored in the form y1, x1, y1, x2 
        centre_points = []
        for box in colony_boxes:
            # yx coordinate of centre point
            ymid = (box[0]+box[2])/2
            xmid = (box[1]+box[3])/2
            centre_point = [ymid, xmid]
            centre_points.append(centre_point)

        return centre_points