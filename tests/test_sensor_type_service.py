import unittest

from .config import get_config

from iot_services_sdk import SensorTypeService


class SensorTypeServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        config = get_config()

        self.sensor_type_service = SensorTypeService(instance=config['IOTS']['instance'],
                                                     user=config['IOTS']['user'],
                                                     password=config['IOTS']['password'])

    def test_get_sensor_types(self) -> None:
        pass

    def test_get_sensor_type_count(self) -> None:
        pass

    def test_create_sensor_type(self) -> None:
        pass

    def test_delete_sensor_type(self) -> None:
        pass

    def test_get_sensor_type(self) -> None:
        pass

    def test_update_sensor_type(self) -> None:
        pass

    def test_add_capability(self) -> None:
        pass

    def test_remove_capability(self) -> None:
        pass

    def test_update_capability(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
