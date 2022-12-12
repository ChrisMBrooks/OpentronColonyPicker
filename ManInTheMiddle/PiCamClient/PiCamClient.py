import os
import requests
from PIL import Image

from ConfigManager import ConfigManager as cm

class PiCamClient():
    def __init__(self, config:dict):
        self.config = config
        self.filename = self.config["man_in_the_middle"]["filename"]
        self.root = self.config["man_in_the_middle"]["root"]
        
        self.server_url_root = \
            self.config["man_in_the_middle"]["pi_cam_server_url_root"]

        self.image_url = self.server_url_root + "/image"

    def get_image_from_server(self):
        #Set Params
        path_name = self.root + "\\"+ "Temp"
        full_path = path_name + "\\" + self.filename
        
        #Get Image File
        r = requests.get(self.image_url, allow_redirects=True)

        #Housekeeping
        if os.path.exists(full_path):
            os.remove(full_path)

        #Write Image to File
        open(full_path, 'wb').write(r.content)

        return full_path
    
    def crop_image(self, image_path:str): 
        image = Image.open(image_path)
        width, height = image.size 
        crop_details = self.config[ "man_in_the_middle"]["crop_details"]

        #Crop Box Positions 
        left = width*float(crop_details["left"]) 
        top = height*float(crop_details["top"])
        right = width - width*float(crop_details["right"])
        bottom = height - height*float(crop_details["bottom"])

        cropped_image = image.crop((left, top, right, bottom)) 
        cropped_image.save(image_path)
        return image_path