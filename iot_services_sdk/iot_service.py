""" Author: Philipp Steinrötter (steinroe) """

import requests
import json
import sys, os
import subprocess
import logging
import contextlib
from http.client import HTTPConnection

class DeviceManagementAPIException(Exception):
    pass

class Response(object):
    """Objects contain information received from API"""

    def __init__(self, status_code, response, headers):
        self.status_code = status_code
        self.result = response
        self.headers = headers

    def get_result(self) -> str:
        """Returns the result of the response, e.g. the body of the message
        
        Returns:
            str -- The body of the response message. Mostly in JSON formatting.
        """
        return self.result

    def get_headers(self) -> str:
        """Returns the header of the response
        
        Returns:
            str -- The header of the response message.
        """
        return self.headers

    def get_status_code(self) -> int:
        """Status code of the response
        
        Returns:
            str -- The status code of the HTTP communication
        """
        return self.status_code

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
        if (instance is None or user is None or password is None):
            raise ValueError('You must specify your instance, user and password.')
        
        self.instance = instance
        self.user = user
        self.password = password

        self.base_uri = '/iot/core/api/v1'

    def debug_requests_on(self):
        """Switches on logging of the requests module.
        """
        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def debug_requests_off(self):
        """Switches off logging of the requests module.
        """
        HTTPConnection.debuglevel = 0

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = False

    def request_core(self, method=None, service=None, headers=None, payload=None, accept_json=False, query=None, files=None) -> Response:
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

        url = 'https://' + self.instance + self.base_uri + service
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