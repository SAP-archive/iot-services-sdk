""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService
from .utils import build_query
from .response import Response


class ProtocolService(IoTService):
    def __init__(self,
                 instance,
                 user,
                 password):
        """Instantiate ProtocolService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """
        self.service = '/protocols'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_protocols(self, skip: int, top: int) -> Response:
        """The endpoint returns a list of protocols available on the instance.
        
        Arguments:
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request
        
        Returns:
            Response -- Response object
        """
        query = build_query(skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, query=query, accept_json=True)

    def get_protocol_count(self):
        """The endpoint returns the count of all protocols.

        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='GET', service=service, accept_json=True)

    def create_protocol(self, protocol_id: str) -> Response:
        """he endpoint is used to create a protocol. The new protocol is visible for all tenants of the instance.
        
        Arguments:
            protocol_id {str} -- ID of the protocol that will be created
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = '{ "id" : "' + protocol_id + '" }'
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload,
                                    accept_json=True)

    def delete_protocol(self, protocol_id: str) -> Response:
        """The endpoint is used to delete a protocol. Deleting is possible only if no tenant on the instance is using it anymore.
        
        Arguments:
            protocol_id {str} -- Unique identifier of a protocol.
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + protocol_id
        return super().request_core(method='DELETE', service=service, accept_json=True)
