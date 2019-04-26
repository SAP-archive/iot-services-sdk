""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService, Response
from .utils import build_query

class GatewayService(IoTService):
    def __init__(self,
                instance,
                user,
                password):
        """Instantiate GatewayService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = '/gateways'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_gateways(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of gateways.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for specific attributes. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"] (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result set (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        response = self.request_core(method='GET', service=self.service, query=query, accept_json=True)
        return response

    def delete_gateway(self, gateway_id: str) -> Response:
        """The endpoint is used to delete the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response

    def get_gateway(self, gateway_id: str) -> Response:
        """The endpoint returns the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id
        response = self.request_core(method='GET', service=service, accept_json=True)
        return response

    def update_gateway_name(self, gateway_id: str, name: str) -> Response:
        """The endpoint is used to update the gateway associated to the given id with details specified in the request body. To update custom properties, bundles or configuration, use the respective APIs.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            name {str} -- Name for the gateway
        
        Returns:
            Response -- Response object
        """

        service = self.service + '/' + gateway_id
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "name" : "' + name + '" }'
        response = self.request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
        return response

    def get_gateway_osgi_bundles(self, gateway_id: str) -> Response:
        """The endpoint returns a list of installed OSGi bundles.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles'
        response = self.request_core(method='GET', service=service, accept_json=True)
        return response

    def install_gateway_osgi_bundle(self, gateway_id: str, osgi_bundle: str) -> Response:
        """This endpoint is used to install an OSGi bundle on the gateway associated to the given id. Note that bundles with a file size over 128 MB will be rejected. The installation takes place asynchronously: the provided bundle is stored on the system (where it is kept up to 24 hours), then a request to download it is dispatched to Gateway. As soon as it receives the request, Gateway initiates the bundle download. The API returns immediately after the download request is dispatched to Gateway; in order to inspect the outcome of the bundle installation, get_gateway_osgi_bundles() should be used
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            osgi_bundle {str} -- Gateway OSGi Bundle
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles'
        response = self.request_core(method='POST', service=service, accept_json=True, files=osgi_bundle)
        return response

    def delete_osgi_bundle(self, gateway_id: str, bundle_id: str) -> Response:
        """This endpoint is used to remove an OSGi bundle from the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            bundle_id {str} -- Unique identifier of an OSGi bundle
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles/' + bundle_id
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response

    def get_osgi_bundle(self, gateway_id: str, bundle_id: str) -> Response:
        """The endpoint returns the OSGi bundle associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            bundle_id {str} -- Unique identifier of an OSGi bundle
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles/' + bundle_id
        response = self.request_core(method='GET', service=service, accept_json=True)
        return response

    def start_gateway_osgi_bundle(self, gateway_id: str, bundle_id: str) -> Response:
        """This endpoint is used to start the OSGi bundle of the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            bundle_id {str} -- Unique identifier of an OSGi bundle
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles/' + bundle_id + '/start'
        response = self.request_core(method='POST', service=service, accept_json=True)
        return response

    def stop_gateway_osgi_bundle(self, gateway_id: str, bundle_id: str) -> Response:
        """This endpoint is used to stop the OSGi bundle of the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            bundle_id {str} -- Unique identifier of an OSGi bundle
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/bundles/' + bundle_id + '/stop'
        response = self.request_core(method='POST', service=service, accept_json=True)
        return response

    def get_gateway_configuration(self, gateway_id: str) -> Response:
        """The endpoint is used to download the gateway specific configuration XML file.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/configuration'
        response = self.request_core(method='GET', service=service)
        return response

    def update_gateway_configuration(self, gateway_id: str, xml: str) -> Response:
        """The endpoint is used to update the gateway specific configuration by uploading a configuration XML file.
        
        Arguments:
            gateway_id {str} -- The endpoint is used to update the gateway specific configuration by uploading a configuration XML file.
            xml {str} -- XML file as string containing the Gateway configuration
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/configuration'
        headers = {'Content-Type' : 'application/xml'}
        payload = xml
        response = self.request_core(method='PUT', service=service, payload=payload, headers=headers)
        return response

    def add_custom_property(self, gateway_id: str, key: str, value: str) -> Response:
        """The endpoint is used to add a custom property to the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/customProperties'
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        response = self.request_core(method='POST', service=service, payload=payload, headers=headers, accept_json=True)
        return response

    def delete_custom_property(self, gateway_id: str, key: str) -> Response:
        """This endpoint is used to delete a custom property from the gateway associated to the given id.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            key {str} -- Key of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + gateway_id + '/customProperties/' + key
        response = self.request_core(method='DELETE', service=service, accept_json=True)
        return response

    def update_custom_property(self, gateway_id: str, key: str, value: str) -> Response:
        """The endpoint is used to update a custom property of the gateway associated to the given id. The ‘key’ attribute cannot be modified.

        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            key {str} -- Key of the custom property
            value {str} -- Updates value of the custom property
        
        Returns:
            Response -- Response object
        """

        service = self.service + '/' + gateway_id + '/customProperties/' + key
        headers = {'Content-Type' : 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        response = self.request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
        return response
    