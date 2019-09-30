import unittest

from .config import get_config

from iot_services_sdk import GatewayService


class GatewayServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.gateway_service = GatewayService(instance=config['IOTS']['instance'],
                                              user=config['IOTS']['user'],
                                              password=config['IOTS']['password'])

    def test_get_gateways(self) -> None:
        pass

    def test_get_gateway_count(self) -> None:
        pass

    def test_delete_gateway(self) -> None:
        pass

    def test_get_gateway(self) -> None:
        pass

    def test_update_gateway_name(self) -> None:
        pass

    def test_get_gateway_certs(self) -> None:
        pass
    
    def test_create_gateway_pem(self) -> None:
        pass

    def test_revoke_gateway_cert(self) -> None:
        pass

    def test_get_gateway_osgi_bundles(self) -> None:
        pass

    def test_install_gateway_osgi_bundle(self) -> None:
        pass

    def test_delete_osgi_bundle(self) -> None:
        pass

    def test_get_osgi_bundle(self) -> None:
        pass

    def test_start_gateway_osgi_bundle(self) -> None:
        pass

    def test_stop_gateway_osgi_bundle(self) -> None:
        pass

    def test_get_gateway_configuration(self) -> None:
        pass

    def test_update_gateway_configuration(self) -> None:
        pass

    def test_add_custom_property(self) -> None:
        pass

    def test_delete_custom_property(self) -> None:
        pass

    def test_update_custom_property(self) -> None:
        pass

    def test_get_gateway_device_certs(self) -> None:
        pass

    def test_get_gateway_device_p12(self) -> None:
        pass

    def test_get_gateway_device_pem(self) -> None:
        pass

    def test_revoke_gateway_device_cert(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
