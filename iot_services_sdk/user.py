""" Author: Philipp Steinrötter (steinroe) """

import json

from .iot_service import IoTService
from .utils import build_query
from .response import Response


class UserService(IoTService):
    def __init__(self,
                 instance,
                 user,
                 password):
        """Instantiate UserService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = '/users'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_users(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of users.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for attributes of a user.  The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"]. (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, query=query, accept_json=True)

    def create_user(self, name: str, password: str, custom_properties=[]) -> Response:
        """The endpoint is used to create a user. Note: This function only supports basic authentication method.
        
        Arguments:
            name {str} -- Name of the user
            password {str} -- Password of the user
            custom_properties {list} -- Custom properties for the user given as list of dicts each with the key-value pairs 'key' and 'value'
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"name": name, "customProperties": custom_properties,
                              "authentications": [{"type": "basic", "password": password}]})
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload,
                                    accept_json=True)

    def get_user_count(self) -> Response:
        """The endpoint is used to delete the user associated to the given id.

        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='GET', service=service, accept_json=True)

    def delete_user(self, user_id: str) -> Response:
        """The endpoint is used to delete the user associated to the given id.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_user(self, user_id: str) -> Response:
        """The endpoint returns the user associated to the given id.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_password(self, user_id: str, password: str) -> Response:
        """The endpoint is used to update the password of the user associated to the given id.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            password {str} -- Password that will be updated
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/authentications/basic'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "password": "' + password + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def add_custom_property(self, user_id: str, key: str, value: str) -> Response:
        """The endpoint is used to add a custom property to the user associated to the given id.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            key {str} -- Key of the custom property that will be created
            value {str} -- Value of the custom property that will be created
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/customProperties'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_custom_property(self, user_id: str, key: str) -> Response:
        """The endpoint is used to delete a custom property from the user associated to the given id.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            key {str} -- Key of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/customProperties/' + key
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def update_custom_property(self, user_id: str, key: str, value: str) -> Response:
        """The endpoint is used to update a custom property of the user associated to the given id. The ‘key’ attribute cannot be modified.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/customProperties/' + key
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def add_role(self, user_id: str, role: str) -> Response:
        """The endpoint is used to add a role to user associated to the given id. The role is valid across the instance.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            role {str} -- Specification of the role that will be created
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/roles'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "role" : "' + role + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_role(self, user_id: str, role: str) -> Response:
        """The endpoint is used to delete the role from user associated to the given id. The role is valid across the instance.
        
        Arguments:
            user_id {str} -- Unique identifier of a user
            role {str} -- Name of the role
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/roles/' + role
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_tenants(self, user_id: str) -> Response:
        """The endpoint returns a list of tenants assigned to the user associated with the given id.

        Arguments:
            user_id {str} -- Unique identifier of a user

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + user_id + '/tenants'
        return super().request_core(method='GET', service=service, accept_json=True)
