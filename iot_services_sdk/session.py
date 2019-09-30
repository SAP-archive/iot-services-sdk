""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService
from .response import Response


class SessionService(IoTService):
    def __init__(self,
                 instance,
                 user,
                 password):
        """Instantiate SessionService object

        Arguments:
            instance {string} -- IoT Services instance
            user {string} -- IoT Services user
            password {string} -- IoT Services password
        """

        self.service = ''

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def logout(self) -> Response:
        """Logs out the user by invalidating the session. The user is identified via session cookie or the
        Authorization header. """
        service = '/logout'
        response = self.request_core(method='POST', service=service, accept_json=True)
        return response

    def me(self) -> Response:
        """The current user is identified via session cookie or the Authorization header."""
        service = '/me'
        response = self.request_core(method='POST', service=service, accept_json=True)
        return response
