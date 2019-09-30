import unittest

from .config import get_config

from iot_services_sdk import UserService


class UserServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.user_service = UserService(instance=config['IOTS']['instance'],
                                        user=config['IOTS']['user'],
                                        password=config['IOTS']['password'])

    def test_get_users(self) -> None:
        pass

    def test_create_user(self) -> None:
        pass

    def test_get_user_count(self) -> None:
        pass

    def test_delete_user(self) -> None:
        pass

    def test_get_user(self) -> None:
        pass

    def test_update_password(self) -> None:
        pass

    def test_add_custom_property(self) -> None:
        pass

    def test_delete_custom_property(self) -> None:
        pass

    def test_update_custom_property(self) -> None:
        pass

    def test_add_role(self) -> None:
        pass

    def test_delete_role(self) -> None:
        pass

    def test_get_tenants(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
