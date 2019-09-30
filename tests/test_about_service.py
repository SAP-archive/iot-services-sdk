""" Author: Philipp Steinrötter (steinroe) """

import unittest

from .config import get_config

from iot_services_sdk import AboutService


class AboutServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        config = get_config()

        self.about_service = AboutService(instance=config['IOTS']['instance'],
                                          user=config['IOTS']['user'],
                                          password=config['IOTS']['password'])

    def test_get_information(self) -> None:
        get_information_response = self.about_service.get_information()
        self.assertEqual(get_information_response.get_status_code(), 200)
