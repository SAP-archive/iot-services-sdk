""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService, Response
from .utils import build_query

class VendorService(IoTService):
    def __init__(self,
                instance,
                user,
                password):
        """Instantiate VendorService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = '/vendors'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_vendors(self, skip=None, top=None) -> Response:
        """The endpoint returns a list of vendors, shared among all tenants of the instance.
        
        Keyword Arguments:
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(skip=skip, top=top)
        response = self.request_core(method='GET', service=self.service, query=query, accept_json=True)
        return response

    def create_vendor(self, vendor_id: str) -> Response:
        """The endpoint is used to create a new vendor. The new vendor is visible for all tenants of the instance.
        
        Arguments:
            vendor_id {str} -- ID of the vendor that will be created
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "id": "' + vendor_id + '" }'
        response = self.request_core(method='POST', service=self.service, headers=headers, payload=payload, accept_json=True)
        return response

    def delete_vendor(self, vendor_id: str) -> Response:
        """The endpoint is used to delete a vendor. Deleting is possible only if no tenant on the instance is using it anymore.
        
        Arguments:
            vendor_id {str} -- Unique identifier of a vendor
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + vendor_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response