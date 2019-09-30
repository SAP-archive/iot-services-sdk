""" Author: Philipp Steinrötter (steinroe) """

import json

from .tenant_iot_service import TenantIoTService
from .utils import build_query
from .response import Response


class CapabilityService(TenantIoTService):
    def __init__(self,
                 instance,
                 user,
                 password,
                 tenant_id):
        """Instantiate CapabilityService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
            tenant_id {string} -- Id of the tenant
        """

        self.service = '/capabilities'

        TenantIoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password,
            tenant_id=tenant_id
        )

    def get_capabilities(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of capabilities.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for attributes of a capability. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"] (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result set (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """

        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, headers=None, payload=None, accept_json=True,
                                    query=query)

    def create_capability(self, alternate_id: str, name: str, properties: list) -> Response:
        """This endpoint is used to create a capability.
        
        Arguments:
            alternate_id {str} -- Alternate ID of the capability
            name {str} -- Name of the capability
            properties {list} -- List of dicts describing the properties
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"alternateId": alternate_id, "name": name, "properties": properties})
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload,
                                    accept_json=True)

    def get_capability_count(self) -> Response:
        """The endpoint returns the count of all capabilities.

        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='GET', service=service, accept_json=True)

    def delete_capability(self, capability_id: str) -> Response:
        """The endpoint is used to delete the capability associated to the given id.
        
        Arguments:
            capability_id {str} -- Unique identifier of a capability
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + capability_id
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_capability(self, capability_id: str) -> Response:
        """The endpoint returns the capability associated to the given id.
        
        Arguments:
            capability_id {str} -- Unique identifier of a capability.
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + capability_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_capability(self, capability_id: str, alternate_id: str = None, name: str = None, properties: list = None) -> Response:
        """This endpoint is used to update the capability associated to the given id with details specified in the request body.
        
        Arguments:
            capability_id {str} -- Unique identifier of a capability
            alternate_id {str} -- Alternate identifier of a capability
            name {str} -- Name of a capability
            properties {list} -- Properties of the capability
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + capability_id
        headers = {'Content-Type': 'application/json'}
        payload = {}
        if alternate_id is not None:
            payload['alternateId'] = alternate_id
        if name is not None:
            payload['name'] = name
        if properties is not None:
            payload['properties'] = properties
        payload_json = json.dumps(payload)
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload_json, accept_json=True)
