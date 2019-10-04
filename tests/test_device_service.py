""" Author: Philipp Steinrötter (steinroe) """

import unittest

from .config import get_config

from iot_services_sdk import DeviceService, GatewayService, DeviceManagementAPIException


class DeviceServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        config = get_config()

        self.device_service = DeviceService(instance=config['IOTS']['instance'],
                                            user=config['IOTS']['user'],
                                            password=config['IOTS']['password'],
                                            tenant_id=config['IOTS']['tenant_id'])

        self.gateway_service = GatewayService(instance=config['IOTS']['instance'],
                                            user=config['IOTS']['user'],
                                            password=config['IOTS']['password'],
                                            tenant_id=config['IOTS']['tenant_id'])

        # Get REST Gateway
        filters = ["status eq 'online'"]
        gateways_response = self.gateway_service.get_gateways(filters=filters)
        self.assertEqual(gateways_response.get_status_code(), 200)

        gateways = gateways_response.get_result()
        self.rest_gateway = next(gateway for gateway in gateways if gateway['protocolId'] == 'rest')

        create_response = self.device_service.create_device(self.rest_gateway.get('id'), 'sdk_device')

        self.device = create_response.get_result()
        self.is_deleted = False

    def test_a_create_device(self) -> None:
        # Is tested in setup
        pass

    def test_b_get_devices(self) -> None:
        filters = ["id eq '" + self.device.get('id') + "'"]
        get_response = self.device_service.get_devices(filters=filters)
        devices = get_response.get_result()
        self.assertEqual(get_response.get_status_code(), 200)
        self.assertEqual(self.device.get('id'), devices[0].get('id'))

    def test_c_get_device_count(self) -> None:
        count_response = self.device_service.get_device_count()
        self.assertEqual(count_response.get_status_code(), 200)

    def test_d_update_device(self) -> None:
        update_response = self.device_service.update_device(self.device.get('id'), 'sdk_new_name')
        self.assertEqual(update_response.get_status_code(), 200)

    def test_e_get_device(self) -> None:
        get_device_response = self.device_service.get_device(self.device.get('id'))
        self.assertEqual(get_device_response.get_status_code(), 200)

    def test_f_get_device_certs(self) -> None:
        try:
            self.device_service.get_device_certs(self.device.get('id'))
            self.assertEqual(0, 1)
        except DeviceManagementAPIException:
            self.assertEqual(0, 0)

    def test_g_get_device_p12(self) -> None:
        get_p12_response = self.device_service.get_device_p12(self.device.get('id'))
        self.assertEqual(get_p12_response.get_status_code(), 200)

    def test_h_get_device_pem(self) -> None:
        get_pem_response = self.device_service.get_device_pem(self.device.get('id'))
        self.assertEqual(get_pem_response.get_status_code(), 200)

    def test_i_create_device_pem(self) -> None:
        pass

    def test_j_revoke_device_cert(self) -> None:
        pass

    def test_k_send_command_to_device(self) -> None:
        pass

    def test_l_add_custom_property_to_device(self) -> None:
        pass

    def test_m_delete_custom_property(self) -> None:
        pass

    def test_n_update_custom_property(self) -> None:
        pass

    def test_o_get_mqtt_client(self) -> None:
        pass

    def test_p_get_rest_client(self) -> None:
        pass

    def test_q_get_measures(self) -> None:
        pass

    def test_r_delete_device(self) -> None:
        delete_response = self.device_service.delete_device(self.device.get('id'))
        self.assertEqual(delete_response.get_status_code(), 200)
        self.is_deleted = True

    def tearDown(self) -> None:
        if self.device is not None and self.device.get('id') is not None and self.is_deleted is not True:
            delete_response = self.device_service.delete_device(self.device.get('id'))
            self.assertEqual(delete_response.get_status_code(), 200)
