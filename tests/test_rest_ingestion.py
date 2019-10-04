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

from iot_services_sdk import RESTGatewayException

from iot_services_sdk import RestClient

class RESTTest(unittest.TestCase):

    def setUp(self):
        config = get_config()

        self.capability_service = CapabilityService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'],
                                    tenant_id=config['IOTS']['tenant_id'])

        self.device_service = DeviceService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'],
                                    tenant_id=config['IOTS']['tenant_id'])

        self.gateway_service = GatewayService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'],
                                            tenant_id=config['IOTS']['tenant_id'])

        self.sensor_type_service = SensorTypeService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'],
                                            tenant_id=config['IOTS']['tenant_id'])

        self.sensor_service = SensorService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'],
                                            tenant_id=config['IOTS']['tenant_id'])

        if False:
            self.capability_service.debug_requests_on()
            self.device_service.debug_requests_on()
            self.gateway_service.debug_requests_on()
            self.sensor_type_service.debug_requests_on()
            self.sensor_service.debug_requests_on()

        self.rest_gateway_id = None
        self.capability_id = None
        self.capability_alternate_id = None
        self.device_id = None
        self.device_alternate_id = None
        self.sensor_type_id = None
        self.sensor_type_alternate_id = None
        self.sensor_id = None
        self.sensor_alternate_id = None
        self.secret = None
        self.pem_filepath = None

        # Get REST Gateway
        filters = ["status eq 'online'"]
        gateways_response = self.gateway_service.get_gateways(filters=filters)

        gateways = gateways_response.get_result()
        rest_gateway = next(gateway for gateway in gateways if gateway['protocolId'] == 'rest')
        self.rest_gateway_id = rest_gateway.get('id')

        # Create Capabiliy
        properties = [
            {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_id', 'sdk_test_cap', properties)

        self.capability_id = create_response.get_result().get('id')
        self.capability_alternate_id = create_response.get_result().get('alternateId')
        
        # Create Sensor Type
        capabilities = [
            {'id': self.capability_id, 'type': 'measure'}
        ]
        create_response = self.sensor_type_service.create_sensor_type('12345', 'sdk_test_type', capabilities)

        self.sensor_type_id = create_response.get_result().get('id')
        self.sensor_type_alternate_id = create_response.get_result().get('alternateId')

        # Create Device
        create_response = self.device_service.create_device(self.rest_gateway_id, 'sdk_device')

        device = create_response.get_result()
        self.device_id = device['id']
        self.device_alternate_id = device['alternateId']

        # Create Sensor
        create_response = self.sensor_service.create_sensor(self.device_id, 'sdk-test-sensor-id', 'sdk-test-sensor-name', self.sensor_type_id)

        self.sensor_id = create_response.get_result()['id']
        self.sensor_alternate_id = create_response.get_result()['alternateId']

        # Download PEM and save to file
        res = self.device_service.get_device_pem(self.device_id).get_result()

        pem = res.get('pem')
        self.secret = res.get('secret')
        self.pem_filepath = 'cert.pem'

        pem_file = open(self.pem_filepath, 'w')
        pem_file.write(pem)
        pem_file.close()
       
    def test_rest_ingestion(self):
        rest_client = self.device_service.get_rest_client(device_alternate_id=self.device_alternate_id, pemfile=self.pem_filepath, secret=self.secret)

        measures = [
            {'sdk_test_temp': 30}
        ]

        data_ingestion_response = rest_client.post_measures(capability_alternate_id=self.capability_alternate_id, sensor_alternate_id=self.sensor_alternate_id, measures=measures)
        self.assertEqual(data_ingestion_response.get_status_code(), 202)

        time.sleep(5)

        get_measures_response = self.device_service.get_measures(self.device_id)
        measures = get_measures_response.get_result()
        self.assertEqual(len(measures), 1)

    def test_rest_gateway_exception(self):
        rest_client = self.device_service.get_rest_client(device_alternate_id=self.device_alternate_id, pemfile=self.pem_filepath, secret=self.secret)

        measures = [
            {'i_am_invalid': 30}
        ]

        self.assertRaises(RESTGatewayException, rest_client.post_measures, self.capability_alternate_id, self.sensor_alternate_id, measures)

    def tearDown(self):
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

        # Delete Capability
        if self.capability_id is not None:
            delete_response = self.capability_service.delete_capability(self.capability_id)
            self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Certfile
        if self.pem_filepath is not None:
            try:
                os.remove(self.pem_filepath)
            except OSError:
                pass
