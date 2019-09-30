""" Author: Philipp Steinrötter (steinroe) """

from .tenant_iot_service import TenantIoTService
from .utils import build_query
from .response import Response


class SensorService(TenantIoTService):
    def __init__(self,
                 instance,
                 user,
                 password,
                 tenant_id):
        """Instantiate SensorService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
            tenant_id {string} -- Id of the tenant
        """

        self.service = '/sensors'

        TenantIoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password,
            tenant_id=tenant_id
        )

    def get_sensors(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of sensors.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for specific attributes. It is possible to filter by 'id’, 'deviceId’, 'name’, and 'alternateId’. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"]. (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result set. (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request. (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, query=query, accept_json=True)

    def get_sensor_count(self):
        """The endpoint returns the count of all sensors.

        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='GET', service=service, accept_json=True)

    def create_sensor(self, device_id: str, alternate_id: str, name: str, sensor_type_id: str) -> Response:
        """This endpoint is used to create a sensor.
        
        Arguments:
            device_id {str} -- Respective device ID for the sensor
            alternate_id {str} -- Alternate ID for the sensor
            name {str} -- Name for the sensor
            sensor_type_id {str} -- ID of the respective sensor type
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = '{ "deviceId": "' + device_id + '", "alternateId": "' + alternate_id + '", "name": "' + name + '", "sensorTypeId": "' + sensor_type_id + '"}'
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload,
                                    accept_json=True)

    def delete_sensor(self, sensor_id: str) -> Response:
        """The endpoint is used to delete the sensor associated to the given id.
        
        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_sensor(self, sensor_id: str) -> Response:
        """The endpoint returns the sensor associated to the given id.
        
        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_sensor(self, sensor_id: str, name: str, sensor_type_id: str) -> Response:
        """This endpoint is used to update a sensor associated to the given id with details specified in the request body.
        
        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
            name {str} -- Name of the sensor
            sensor_type_id {str} -- Respective sensor type ID
        
        Returns:
            Response -- [description]
        """
        service = self.service + '/' + sensor_id
        headers = {'Content-Type': 'application/json'}
        payload = '{ "name" : "' + name + '", "sensorTypeId" : "' + sensor_type_id + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def add_custom_property(self, sensor_id: str, key: str, value: str) -> Response:
        """The endpoint is used to add a custom property to the sensor associated to the given id.

        Arguments:
            sensor_id {str} --  Unique identifier of a sensor
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id + '/customProperties'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_custom_property(self, sensor_id: str, key: str) -> Response:
        """Delete a custom property from the sensor associated to the given id.

        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
            key {str} -- Key of the custom property

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id + '/customProperties/' + key
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def update_custom_property(self, sensor_id: str, key: str, value: str) -> Response:
        """Updates a custom property of the sensor associated to the given id. The ‘key’ attribute cannot be modified.

        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
            key {str} -- Key of the custom property
            value {str} -- The updated value of the custom property

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id + '/customProperties/' + key
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
