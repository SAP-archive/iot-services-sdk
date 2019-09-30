import unittest

from .config import get_config

from iot_services_sdk import VendorService


class VendorServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.vendor_service = VendorService(instance=config['IOTS']['instance'],
                                            user=config['IOTS']['user'],
                                            password=config['IOTS']['password'])

    def test_get_vendors(self) -> None:
        pass

    def test_get_vendor_count(self) -> None:
        pass

    def test_create_vendor(self) -> None:
        pass

    def test_delete_vendor(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
