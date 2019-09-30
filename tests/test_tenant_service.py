import unittest

from .config import get_config

from iot_services_sdk import TenantService


class TenantServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.tenant_service = TenantService(instance=config['IOTS']['instance'],
                                            user=config['IOTS']['user'],
                                            password=config['IOTS']['password'])

    def test_get_tenants(self) -> None:
        pass

    def test_create_tenant(self) -> None:
        pass

    def test_get_tenants_count(self) -> None:
        pass

    def test_delete_tenant(self) -> None:
        pass

    def test_get_tenant(self) -> None:
        pass

    def test_update_tenant(self) -> None:
        pass

    def test_add_custom_property(self) -> None:
        pass

    def test_delete_custom_property(self) -> None:
        pass

    def test_update_custom_property(self) -> None:
        pass

    def test_get_trusted_ca_certificates(self) -> None:
        pass

    def test_get_gateway_registration_client_cert(self) -> None:
        pass

    def test_get_gateway_registration_client_cert_p12(self) -> None:
        pass

    def test_get_gateway_registration_client_cert_pem(self) -> None:
        pass

    def test_revoke_gateway_cert(self) -> None:
        pass

    def test_get_users(self) -> None:
        pass

    def test_add_user(self) -> None:
        pass

    def test_delete_user(self) -> None:
        pass

    def test_get_user(self) -> None:
        pass

    def test_update_user(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
