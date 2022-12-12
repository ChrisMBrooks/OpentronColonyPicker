# Automated Colony Picker for OT-2
The following hardware and software solution is a 3rd party, open source add-on to the OpenTron OT-2 liquid handling automation platform. The solution leverages computer vision & the precision contrl of the OT-2 to automate the picking of colonies from a 90mm petri dish.  

## Software

### OT-2 Client
A Jupyter Notebook file for orchestrating the automation protcol including REST API data retrieval, calibration and precision control of the OT-2 P300 single channel pipette used to pick colonies. 

#### Installation & Configuration
Simply import the Jupyter notebook file onto the native Jupyter server hosted on OT-2 robot.

A custome Labware definitionf file is also provided and must be manually imported using the OT-2 Host PC application. 

#### Dependencies
Python3 including the following packages: Opentron

### ManInTheMiddle
A micro REST-style API to facilitate information exchange between the PiCam API and the OT-2 Client. The client also uses TensorFlow to detect potential colonies and return the corresponding x,y location coordinates.  

The pre-trained TensorFlow model, NeuralNetClient\frozen_inference_graph.pb, was adopted from the from the iGEMMarburg2019 project ([Link](https://2019.igem.org/Team:Marburg)).

#### Url Endpoints 
```
GET pi-cam-image
GET colony-locations
```

#### Installation & Configuration
The web server is configured to run on the Windows OS. Configuration details are stored in the ConfigManager\config.json file. To set-up, simply copy the ManInTheMiddle directory & contents to the OT-2 host PC. 

```
python3 OpenTronColonyPicker\ManInTheMiddle\wsgi.py
```

It is recommended to configure a Windows Schedule Task to ensure the server resumes after reboot. For production gUnicorn & NGINX are recommended.

#### Dependencies
Python3 including the following packages: Flask, TensorFlow, Requests, Pillow,MatPlotLib, Numpy, 

### PiCam Server
A micro REST-style API to enable remote orchestration of the light table and and the Pi Cam HQ. To set-up, simply copy the Server directory & contents to the RasPi.  

#### Url Endpoints 
```
GET image
GET light-table-on
GET light-table-off
```

#### Installation & Configuration
The web server is configured to run on the RasPi OS. Configuration details are stored in the ConfigManager\config.json file. You will need to specify the USB com port for the light table. 

```
python3 OpenTronColonyPicker\Server\wsgi.py
```

It is recommended to configure a CronJob to ensure the server resumes after reboot. For production gUnicorn & NGINX are recommended.

#### Dependencies
Python3 including the following packages: Flask, PiCamera2, PySerial, Requests

## Hardware
The CAD files for the camera mount & light table are included as STL files. The hardware design was adopted from the iGEMMarburg2019 project ([Link](https://2019.igem.org/Team:Marburg)).


### Authors and Copyright
Imperial Systems & Synthetic Biology (SSB) MRes - 2022

## Licensure
This software is provided open-source under the GNU General Public License version 3 (GLPv3) and our hardware is provided open-source under the CERN Open Hardware Licence version 1.2 (CERN OHL).
