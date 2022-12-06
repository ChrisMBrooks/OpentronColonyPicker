import os
import platform
from picamera2 import Picamera2

class Camera():
    def __init__(self, config:dict): 
        self.config = config
        self.setup()

    def setup(self):
        self.filename = self.config["server"]["filename"]
        self.pi_camera = Picamera2()
        self.capture_config = self.pi_camera.create_still_configuration()
        self.root = self.config["server"]["root"]
        self.full_path = self.root + "/" + "Temp" + "/" + self.filename
        print(self.full_path)
    
    def capture(self):
        self.file_housekeeping()        
        self.pi_camera.start(show_preview=False)
        self.pi_camera.switch_mode_and_capture_file(self.capture_config, self.full_path)
        self.pi_camera.stop()
        return self.full_path

    def file_housekeeping(self):
        if os.path.exists(self.full_path):
            os.remove(self.full_path)
    
    def test_image(self):
        filename = "test_image.jpeg"
        full_path = self.root + "/" + "Server/Camera/Test/" + filename
        return full_path
