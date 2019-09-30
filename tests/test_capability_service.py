""" Author: Philipp Steinrötter (steinroe) """

import unittest

from .config import get_config

from iot_services_sdk import CapabilityService, DeviceManagementAPIException


class CapabilityServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        config = get_config()

        self.capability_service = CapabilityService(instance=config['IOTS']['instance'],
                                                    user=config['IOTS']['user'],
                                                    password=config['IOTS']['password'],
                                                    tenant_id=config['IOTS']['tenant_id'])

        self.capability = None
        self.is_deleted = None

    def test_create_capability(self) -> None:
        properties = [
            {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_measure_id', 'sdk_test_measure_cap',
                                                                    properties)

        self.capability = create_response.get_result()
        self.is_deleted = False

    def test_get_capabilities(self) -> None:
        filters = ["id eq '" + self.capability_measure_id + "'"]
        get_response = self.capability_service.get_capabilities(filters=filters)
        capabilities = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(self.capability, capabilities[0])

    def test_get_capability_count(self) -> None:
        count_response = self.capability_service.get_capability_count()
        self.assertEqual(count_response.get_status_code(), 200)

    def test_update_capability(self) -> None:
        properties = [
            {
                "dataType": "integer",
                "name": "sdk_property",
                "unitOfMeasure": "SDK"
            }
        ]
        update_response = self.capability_service.update_capability(self.capability.get['id'], 'sdk_new_alt_id',
                                                                    'sdk_new_name', properties)
        self.assertEqual(update_response.get_status_code(), 200)

    def test_get_capability(self) -> None:
        get_response = self.capability_service.get_capability(self.capability.get['id'])
        capability = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(capability['name'], 'sdk_new_name')

    def test_delete_capability(self) -> None:
        delete_response = self.capability_service.delete_capability(self.capability.get['id'])
        self.assertEqual(delete_response.get_status_code(), 200)
        self.is_deleted = True

    def tearDown(self) -> None:
        if self.capability is not None and self.capability.get['id'] is not None and self.is_deleted is not True:
            delete_response = self.capability_service.delete_capability(self.capability.get['id'])
            self.assertEqual(delete_response.get_status_code(), 200)

