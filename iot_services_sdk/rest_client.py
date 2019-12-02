""" Author: Philipp Steinrötter (steinroe) """

from requests.adapters import HTTPAdapter

import json
import requests
import ssl

from .response import Response
from .utils import current_milli_time


class RESTGatewayException(Exception):
    pass


class RestClient(object):

    def __init__(self, instance: str, device_alternate_id: str, pemfile: str, secret: str):
        """Instantiate REST Client configured for specified instance and device
        
        Arguments:
            instance {str} -- IoT Services instance
            device_alternate_id {str} -- The alternate id of the device
            certfile_path {str} -- The certfile path for the device
            keyfile_path {str} -- The keyfile path for the device
        """

        self.instance = instance
        self.device_alternate_id = device_alternate_id
        self.pemfile = pemfile

        self.session = self._init_session(pemfile, secret)

        self.gateway_uri = '/iot/gateway'

    def _init_session(self, pemfile: str, secret: str):
        session = requests.Session()
        adapter = RESTGatewayAdapter(pemfile=pemfile, secret=secret)
        session.mount('https://' + self.instance, adapter)
        return session

    def _request_gateway(self, service: str, headers: dict, payload: str) -> Response:
        """Fires a HTTP request against a gateway
        
        Arguments:
            service {str} -- Service path
            headers {dict} -- HTTP headers
            payload {str} -- Message payload
        
        Returns:
            Response -- Response object
        """

        service = 'https://' + self.instance + self.gateway_uri + '/rest' + service

        try:
            response = self.session.request(method='POST', url=service, data=payload, headers=headers)
            response.raise_for_status()
            if response.status_code == 207:
                # Batch upload with partial failure. Raise Exception.
                raise RESTGatewayException(self._parse_error(json.loads(response.text)))
            return Response(response.status_code, json.loads(response.text), response.headers)
        except requests.exceptions.HTTPError as err:
            raise RESTGatewayException(self._parse_error(json.loads(err.response.text)))

    def _parse_error(self, message_infos) -> str:
        messages = ''
        for msg in message_infos:
            if msg.get('messages') is not None:
                messages += ' '.join(msg['messages'])

    def post_command(self, capability_alternate_id: str, sensor_alternate_id: str, command: dict, device_alternate_id: str = None) -> Response:
        """Post commands over rest gateway for specified device
        
        Arguments:
            device_alternate_id {str} -- Alternate ID of the device. If none, the device from the client id will be used.
            capability_alternate_id {str} -- Alternate ID for capability
            sensor_alternate_id {str} -- Alternate ID for sensor
            command {dict} -- Dict with the keys and respective values of the desired commands
        
        Returns:
            Response -- Response object
        """
        if device_alternate_id is None:
            device_alternate_id = self.device_alternate_id

        service = '/commands/' + device_alternate_id
        headers = {'Content-Type': 'application/json'}
        payload_json = json.dumps(
            {"capabilityAlternateId": capability_alternate_id, "sensorAlternateId": sensor_alternate_id,
             "command": command})
        response = self._request_gateway(service=service, headers=headers, payload=payload_json)
        return response

    def post_measures(self, capability_alternate_id: str, sensor_alternate_id: str, measures: list,
                      sensor_type_alternate_id: int = None, use_timestamp: bool = False, timestamp: int = None, device_alternate_id: str = None) -> Response:
        """Post measures over rest gateway for specified device
        
        Arguments:
            capability_alternate_id {str} -- Alternate ID for capability
            sensor_alternate_id {str} -- Alternate ID for sensor
            measures {list} -- List of key-value pairs with the keys and respective values of the desired measures
            sensor_type_alternate_id {int} -- (Optional) If this parameter is set, the device will be auto-onboarded if it does not exist yet. Note: The alternate id of the sensor type must be numeric.
            use_timestamp {bool} -- If this is set to false, no timestamp will be sent.
            timestamp {int} -- UNIX time in milliseconds. If None, current time will be used.
            device_alternate_id {str} -- Alternate ID of the device. If none, the device from the client id will be used.
        Returns:
            Response -- Response object
        """
        if device_alternate_id is None:
            device_alternate_id = self.device_alternate_id

        service = '/measures/' + device_alternate_id
        headers = {'Content-Type': 'application/json'}
        payload = {
            "capabilityAlternateId": capability_alternate_id,
            "sensorAlternateId": sensor_alternate_id,
            "measures": measures
        }

        if sensor_type_alternate_id is not None:
            payload['sensorTypeAlternateId'] = sensor_type_alternate_id

        if use_timestamp:
            payload['timestamp'] = current_milli_time()
            if timestamp is not None:
                payload['timestamp'] = timestamp

        payload_json = json.dumps(payload)
        response = self._request_gateway(service=service, headers=headers, payload=payload_json)
        return response

    def post_batched_measures(self, messages: list, device_alternate_id: str = None) -> Response:
        """Post batched measures over rest gateway
        
        Arguments:
            messages {list} -- List of dicts, each containing sensorAlternateId, capabilityAlternateId and an array of measures as key-value pairs. If the device should be onboarded automatically, the sensorTypeAlternateId must also be provided.
            device_alternate_id {str} -- Alternate ID of the device. If none, the device from the client id will be used.

        Returns:
            Response -- Response object
        """
        if device_alternate_id is None:
            device_alternate_id = self.device_alternate_id

        service = '/measures/' + device_alternate_id
        headers = {'Content-Type': 'application/json'}
        payload_json = json.dumps(messages)
        response = self._request_gateway(service=service, headers=headers, payload=payload_json)
        return response


class RESTGatewayAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        pemfile = kwargs.pop('pemfile', None)
        secret = kwargs.pop('secret', None)
        if pemfile is None or secret is None:
            raise ValueError('Either "pemfile" or "secret" is missing')
        self.ssl_context = self._create_ssl_context(pemfile, secret)
        super(RESTGatewayAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.ssl_context:
            kwargs['ssl_context'] = self.ssl_context
        return super(RESTGatewayAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        if self.ssl_context:
            kwargs['ssl_context'] = self.ssl_context
        return super(RESTGatewayAdapter, self).proxy_manager_for(*args, **kwargs)

    def _create_ssl_context(self, pemfile, secret):
        if ssl is None:
            raise ValueError('This platform has no SSL/TLS.')
        if not hasattr(ssl, 'SSLContext'):
            # Require Python version that has SSL context support in standard library
            raise ValueError('Python 2.7.9 and 3.2 are the minimum supported versions for TLS.')
        # Create SSLContext object
        tls_version = ssl.PROTOCOL_TLSv1
        # If the python version supports it, use highest TLS version automatically
        if hasattr(ssl, "PROTOCOL_TLS"):
            tls_version = ssl.PROTOCOL_TLS
        context = ssl.SSLContext(tls_version)

        # Configure context
        if pemfile is not None:
            context.load_cert_chain(pemfile, password=secret)

        return context
