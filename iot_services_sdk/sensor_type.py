""" Author: Philipp Steinrötter (steinroe) """

import json

from .iot_service import IoTService, Response
from .utils import build_query

class SensorTypeService(IoTService):
    def __init__(self,
                instance,
                user,
                password):
        """Instantiate SensorTypeService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """
        self.service = '/sensorTypes'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )
    
    def get_sensor_types(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of sensor types.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for attributes of a sensorType. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"] (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result set. (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request. (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        response = self.request_core(method='GET', service=self.service, query=query, accept_json=True)
        return response

    def create_sensor_type(self, alternate_id: str, name: str, capabilities: list) -> Response:
        """This endpoint is used to create a sensor type.
        
        Arguments:
            alternate_id {str} -- Alternate ID of the sensor type
            name {str} -- Name of the sensor type
            capabilities {list} -- List of dicts each containing key-value pairs for 'id' and 'type'
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type' : 'application/json'}
        payload = json.dumps({"alternateId": alternate_id,"name": name,"capabilities": capabilities})
        response = self.request_core(method='POST', service=self.service, headers=headers, payload=payload, accept_json=True)
        return response

    def delete_sensor_type(self, sensor_type_id: str) -> Response:
        """The endpoint is used to delete the sensor type associated to the given id.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensor type
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response

    def get_sensor_type(self, sensor_type_id: str) -> Response:
        """The endpoint returns the sensor type associated to the given id.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensor type
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id
        response = self.request_core(method='GET', service=service, accept_json=True)
        return response

    def update_sensor_type(self, sensor_type_id: str, alternate_id: str, name: str) -> Response:
        """This endpoint is used to update the sensor type associated to the given id with details specified in the request body. To update capabilities, use the respective API.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensor type
            alternate_id {str} -- Alternate identifier of the sensor type
            name {str} -- Name of the sensor type
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "alternateId" : "' + alternate_id + '", "name" : "' + name + '" }'
        response = self.request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
        return response

    def add_capability(self, sensor_type_id: str, capability_id: str, capability_type: str) -> Response:
        """This endpoint is used to add a capability. Note that it is not supported to add a capability to a sensor type which is already associated with a sensor.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensorType
            capability_id {str} -- ID of the capability that will be added
            capability_type {str} -- Type of the capability that will be added. Can be 'measure' or 'command'
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id + '/capabilities'
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "id" : "' + capability_id + '", "type" : "' + capability_type + '" }'
        response = self.request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)
        return response

    def remove_capability(self, sensor_type_id: str, capability_id: str) -> Response:
        """The endpoint is used to remove the capability associated to the given id. Note that it is not supported to delete a capability in a sensor type which is already associated with a sensor.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensorType
            capability_id {str} -- Unique identifier of a capability
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id + '/capabilities/' + capability_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response

    def update_capability(self, sensor_type_id: str, capability_id: str, capability_type: str) -> Response:
        """This endpoint is used to update the capability associated to the given id with details specified in the request body. Note that it is not supported to modify the type of a capability in a sensor type if it is already associated with a sensor.
        
        Arguments:
            sensor_type_id {str} -- Unique identifier of a sensorType
            capability_id {str} -- ID of the capability that will be updated
            capability_type {str} -- Type of the capability that will be added. Can be 'measure' or 'command'
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + sensor_type_id + '/capabilities/' + capability_id
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "id" : "' + capability_id + '", "type" : "' + capability_type + '" }'
        response = self.request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
        return response
