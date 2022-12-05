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
def hello_world():
    return "<p>Welcome to the Pi Colony Picker Client Server</p>"

@app.route("/test-image")
def get_test_image():
    full_path = camera.test_image()
    return send_file(full_path, as_attachment=True)

@app.route("/image")
def get_image():
    light_table().turn_arduino_on()
    full_path = camera.capture()
    light_table().turn_arduino_on()
    return send_file(full_path, as_attachment=True)

@app.route("/os")
def get_os():
    return "<p>OS: {}</p>".format(platform.system())
