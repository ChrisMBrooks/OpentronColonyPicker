#############################################################
# Micro Webservice for Controlling Camera & Light Table.
# Configuration details are managed in confgi.json. 
# To be run on the RasPi. 
#############################################################

import os
import platform
from flask import Flask
from flask import send_file

from LightTable import LightTable as lt
from Camera import Camera as cam
from ConfigManager import ConfigManager as cm

config = cm.ConfigManaager().entries
camera = cam.Camera(config)
light_table = lt.LightTable(config)

app = Flask(__name__)
@app.route("/")
def get_home_page():
    return "<p>Welcome to the Pi Colony Picker Client Server</p>"

@app.route("/test-image")
def get_test_image():
    full_path = camera.test_image()
    return send_file(full_path, as_attachment=True)

@app.route("/image")
def get_image():
    light_table.turn_arduino_leds_on()
    full_path = camera.capture()
    light_table.turn_arduino_leds_off()
    return send_file(full_path, as_attachment=True)

@app.route("/light-table-on")
def turn_light_table_on():
    light_table.turn_arduino_leds_on()
    return "<p>Table on!</p>"

@app.route("/light-table-off")
def turn_light_table_off():
    light_table.turn_arduino_leds_off()
    return "<p>Table off!</p>"

@app.route("/os")
def get_os():
    return "<p>OS: {}</p>".format(platform.system())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
