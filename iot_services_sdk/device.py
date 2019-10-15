""" Author: Philipp Steinrötter (steinroe) """

import json

from .tenant_iot_service import TenantIoTService
from .mqtt_client import MQTTClient
from .rest_client import RestClient
from .utils import build_query
from .response import Response


class DeviceService(TenantIoTService):
    def __init__(self,
                 instance,
                 user,
                 password,
                 tenant_id):
        """Instantiate DeviceService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
            tenant_id {string} -- Id of the tenant
        """

        self.service = '/devices'

        TenantIoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password,
            tenant_id=tenant_id
        )

    def get_devices(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of devices.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for specific attributes. It is possible to filter by 'id’, 'alternateId’, 'gatewayId’, 'name’, 'description’, and 'status’. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"]. (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result set (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, headers=None, payload=None, accept_json=True,
                                    query=query)

    def create_device(self, gateway_id: str, name: str, as_router=False, custom_properties=None) -> Response:
        """This endpoint is used to create a device.
        
        Arguments:
            gateway_id {str} -- Unique identifier of a gateway
            name {str} -- Unique identifier of a name
            custom_properties {list} -- List of dicts with the keys 'key' and 'value' specifying the custom properties

        Returns:
            Response --  Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = {"gatewayId": gateway_id, "name": name, "customProperties": custom_properties}
        if as_router is True:
            payload['authorizations'] = [{'type': 'router'}]
        payload_json = json.dumps(payload)
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload_json,
                                    accept_json=True)

    def get_device_count(self) -> Response:
        """The endpoint returns the count of all devices.

        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='GET', service=service, accept_json=True)

    def delete_device(self, device_id: str) -> Response:
        """The endpoint is used to delete the device associated to the given id.

        Arguments:
            device_id {str} -- Unique identifier of a device
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id
        return super().request_core(method='DELETE', service=service)

    def get_device(self, device_id: str) -> Response:
        """The endpoint returns the device associated to the given id.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_device(self, device_id: str, name: str) -> Response:
        """This endpoint is used to update the device associated to the given id with details specified in the request body. This endpoint can only be used to modify a devices name. To update custom properties, sensors or authentications, use the respective APIs.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
            name {str} -- New device name
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id
        headers = {'Content-Type': 'application/json'}
        payload = '{ "name" : "' + name + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def get_device_certs(self, device_id: str) -> Response:
        """The endpoint is used to list the fingerprints and expiration dates for device certificates of the given device.

        Arguments:
            device_id {str} -- Unique identifier of a device

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/authentications/clientCertificate'
        return super().request_core(method='GET', service=service, accept_json=True)

    def get_device_p12(self, device_id: str) -> Response:
        """The endpoint is used to download device specific p12 file for authentication.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/authentications/clientCertificate/p12'
        return super().request_core(method='GET', service=service, accept_json=True)

    def get_device_pem(self, device_id: str) -> Response:
        """Used to download a device specific private key and certificate in PEM format for authentication.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/authentications/clientCertificate/pem'
        return super().request_core(method='GET', service=service, accept_json=True)

    def create_device_pem(self, device_id: str, csr: str) -> Response:
        """The endpoint is used to create a device specific certificate in PEM format for authentication.

        Arguments:
            device_id {str} -- Unique identifier of a device
            request {dict} -- Specification of the certificate signing request for the device certificate.

        Returns:
            Response -- Response object
        """
        # service = self.service + '/' + device_id + '/authentications/clientCertificate/pem'
        # headers = {'Content-Type': 'application/json'}
        # payload = json.dumps({
        #     'csr': csr,
        #     'type': 'clientCertificate'
        # })
        # return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)
        raise NotImplementedError('This method is not supported yet.')

    def revoke_device_cert(self, device_id: str, fingerprint: str) -> Response:
        """The endpoint is used to revoke a certificate of the given device.

        Arguments:
            device_id {str} -- Unique identifier of a device
            fingerprint {str} -- The fingerprint of the certificate hashed with SHA-256 in hex format.

        Returns:
            Response -- Response object
        """
        # service = self.service + '/' + device_id + '/authentications/clientCertificate/' + fingerprint
        # return super().request_core(method='DELETE', service=service)
        raise NotImplementedError('This method is not supported yet.')

    def send_command_to_device(self, device_id: str, capability_id: str, sensor_id: str, command: dict) -> Response:
        """Used to send the command specified in the request body to the device associated to the given id.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
            capability_id {str} -- Unique identifier of a capability
            sensor_id {str} -- Unique identifier of a sensor
            command {dict} --  Dict with additional properties and their respective values
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/commands'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"capabilityId": capability_id, "sensorId": sensor_id, "command": command})
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def add_custom_property(self, device_id: str, key: str, value: str) -> Response:
        """Used to add a custom property to the device associated to the given id.
        
        Arguments:
            device_id {str} --  Unique identifier of a device
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/customProperties'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_custom_property(self, device_id: str, key: str) -> Response:
        """Delete a custom property from the device associated to the given id.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
            key {str} -- Key of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/customProperties/' + key
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def update_custom_property(self, device_id: str, key: str, value: str) -> Response:
        """Updates a custom property of the device associated to the given id. The ‘key’ attribute cannot be modified.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
            key {str} -- Key of the custom property
            value {str} -- The updated value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/customProperties/' + key
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def get_mqtt_client(self, device_alternate_id: str, pemfile: str, secret: str) -> MQTTClient:
        """Returns MQTT client for specified router device
        
        Arguments:
            device_alternate_id {str} -- Alternate identifier of a device
            certfile_path {str} -- Path to the certfile
            keyfile_path {str} -- Path to the keyfile
        
        Returns:
            MQTTClient -- The MQTTClient object configured for the specified router device
        """
        return MQTTClient(self.instance, device_alternate_id, pemfile, secret)

    def get_rest_client(self, device_alternate_id: str, pemfile: str, secret: str) -> RestClient:
        """Returns REST client for specified device
        
        Arguments:
            device_alternate_id {str} -- Alternate identifier of a device
            certfile_path {str} -- Path to the certfile
            keyfile_path {str} -- Path to the keyfile
        
        Returns:
            RestClient -- The RestClient object configured for the specified device
        """
        return RestClient(self.instance, device_alternate_id, pemfile, secret)

    def get_measures(self, device_id: str, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """Returns a list of measures related to the device associated to the given id.
        
        Arguments:
            device_id {str} -- Unique identifier of a device
        
        Keyword Arguments:
            filter {list} -- This parameter allows clients to filter the collection for specific attributes. It is possible to filter by ‘capabilityId’ and 'timestamp’. When filtering by ‘timestamp’ the following binary operator are supported 'le’, 'lt’, 'ge’, and 'gt’. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"] (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result set (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request (default: {None})
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + device_id + '/measures'
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=service, query=query, accept_json=True)
