""" Author: Philipp Steinrötter (steinroe) """

import requests
import json
from .response import Response


class DeviceManagementAPIException(Exception):
    pass


class IoTService(object):
    def __init__(self, instance: str, user: str, password: str):
        """Instantiate IoT Service object
        
        Arguments:
            instance {str} -- IoT Service instance
            user {str} -- IoT Service user
            password {str} -- IoT Service password
        
        Raises:
            ValueError -- Raised if any argument is not provided
        """
        if instance is None or user is None or password is None:
            raise ValueError('You must specify your instance, user and password.')

        self.instance = instance
        self.user = user
        self.password = password

        self._api_path = '/iot/core/api/v1'

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

        url = 'https://' + self.instance + self._api_path + service
        if query is not None:
            url = url + query

        user = self.user
        password = self.password

        try:
            response = requests.request(method, url, headers=headers, auth=(user, password), data=payload, files=files)
            response.raise_for_status()
            if accept_json:
                response_json = json.loads(response.text)
                return Response(response.status_code, response_json, response.headers)
            else:
                return Response(response.status_code, response.text, response.headers)
        except requests.exceptions.HTTPError as err:
            try:
                raise DeviceManagementAPIException(json.loads(err.response.text)['message'])
            except json.decoder.JSONDecodeError:
                raise DeviceManagementAPIException(err)
