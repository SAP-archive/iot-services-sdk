""" Author: Philipp Steinrötter (steinroe) """

import unittest
import time
import os
import paho.mqtt.client as paho

from .config import get_config

from iot_services_sdk import AboutService
from iot_services_sdk import CapabilityService
from iot_services_sdk import DeviceService
from iot_services_sdk import GatewayService
from iot_services_sdk import ProtocolService
from iot_services_sdk import SensorTypeService
from iot_services_sdk import SensorService
from iot_services_sdk import TenantService
from iot_services_sdk import UserService
from iot_services_sdk import VendorService

from iot_services_sdk import DeviceManagementAPIException
from iot_services_sdk import RESTGatewayException

from iot_services_sdk import MQTTClient

class SDKTest(unittest.TestCase):

    def setUp(self):
        config = get_config()

        self.about_service = AboutService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'])

        #self.about_service.debug_requests_on()

        self.capability_service = CapabilityService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'])

        #self.capability_service.debug_requests_on()

        self.device_service = DeviceService(instance = config['IOTS']['instance'],
                                    user = config['IOTS']['user'],
                                    password = config['IOTS']['password'])

        #self.device_service.debug_requests_on()

        self.gateway_service = GatewayService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.gateway_service.debug_requests_on()

        self.protocol_service = ProtocolService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.protocol_service.debug_requests_on()

        self.sensor_type_service = SensorTypeService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.sensor_type_service.debug_requests_on()

        self.sensor_service = SensorService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.sensor_service.debug_requests_on()

        self.tenant_service = TenantService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.tenant_service.debug_requests_on()

        self.user_service = UserService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.user_service.debug_requests_on()

        self.vendor_service = VendorService(instance = config['IOTS']['instance'],
                                            user = config['IOTS']['user'],
                                            password = config['IOTS']['password'])

        #self.vendor_service.debug_requests_on()

    def test_all_rest(self):
        # Get REST Gateway
        filters = ["status eq 'online'"]
        gateways_response = self.gateway_service.get_gateways(filters=filters)
        self.assertEqual(gateways_response.get_status_code(), 200)

        gateways = gateways_response.get_result()
        rest_gateway = next(gateway for gateway in gateways if gateway['protocolId'] == 'rest')

        # Create Capabiliy
        properties = [
            {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_id', 'sdk_test_cap', properties)
        self.assertEqual(create_response.get_status_code(), 200)

        capability_id = create_response.get_result().get('id')
        capability_alternate_id = create_response.get_result().get('alternateId')
        
        # Get All Capabilities
        filters = ["id eq '" + capability_id + "'"]
        get_response = self.capability_service.get_capabilities(filters=filters)
        capabilities = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(create_response.get_result(), capabilities[0])

        # Update Capability
        update_response = self.capability_service.update_capability(capability_id, capability_alternate_id, 'sdk_new_name')
        self.assertEqual(update_response.get_status_code(), 200)

        # Get Capability
        get_one_response = self.capability_service.get_capability(capability_id)
        json = get_one_response.get_result()
        self.assertEqual(json['name'], 'sdk_new_name')
        self.assertEqual(get_one_response.get_status_code(), 200)

        # Create Sensor Type
        capabilities = [
            {'id': capability_id, 'type': 'measure'}
        ]
        create_response = self.sensor_type_service.create_sensor_type('12345', 'sdk_test_type', capabilities)
        self.assertEqual(create_response.get_status_code(), 200)

        sensor_type_id = create_response.get_result().get('id')
        alternate_id = create_response.get_result().get('alternateId')

        # Get All Sensor Types
        filters = ["id eq '" + sensor_type_id + "'"]
        get_response = self.sensor_type_service.get_sensor_types(filters=filters)
        sensor_types = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(create_response.get_result(), sensor_types[0])

        # Update Sensor Type
        update_response = self.sensor_type_service.update_sensor_type(sensor_type_id, alternate_id, 'sdk_new_name')

        # Get Sensor Type
        get_one_response = self.sensor_type_service.get_sensor_type(sensor_type_id)
        json = get_one_response.get_result()
        self.assertEqual(json['name'], 'sdk_new_name')
        self.assertEqual(get_one_response.get_status_code(), 200)

        # Create Device
        create_response = self.device_service.create_device(rest_gateway['id'], 'sdk_device')
        self.assertEqual(create_response.get_status_code(), 200)

        device = create_response.get_result()
        device_id = device['id']
        device_alternate_id = device['alternateId']

        # Create Sensor
        create_response = self.sensor_service.create_sensor(device_id, 'sdk-test-sensor-id', 'sdk-test-sensor-name', sensor_type_id)
        self.assertEqual(create_response.get_status_code(), 200)

        sensor_id = create_response.get_result()['id']
        sensor_alternate_id = create_response.get_result()['alternateId']

        # Get All Devices
        filters = ["id eq '" + device_id + "'"]
        get_response = self.device_service.get_devices(filters=filters)
        devices = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(device['id'], devices[0]['id'])

        # Update Device
        update_response = self.device_service.update_device(device_id, 'sdk_new_name')
        self.assertEqual(update_response.get_status_code(), 200)

        # Get Device
        get_one_response = self.device_service.get_device(device_id)
        json = get_one_response.get_result()
        self.assertEqual(json['name'], 'sdk_new_name')
        self.assertEqual(get_one_response.get_status_code(), 200)

        # Add Custom Property
        add_prop_response = self.device_service.add_custom_property_to_device(device_id, 'whoami', 'sdk')
        self.assertEqual(add_prop_response.get_status_code(), 200)

        # Update Custom Property
        update_prop_response = self.device_service.update_custom_property(device_id, 'whoami', 'updated_by_sdk')
        self.assertEqual(update_prop_response.get_status_code(), 200)

        # Check for Update in Property
        device_res = self.device_service.get_device(device_id)
        device = device_res.get_result()

        custom_props = device.get('customProperties')
        included = False
        for prop in custom_props:
            if prop['key'] == 'whoami' and prop['value'] == 'updated_by_sdk':
                included = True
                break
        
        self.assertEqual(included, True)
        
        # Download PEM and save to file
        res = self.device_service.get_device_pem(device_id).get_result()
        self.assertIsNotNone(res.get('pem'))

        pem = res.get('pem')
        secret = res.get('secret')
        pem_filepath = 'cert.pem'

        pem_file = open(pem_filepath, 'w')
        pem_file.write(pem)
        pem_file.close()

        # Push data to test measures endpoint
        rest_client = self.device_service.get_rest_client(device_alternate_id=device_alternate_id, pemfile=pem_filepath, secret=secret)

        # REST Data Ingestion
        measures = [
            {'sdk_test_temp': 30}
        ]

        data_ingestion_response = rest_client.post_measures(capability_alternate_id=capability_alternate_id, sensor_alternate_id=sensor_alternate_id, measures=measures)
        self.assertEqual(data_ingestion_response.get_status_code(), 202)

        time.sleep(0.5)

        # Get Measures
        get_measures_response = self.device_service.get_measures(device_id)
        measures = get_measures_response.get_result()
        self.assertEqual(len(measures), 1)

        # Delete Custom Property
        delete_prop_res = self.device_service.delete_custom_property(device_id, 'whoami')
        self.assertEqual(delete_prop_res.get_status_code(), 200)

        # Delete Sensor
        delete_sensor_res = self.sensor_service.delete_sensor(sensor_id)
        self.assertEqual(delete_sensor_res.get_status_code(), 200)

        # Delete Device
        delete_response = self.device_service.delete_device(device_id)
        self.assertEqual(delete_response.get_status_code(), 200)    
        
        # Delete SensorType
        delete_sensor_type_response = self.sensor_type_service.delete_sensor_type(sensor_type_id)
        self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Capability
        delete_response = self.capability_service.delete_capability(capability_id)
        self.assertEqual(delete_response.get_status_code(), 200)

        # Delete Certfiles
        os.remove(pem_filepath)        
    
    def test_device_management_api_exception(self):
        self.assertRaises(DeviceManagementAPIException, self.gateway_service.get_gateways, ["status bb 'online'"])
        properties = [
            {"": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        self.assertRaises(DeviceManagementAPIException, self.capability_service.create_capability, 'sdk_test_id', 'sdk_test_cap', properties)