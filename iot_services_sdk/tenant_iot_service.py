""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService
from .response import Response


class TenantIoTService(IoTService):
    def __init__(self, instance: str, user: str, password: str, tenant_id: str):
        """Instantiate IoT Service object

        Arguments:
            instance {str} -- IoT Service instance
            user {str} -- IoT Service user
            password {str} -- IoT Service password
            tenant {str} -- IoT Service Tenant

        Raises:
            ValueError -- Raised if any required argument is not provided
        """
        if instance is None or user is None or password is None or tenant_id is None:
            raise ValueError('You must specify your instance, user and password.')

        self._tenant_id = tenant_id

        self._service_base_path = '/tenant/' + tenant_id

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    @property
    def tenant_id(self):
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        if tenant_id is None:
            raise ValueError('Tenant Id must be set. Please use IoTService base class to call a service not related '
                             'to a specific tenant.')

        self._tenant_id = tenant_id
        self._service_base_path = '/tenant/' + tenant_id

    def request_core(self, method=None, service=None, headers=None, payload=None, accept_json=False, query=None,
                     files=None) -> Response:
        """Fires a HTTP request to core services

        Keyword Arguments:
            method {str} -- HTTP method (default: {None})
            service {str} -- Service Path (default: {None})
            headers {dict} -- HTTP headers (default: {None})
            payload {str} -- Message payload (default: {None})
            accept_json {bool} -- If set to true, the response is parsed a JSON (default: {False})
            query {str} -- Query for filtering (default: {None})
            files {str} -- Path to files (default: {None})

        Returns:
            Response -- Response object
        """

        service = self._service_base_path + service
        return super().request_core(method=method, service=service, headers=headers, payload=payload, accept_json=accept_json, query=query, files=files)