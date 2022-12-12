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

@app.route("/pi-cam-image")
def get_pi_cam_image():
    image_file_location = cam_client.get_image_from_server()
    image_file_location = cam_client.crop_image(image_path=image_file_location)
    return send_file(image_file_location, as_attachment=True) 

@app.route("/colony-locations")
def get_colony_locations():
    image_file_location = cam_client.get_image_from_server()
    xys_file_locations = neural_net_client.get_locations(image_file_location)
    return {"colony_locations":xys_file_locations}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['man_in_the_middle']['host_port'])