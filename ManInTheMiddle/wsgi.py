from flask import Flask
from flask import send_file

import requests
import json

from ConfigManager import ConfigManager as cm
from PiCamClient import PiCamClient as pcc
from NeuralNetClient import NeuralNetClient as nnc

config = cm.ConfigManaager().entries
cam_client = pcc.PiCamClient(config=config)
neural_net_client = nnc.NeuralNetClient(config=config)

app = Flask(__name__)
@app.route("/")
def default():
    return "<p>Welcome to the Pi Colony Picker Man in the Middle Server</p>"

@app.route("/pi-cam-os")
def get_pi_cam_os():
    url = config['man_in_the_middle']['pi_cam_server_url_root'] +'/os'
    response = requests.get(url, allow_redirects=True)
    return "pi cam response: {}".format(response.text)

@app.route("/colony-locations")
def get_colony_locations():
    image_file_location = cam_client.get_image_from_server()
    xys_file_locations = neural_net_client.get_locations(image_file_location)
    return json.dumps(xys_file_locations)