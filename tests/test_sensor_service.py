import unittest

from .config import get_config

from iot_services_sdk import SensorService


class SensorServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.sensor_service = SensorService(instance=config['IOTS']['instance'],
                                            user=config['IOTS']['user'],
                                            password=config['IOTS']['password'])

    def test_get_sensors(self) -> None:
        pass

    def test_get_sensor_count(self) -> None:
        pass

    def test_create_sensor(self) -> None:
        pass

    def test_delete_sensor(self) -> None:
        pass

    def test_get_sensor(self) -> None:
        pass

    def test_update_sensor(self) -> None:
        pass

    def test_add_custom_property(self) -> None:
        pass

    def test_delete_custom_property(self) -> None:
        pass

    def test_update_custom_property(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
