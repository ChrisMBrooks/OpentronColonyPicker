import os
import platform
import cv2

class Camera():
    def __init__(self, config:dict): 
        self.config = config
        self.setup()

    def is_pi_os(self):
        if platform.system() == "Darwin":
            return False
        else:
            return True    

    def setup(self):
        self.filename = self.config["server"]["filename"]
        self.pi_os = self.is_pi_os()
        if self.is_pi_os():
            from picamera import PiCamera
            self.pi_camera = PiCamera()
            self.root = self.config["server"]["raspi_root"]
        else:
            self.root = self.config["server"]["mac_root"]
        
        self.full_path = self.root + "/" + "Temp" + "/" + self.filename
        print(self.full_path)
    
    def capture(self):
        self.file_housekeeping()
        if self.pi_os:
            self.pi_camera.capture(self.full_path)
        else: 
            self.get_mac_cam_image()
            
        return self.full_path

    def file_housekeeping(self):
        if os.path.exists(self.full_path):
            os.remove(self.full_path)

    def get_mac_cam_image(self):
        cap = cv2.VideoCapture(0) 
        ret,frame = cap.read()
        cv2.imwrite(self.full_path,frame)
        cap.release()
    
    def test_image(self):
        filename = "test_image.jpeg"
        full_path = self.root + "/" + "Server/Camera/Test/" + filename
        return full_path