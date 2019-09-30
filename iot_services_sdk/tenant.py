""" Author: Philipp Steinrötter (steinroe) """

import json

from .iot_service import IoTService
from .utils import build_query
from .response import Response


class TenantService(IoTService):
    def __init__(self,
                 instance,
                 user,
                 password):
        """Instantiate TenantService object
        
        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = '/tenants'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_tenants(self, filters=None, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of tenants.
        
        Keyword Arguments:
            filters {list} -- This parameter allows clients to filter the collection for attributes of a tenant. The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"]. (default: {None})
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result set. (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request. (default: {None})
        
        Returns:
            Response -- Response object
        """
        query = build_query(filters=filters, orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=self.service, query=query, accept_json=True)

    def create_tenant(self, name: str, custom_properties=[]) -> Response:
        """The endpoint is used to create a tenant.
        
        Arguments:
            name {str} -- Name of the tenant
            custom_properties {list} -- Custom properties of the tenant as a list of dicts, each with the key-value pairs 'key' and 'value'
        
        Returns:
            Response -- Response object
        """
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"name": name, "customProperties": custom_properties})
        return super().request_core(method='POST', service=self.service, headers=headers, payload=payload,
                                    accept_json=True)

    def get_tenants_count(self) -> Response:
        """Returns the count of all tenants.
        Returns:
            Response -- Response object
        """
        service = self.service + '/count'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_tenant(self, tenant_id: str) -> Response:
        """The endpoint is used to delete the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_tenant(self, tenant_id: str) -> Response:
        """The endpoint returns the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_tenant(self, tenant_id: str, name: str) -> Response:
        """The endpoint is used to update the tenant associated to the given id with details specified in the request body. To update custom properties or users, use the respective APIs.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            name {str} -- Name of the tenant
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id
        headers = {'Content-Type': 'application/json'}
        payload = '{ "name" : "' + name + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def add_custom_property(self, tenant_id: str, key: str, value: str) -> Response:
        """The endpoint is used to add a custom property to the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/customProperties'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_custom_property(self, tenant_id: str, custom_property_key: str) -> Response:
        """This endpoint is used to delete a custom property from the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            custom_property_key {str} -- Key of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/customProperties/' + custom_property_key
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def update_custom_property(self, tenant_id: str, key: str, value: str) -> Response:
        """The endpoint is used to update a custom property of the tenant associated to the given id. The ‘key’ attribute cannot be modified.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            key {str} -- Key of the custom property
            value {str} -- Value of the custom property
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/customProperties/' + key
        headers = {'Content-Type': 'application/json'}
        payload = '{ "key" : "' + key + '", "value" : "' + value + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)

    def get_trusted_ca_certificates(self, tenant_id: str) -> Response:
        """The endpoint is used to download tenant specific trusted CA certificates for authentication.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/trustedCACertificates'
        return super().request_core(method='GET', service=service, accept_json=True)

    def get_gateway_registration_client_cert(self, tenant_id: str) -> Response:
        """The endpoint is used to list the fingerprints and expiration dates for gateway registration certificates of the given tenant.

        Arguments:
            tenant_id {str} -- Unique identifier of a tenant

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/gatewayRegistrations/clientCertificate'
        return super().request_core(method='GET', service=service, accept_json=True)

    def get_gateway_registration_client_cert_p12(self, tenant_id: str) -> Response:
        """The endpoint is used to download tenant specific p12 file for the registration of a gateway.

        Arguments:
            tenant_id {str} -- Unique identifier of a tenant

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/gatewayRegistrations/clientCertificate/p12'
        return super().request_core(method='GET', service=service, accept_json=True)

    def get_gateway_registration_client_cert_pem(self, tenant_id: str) -> Response:
        """The endpoint is used to download tenant specific pem file for the registration of a gateway.

        Arguments:
            tenant_id {str} -- Unique identifier of a tenant

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/gatewayRegistrations/clientCertificate/pem'
        return super().request_core(method='GET', service=service, accept_json=True)

    def revoke_gateway_cert(self, tenant_id: str, fingerprint: str) -> Response:
        """The endpoint is used to revoke a gateway registration certificate of the given tenant.

        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            fingerprint {str} -- The fingerprint of the certificate hashed with SHA-256 in hex format.

        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/gatewayRegistrations/clientCertificate/' + fingerprint
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_users(self, tenant_id: str, orderby=None, asc=True, skip=None, top=None) -> Response:
        """The endpoint returns a list of users assigned to the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
        
        Keyword Arguments:
            orderby {str} -- The attribute to order by. (default: {None})
            asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered asc or desc. (default: {True})
            skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore not included in the result set. (default: {None})
            top {int} -- This parameter restricts the maximum number of items which will be returned by the request. (default: {None})
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/users'
        query = build_query(orderby=orderby, asc=asc, skip=skip, top=top)
        return super().request_core(method='GET', service=service, query=query, accept_json=True)

    def add_user(self, tenant_id: str, role: str, user_id: str) -> Response:
        """The endpoint is used to add the user specified in the request body to the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            role {str} -- Role of the user
            user_id {str} -- ID of the user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/users'
        headers = {'Content-Type': 'application/json'}
        payload = '{ "role" : "' + role + '", "userId" : "' + user_id + '" }'
        return super().request_core(method='POST', service=service, headers=headers, payload=payload, accept_json=True)

    def delete_user(self, tenant_id: str, user_id: str) -> Response:
        """The endpoint is used to remove the user from the tenant associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            user_id {str} -- Unique identifier of a user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/users/' + user_id
        return super().request_core(method='DELETE', service=service, accept_json=True)

    def get_user(self, tenant_id: str, user_id: str) -> Response:
        """The endpoint is used to return the tenant user associated to the given id.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            user_id {str} -- Unique identifier of a user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/users/' + user_id
        return super().request_core(method='GET', service=service, accept_json=True)

    def update_user(self, tenant_id: str, user_id: str, role: str) -> Response:
        """The endpoint is used to update the tenant user associated to the given id with details specified in the request body.
        
        Arguments:
            tenant_id {str} -- Unique identifier of a tenant
            user_id {str} -- Unique identifier of a user
            role {str} -- Role of the user
        
        Returns:
            Response -- Response object
        """
        service = self.service + '/' + tenant_id + '/users/' + user_id
        headers = {'Content-Type': 'application/json'}
        payload = '{ "role" : "' + role + '", "userId" : "' + user_id + '" }'
        return super().request_core(method='PUT', service=service, headers=headers, payload=payload, accept_json=True)
