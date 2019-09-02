""" Author: Philipp Steinrötter (steinroe) """

import unittest
import time
import os

from .config import get_config

from iot_services_sdk import CapabilityService
from iot_services_sdk import DeviceService
from iot_services_sdk import GatewayService
from iot_services_sdk import SensorTypeService
from iot_services_sdk import SensorService

from iot_services_sdk import MQTTClient

class MQTTTest(unittest.TestCase):

    def setUp(self):
        config = get_config()

        self.capability_service = CapabilityService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'])

        self.device_service = DeviceService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'])

        self.gateway_service = GatewayService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        self.sensor_type_service = SensorTypeService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        self.sensor_service = SensorService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        if False:
            self.capability_service.debug_requests_on()
            self.device_service.debug_requests_on()
            self.gateway_service.debug_requests_on()
            self.sensor_type_service.debug_requests_on()
            self.sensor_service.debug_requests_on()

        self.mqtt_gateway_id = None
        self.capability_measure_id = None
        self.capability_measure_alternate_id = None
        self.capability_cmd_id = None
        self.capability_cmd_alternate_id = None
        self.device_id = None
        self.device_alternate_id = None
        self.sensor_type_id = None
        self.sensor_type_alternate_id = None
        self.sensor_id = None
        self.sensor_alternate_id = None
        self.secret = None
        self.pem_filepath = None
        self.mqtt_client = None
        self.command_received = False
        self.error_received = False

        filters = ["status eq 'online'"]
        gateways_response = self.gateway_service.get_gateways(filters=filters)

        gateways = gateways_response.get_result()
        mqtt_gateway = next(gateway for gateway in gateways if gateway['protocolId'] == 'mqtt')
        self.mqtt_gateway_id = mqtt_gateway['id']

        properties = [
            {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_measure_id', 'sdk_test_measure_cap', properties)

        self.capability_measure_id = create_response.get_result().get('id')
        self.capability_measure_alternate_id = create_response.get_result().get('alternateId')

        properties = [
            {"name": "sdk_test_cmd", "dataType": "string"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_cmd_id', 'sdk_test_cmd_cap', properties)

        self.capability_cmd_id = create_response.get_result().get('id')
        self.capability_cmd_alternate_id = create_response.get_result().get('alternateId')

        create_response = self.device_service.create_device(self.mqtt_gateway_id, 'sdk_device')

        device = create_response.get_result()
        self.device_id = device['id']
        self.device_alternate_id = device['alternateId']

        capabilities = [
            {'id': self.capability_measure_id, 'type': 'measure'},
            {'id': self.capability_cmd_id, 'type': 'command'}
        ]
        create_response = self.sensor_type_service.create_sensor_type('12345', 'sdk_mqtt_test_type', capabilities)

        self.sensor_type_id = create_response.get_result().get('id')
        self.sensor_type_alternate_id = create_response.get_result().get('alternateId')

        create_response = self.sensor_service.create_sensor(self.device_id, 'sdk-test-mqtt-sensor-id', 'sdk-test-mqtt-sensor-name', self.sensor_type_id)

        self.sensor_id = create_response.get_result()['id']
        self.sensor_alternate_id = create_response.get_result()['alternateId']

        res = self.device_service.get_device_pem(self.device_id).get_result()

        pem = res.get('pem')
        self.secret = res.get('secret')
        self.pem_filepath = 'cert.pem'

        pem_file = open(self.pem_filepath, 'w')
        pem_file.write(pem)
        pem_file.close()

        # Get MQTT Client for Device
        self.mqtt_client = self.device_service.get_mqtt_client(self.device_alternate_id, self.pem_filepath, self.secret)
        self.mqtt_client.connect()
        self.mqtt_client.loop_start()

        time.sleep(0.5)

    def test_ingestion(self):
        measures = [
            {'sdk_test_temp': 30}
        ]
        message_info_measures = self.mqtt_client.publish(self.capability_measure_alternate_id, self.sensor_alternate_id, measures, self.device_alternate_id)

        time.sleep(5)

        get_measures_response = self.device_service.get_measures(self.device_id)
        measures = get_measures_response.get_result()
        self.assertEqual(len(measures), 1)

    def test_ingestion_error(self):
        def on_error(client, userdata, report):
            self.error_received = True

        self.mqtt_client.on_error = on_error

        measures = [
            {'i_am_invalid': 30}
        ]
        message_info_measures = self.mqtt_client.publish(self.capability_measure_alternate_id, self.sensor_alternate_id, measures, self.device_alternate_id)

        time.sleep(0.5)

        self.assertTrue(self.error_received)

    def test_commands(self):
        def on_command(client, userdata, command):
            self.command_received = True

        self.mqtt_client.on_command = on_command

        self.mqtt_client.subscribe(self.device_alternate_id)

        command = {'sdk_test_cmd': 'I am a SDK!'}
        
        send_command_res = self.device_service.send_command_to_device(self.device_id, self.capability_cmd_id, self.sensor_id, command)
        self.assertEqual(send_command_res.get_status_code(), 202)

        time.sleep(2)

        # Check if command was received
        self.assertTrue(self.command_received)

    def tearDown(self):
        if self.mqtt_client is not None:
            self.mqtt_client.loop_stop()

        # Delete Sensor
        if self.sensor_id is not None:
            delete_sensor_res = self.sensor_service.delete_sensor(self.sensor_id)
            self.assertEqual(delete_sensor_res.get_status_code(), 200)

        # Delete Device
        if self.device_id is not None:
            delete_response = self.device_service.delete_device(self.device_id)
            self.assertEqual(delete_response.get_status_code(), 200)    
        
        # Delete SensorTyp
        if self.sensor_type_id is not None:
            delete_sensor_type_response = self.sensor_type_service.delete_sensor_type(self.sensor_type_id)
            self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Measure Capability
        if self.capability_measure_id is not None:
            delete_response = self.capability_service.delete_capability(self.capability_measure_id)
            self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Command Capability
        if self.capability_cmd_id is not None:
            delete_response = self.capability_service.delete_capability(self.capability_cmd_id)
            self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Certfile
        if self.pem_filepath is not None:
            try:
                os.remove(self.pem_filepath)
            except OSError:
                pass
