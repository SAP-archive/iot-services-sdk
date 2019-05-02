**Table of Contents**

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to obtain support](#how-to-obtain-support)
- [License](#license)
- [Usage](#usage)
- [Test](#test)
- [Build Docs](#build-docs)


## Description
This package wraps the SAP IoT Services, Cloud Foundry Edition Device Management APIs as well as the REST and the MQTT Cloud Gateway APIs in easy-to-use Python code. You can find more information on the APIs [here](https://help.sap.com/viewer/643f531cbf50462c8cc45139ba2dd051/Cloud/en-US) and [here](https://help.sap.com/viewer/6040fec3f22e4f9b8bf495f3789d66b5/Cloud/en-US#).

Features include:
+ Wrapper around every functionality of the Device Management API
+ Better error feedback
+ Wrapper around both Cloud Gateways
+ Both clients, REST and MQTT, are extended so that they work directly with the encrypted keys in the pem file
+ Better error handling and error feedback for REST and MQTT
  + The MQTT client has an on_error and an on_command callback which directly return the parsed message
  + The REST client parses the error for batched and single uploads and throws an error with the respective message
  + Both clients return the failed message to enable the user to retry easily

## Requirements
You will need an instance of IoT Services, Cloud Foundry to use this SDK. You can find more information on how to activate the service [here](https://cloudplatform.sap.com/capabilities/product-info.SAP-Cloud-Platform-Internet-of-Things.48b79cfa-3d49-4a42-9249-e589696691ae.html).

## Installation
The package will be available at pip:

`pip install iot-services-sdk`

If you want to download it manually, please make sure to install `paho-mqtt` and `requests` into your Python environment.

## How to obtain support
Please use [GitHub Issues](https://github.com/SAP/iot-services-sdk/issues) to file a bug.

## License
Copyright (c) 2019 SAP SE or an SAP affiliate company. All rights reserved.
This file is licensed under the SAP Sample Code License except as noted otherwise in the [LICENSE file](LICENSE).

## Usage
Please refer to the API documentation in the PDF file for details. You can check the tests for sample code.

Here is a small example displaying the following functionality:

+ Creating capabilities, a sensor type, a sensor and a device.
+ Downloading the certificate and creating a MQTT client.
+ Publishing valid and invalid measures as well as publishing and receiving commands.
+ Deleting every entity which was created.

```python
import os

from iot_services_sdk import CapabilityService
from iot_services_sdk import DeviceService
from iot_services_sdk import GatewayService
from iot_services_sdk import SensorTypeService
from iot_services_sdk import SensorService

from iot_services_sdk import MQTTClient

# Initialize services
device_service = DeviceService(instance = myinstance.eu10.cp.iot.sap, user = myuser, password = mypassword)
capability_service = CapabilityService(instance = myinstance.eu10.cp.iot.sap, user = myuser, password = mypassword)
gateway_service = GatewayService(instance = myinstance.eu10.cp.iot.sap, user = myuser, password = mypassword)
sensor_type_service = SensorTypeService(instance = myinstance.eu10.cp.iot.sap, user = myuser, password = mypassword)
sensor_service = SensorService(instance = myinstance.eu10.cp.iot.sap, user = myuser, password = mypassword)

# Turn requests debug functionality on
capability_service.debug_requests_on()
device_service.debug_requests_on()
gateway_service.debug_requests_on()
sensor_type_service.debug_requests_on()
sensor_service.debug_requests_on()

# Get Gateway
filters = ["status eq 'online'"]
gateways_response = gateway_service.get_gateways(filters=filters)
gateways = gateways_response.get_result()
mqtt_gateway = next(gateway for gateway in gateways if gateway['protocolId'] == 'mqtt')

# Create Measure Capability
properties = [
    {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
]
create_response = capability_service.create_capability('sdk_test_measure_id', 'sdk_test_measure_cap', properties)

capability_measure_id = create_response.get_result().get('id')
capability_measure_alternate_id = create_response.get_result().get('alternateId')

# Create Command Capability
properties = [
    {"name": "sdk_test_cmd", "dataType": "string"}
]
create_response = capability_service.create_capability('sdk_test_cmd_id', 'sdk_test_cmd_cap', properties)

capability_cmd_id = create_response.get_result().get('id')
capability_cmd_alternate_id = create_response.get_result().get('alternateId')

# Create Device
create_response = device_service.create_device(mqtt_gateway['id'], 'sdk_device')

device = create_response.get_result()
device_id = device['id']
device_alternate_id = device['alternateId']

# Create Sensor Type
capabilities = [
    {'id': capability_measure_id, 'type': 'measure'},
    {'id': capability_cmd_id, 'type': 'command'}
]
create_response = sensor_type_service.create_sensor_type('123456', 'sdk_mqtt_test_type', capabilities)

sensor_type_id = create_response.get_result().get('id')
sensor_type_alternate_id = create_response.get_result().get('alternateId')

# Create Sensor
create_response = sensor_service.create_sensor(device_id, 'sdk-test-mqtt-sensor-id', 'sdk-test-mqtt-sensor-name', sensor_type_id)

sensor_id = create_response.get_result()['id']
sensor_alternate_id = create_response.get_result()['alternateId']

# Download Certificate
res = device_service.get_device_pem(device_id).get_result()

pem = res.get('pem')
secret = res.get('secret')
pem_filepath = 'cert.pem'

# Write Certificate to PEM file
pem_file = open(pem_filepath, 'w')
pem_file.write(pem)
pem_file.close()

# Get MQTT Client for Device
mqtt_client = device_service.get_mqtt_client(device_alternate_id, pem_filepath, secret)
mqtt_client.connect()
mqtt_client.loop_start()

# Publish a measure
measures = [
    {'sdk_test_temp': 30}
]
message_info_measures = mqtt_client.publish(capability_measure_alternate_id, sensor_alternate_id, measures, device_alternate_id)

# Read measures
get_measures_response = device_service.get_measures(device_id)
measures = get_measures_response.get_result()

# Publish invalid measure and receive error
def on_error(client, userdata, report):
    print('ERROR RECEIVED: ')
    print(report)

mqtt_client.on_error = on_error

measures = [
    {'i_am_invalid': 30}
]
message_info_measures = mqtt_client.publish(capability_measure_alternate_id, sensor_alternate_id, measures, device_alternate_id)

# Publish and receive command
def on_command(client, userdata, command):
    print('COMMAND RECEIVED: ')
    print(command)

mqtt_client.on_command = on_command

mqtt_client.subscribe(device_alternate_id)

command = {'sdk_test_cmd': 'I am a SDK!'}

send_command_res = device_service.send_command_to_device(device_id, capability_cmd_id, sensor_id, command)

# Stop MQTT loop
mqtt_client.loop_stop()

# Delete Sensor
delete_sensor_res = sensor_service.delete_sensor(sensor_id)

# Delete Device
delete_response = device_service.delete_device(device_id)

# Delete SensorType
delete_sensor_type_response = sensor_type_service.delete_sensor_type(sensor_type_id)

# Delete Measure Capability
delete_response = capability_service.delete_capability(capability_measure_id)

# Delete Command Capability
delete_response = capability_service.delete_capability(capability_cmd_id)

# Delete Certfile
try:
    os.remove(pem_filepath)
except OSError:
    pass
```

## Test
To run the tests, you have to place a config.ini in the root directory. It has to contain the following information:
```
[IOTS]
INSTANCE=myinstance.eu10.cp.iot.sap
BASE_URI=/iot/core/api/v1
GATEWAY_URI=/iot/gateway
USER=myuser
PASSWORD=mypassword
```
Then, run 

`nosetests`

in the root directory. The tests will clean up after themselves - there is no need to check your system afterwards.

## Build Docs
Use Sphinx to build the documentation directly from the docstrings:

`cd docs`

`sphinx-apidoc -f -o source/ ../sap_iot_services_sdk`

`make latexpdf`

Copy the SAPIoTServicesSDK.pdf file into the root directory.
