""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService, Response
from .utils import build_query

class SensorService(IoTService):
    def __init__(self,
                instance,
                user,
                password):
        """Instantiate SensorService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = '/sensors'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
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
        response = self.request_core(method='GET', service=self.service, query=query, accept_json=True)
        return response

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
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "deviceId": "' + device_id + '", "alternateId": "' + alternate_id + '", "name": "' + name + '", "sensorTypeId": "' + sensor_type_id + '"}'
        response = self.request_core(method='POST', service=self.service, headers=headers, payload=payload, accept_json=True)
        return response

    def delete_sensor(self, sensor_id: str) -> Response:
        """The endpoint is used to delete the sensor associated to the given id.
        
        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response        

    def get_sensor(self, sensor_id: str) -> Response:
        """The endpoint returns the sensor associated to the given id.
        
        Arguments:
            sensor_id {str} -- Unique identifier of a sensor
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_id
        response = self.request_core(method='GET', service=service, accept_json=True)
        return response

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
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "name" : "' + name + '", "sensorTypeId" : "' + sensor_type_id + '" }'
        response = self.request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
        return response
    