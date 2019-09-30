""" Author: Philipp Steinrötter (steinroe) """

import unittest

from .config import get_config

from iot_services_sdk import ProtocolService


class ProtocolServiceTest(unittest.TestCase):

    def setUp(self):
        config = get_config()

        self.protocol_service = ProtocolService(instance=config['IOTS']['instance'],
                                                user=config['IOTS']['user'],
                                                password=config['IOTS']['password'])

    def test_get_protocols(self) -> None:
        pass

    def test_get_protocol_count(self) -> None:
        pass

    def test_create_protocol(self) -> None:
        pass

    def test_delete_protocol(self) -> None:
        pass
