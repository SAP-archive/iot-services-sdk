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
        properties = [
            {"name": "sdk_test_temp", "dataType": "double", "unitOfMeasure": "Celcius"}
        ]
        create_response = self.capability_service.create_capability('sdk_test_measure_id', 'sdk_test_measure_cap',
                                                                    properties)
        self.capability = create_response.get_result()
        self.is_deleted = False

    def test_a_create_capability(self) -> None:
        # Is tested in setup
        pass

    def test_b_get_capabilities(self) -> None:
        filters = ["id eq '" + self.capability.get('id') + "'"]
        get_response = self.capability_service.get_capabilities(filters=filters)
        capabilities = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(self.capability, capabilities[0])

    def test_c_get_capability_count(self) -> None:
        count_response = self.capability_service.get_capability_count()
        self.assertEqual(count_response.get_status_code(), 200)

    def test_d_update_capability(self) -> None:
        update_response = self.capability_service.update_capability(self.capability.get('id'), 'sdk_new_alt_id',
                                                                    'sdk_new_name')
        self.assertEqual(update_response.get_status_code(), 200)
        self.assertEqual(update_response.get_result().get('name'), 'sdk_new_name')

    def test_e_get_capability(self) -> None:
        get_response = self.capability_service.get_capability(self.capability.get('id'))
        self.assertEqual(get_response.get_status_code(), 200)

    def test_f_delete_capability(self) -> None:
        delete_response = self.capability_service.delete_capability(self.capability.get('id'))
        self.assertEqual(delete_response.get_status_code(), 200)
        self.is_deleted = True

    def tearDown(self) -> None:
        if self.capability is not None and self.capability.get('id') is not None and self.is_deleted is not True:
            delete_response = self.capability_service.delete_capability(self.capability.get('id'))
            self.assertEqual(delete_response.get_status_code(), 200)

