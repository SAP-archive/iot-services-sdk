""" Author: Philipp Steinrötter (steinroe) """

from .iot_service import IoTService, Response

class AboutService(IoTService):
    def __init__(self,
                instance,
                user,
                password):
        
        self.service = '/about'

        IoTService.__init__(
            self,
            instance=instance,
            user=user,
            password=password
        )

    def get_information(self) -> Response:
        """The endpoint returns information about the service and its configuration parameters.
        
        Returns:
            Response -- Response object
        """
        response = self.request_core(method='GET', service=self.service, accept_json=True)
        return response
