import platform 
import os
import requests

from ConfigManager import ConfigManager as cm
from NeuralNetClient import NeuralNetClient as nnc

class PiCamClient():
    def __init__(self, config:dict):
        self.config = config
        self.pi_os = self.is_pios()
        self.cm = cm.ConfigManager()
        self.filename = self.cm.entries["client"]["filename"]
        self.root = self.cm.entries["client"]["root"]
        self.server_url_root = self.cm.entries["client"]["server_url_root"]
        self.nnc = nnc.NeuralNetClient()

    def is_pi_os(self):
        if platform.system() == "Linux":
            return True
        else:
            return False    

    def get_image_from_server(self):
        #Set Params
        path_name = self.root + "/"+ "Temp"
        full_path = path_name + "/" + self.filename
        
        #Get Image File
        r = requests.get(self.server_url, allow_redirects=True)

        #Housekeeping
        if os.path.exists(full_path):
            os.remove(full_path)

        #Write Image to File
        open(full_path, 'wb').write(r.content)

        return full_path
    
    def get_locations(self, full_path_file_name:str):
        self.nnc.get_xy_locations_from_graph(full_path_file_name)

    def run(self):
        file_location = self.get_image_from_server()
        self.get_locations(file_location)
        #operate the opentron using the locations ....