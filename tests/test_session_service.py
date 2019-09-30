import unittest

from .config import get_config

from iot_services_sdk import SessionService


class SessionServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.session_service = SessionService(instance=config['IOTS']['instance'],
                                              user=config['IOTS']['user'],
                                              password=config['IOTS']['password'])

    def test_logout(self) -> None:
        pass

    def test_me(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
