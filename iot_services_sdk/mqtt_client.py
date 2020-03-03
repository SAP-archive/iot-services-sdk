""" Author: Philipp Steinrötter (steinroe) """

import ssl
import json
import uuid
import time
from datetime import datetime
import random
import base64
import paho.mqtt.client as mqtt

from .utils import current_milli_time


class PahoMQTT(mqtt.Client):
    """Overwrites the mqtt.Client class to work with password protected pem files
    """

    def tls_set(self, ca_certs=None, pemfile=None, secret=None, tls_version=None):
        """Configure network encryption and authentication options. Enables SSL/TLS support.
        ca_certs : a string path to the Certificate Authority certificate files
        that are to be treated as trusted by this client. If this is the only
        option given then the client will operate in a similar manner to a web
        browser. That is to say it will require the broker to have a
        certificate signed by the Certificate Authorities in ca_certs and will
        communicate using TLS v1, but will not attempt any form of
        authentication. This provides basic network encryption but may not be
        sufficient depending on how the broker is configured.
        By default, on Python 2.7.9+ or 3.4+, the default certification
        authority of the system is used. On older Python version this parameter
        is mandatory.
        pemfile is a string pointing to the PEM encoded client
        certificate. If the argument is not
        None it they will be used as client information for TLS based
        authentication.  Support for this feature is broker dependent. Note
        that if the file in encrypted and needs a password to
        decrypt it, you will have to provide the secret, too.
        tls_version allows the version of the SSL/TLS protocol used to be
        specified. By default TLS v1 is used. Previous versions (all versions
        beginning with SSL) are possible but not recommended due to possible
        security problems.
        Must be called before connect() or connect_async()."""
        if ssl is None:
            raise ValueError('This platform has no SSL/TLS.')

        if not hasattr(ssl, 'SSLContext'):
            # Require Python version that has SSL context support in standard library
            raise ValueError('Python 2.7.9 and 3.2 are the minimum supported versions for TLS.')

        # Create SSLContext object
        if tls_version is None:
            tls_version = ssl.PROTOCOL_TLSv1
            # If the python version supports it, use highest TLS version automatically
            if hasattr(ssl, "PROTOCOL_TLS"):
                tls_version = ssl.PROTOCOL_TLS
        context = ssl.SSLContext(tls_version)

        # Configure context
        if pemfile is not None:
            context.load_cert_chain(pemfile, password=secret)

        context.verify_mode = ssl.CERT_REQUIRED

        context.load_default_certs()

        self.tls_set_context(context)

        self.tls_insecure_set(False)


class MQTTClient(PahoMQTT):
    """Wrapper around the Paho MQTT Client to simplify its usage with the IoTS Cloud Gateway
    """

    def __init__(self, instance: str, device_alternate_id: str, pemfile: str, secret: str):
        """Instantiate MQTT Client configured for specified instance and device
        
        Arguments:
            instance {str} -- IoT Services instance
            device_alternate_id {str} -- The alternate id of the mqtt (router) device
            certfile_path {str} -- The certfile path for the mqtt (router) device
            keyfile_path {str} -- The keyfile path for the mqtt (router) device
        """
        super(MQTTClient, self).__init__(client_id=device_alternate_id)

        self.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, pemfile=pemfile, secret=secret)

        self.host = instance
        self.port = 8883
        self.device_alternate_id = device_alternate_id

        self._on_error = None
        self._on_command = None
        self._message_buffer = {}
        self._command_callbacks = {}

    @property
    def on_error(self):
        """If implemented, called when the client has error.
        Defined to allow error handling."""
        return self._on_error

    @on_error.setter
    def on_error(self, func):
        with self._callback_mutex:
            self._on_error = func

    @property
    def on_command(self):
        """If implemented, called when the client has received a command message.
        Defined to allow command handling."""
        return self._on_command

    @on_command.setter
    def on_command(self, func):
        with self._callback_mutex:
            self._on_command = func

    def connect(self, keepalive=60):
        """Connects to the broker
        
        Keyword Arguments:
            keepalive {int} -- The number of seconds the connection should be kept alive (default: {60})
        """
        super(MQTTClient, self).connect(host=self.host, port=self.port, keepalive=keepalive)
        self._subscribe_ack()

    def _subscribe_ack(self):
        service = 'ack/' + self.device_alternate_id
        self.message_callback_add(service, self._ack_message_handler)
        return super(MQTTClient, self).subscribe(service, 1)

    def _ack_message_handler(self, client, userdata, message):
        message_infos = json.loads(message.payload.decode("utf-8"))
        report = []
        for msg_info in message_infos:
            if msg_info.get('code') != 200 and msg_info.get('code') != 202:
                error = {
                    'message': self._message_buffer.get(msg_info.get('id')),
                    'error': ' '.join(msg_info.get('messages'))
                }
                report.append(error)
            if msg_info.get('id') in self._message_buffer:
                del self._message_buffer[msg_info.get('id')]

        if len(report) > 0:
            self.on_error(self, userdata, report)

    def subscribe(self, device_alternate_id: str) -> (str, str):
        """Subscribe to a devices commands
        
        Arguments:
            device_alternate_id {str} -- The alternate id of the device
        
        Returns:
            str -- Result of the subscription
            str -- Message ID
        """
        service = 'commands/' + device_alternate_id
        self.message_callback_add(service, self._command_message_handler)
        return super(MQTTClient, self).subscribe(service, 1)

    def _command_message_handler(self, client, userdata, message):
        parsed_message = json.loads(message.payload.decode("utf-8"))
        self.on_command(self, userdata, parsed_message)

    def publish(self, capability_alternate_id: str, sensor_alternate_id: str, measures: list,
                device_alternate_id: str = None, timestamp: int = None) -> mqtt.MQTTMessageInfo:
        """Publishes measures to the IoT Services
        
        Arguments:
            device_alternate_id {str} -- Alternate ID of the device. If none, the device from the client id will be used.
            capability_alternate_id {str} -- Alternate ID of the capability
            sensor_alternate_id {str} -- Alternate ID of the sensor
            timestamp {int} -- UNIX time in milliseconds. If None, current time will be used.
            measures {list} -- List of key-value pairs containing the measures and their respective values 
        
        Returns:
            mqtt.MQTTMessageInfo -- MQTT Message Info
        """
        if device_alternate_id is None:
            device_alternate_id = self.device_alternate_id

        service = 'measures/' + device_alternate_id
        measure_message_id = str(uuid.uuid4())
        payload = {
            "timestamp": current_milli_time(),
            "capabilityAlternateId": capability_alternate_id,
            "sensorAlternateId": sensor_alternate_id,
            "measureMessageId": measure_message_id,
            "measures": measures
        }

        if timestamp is not None:
            payload['timestamp'] = timestamp

        self._message_buffer[measure_message_id] = payload
        payload_json = json.dumps(payload)
        return super(MQTTClient, self).publish(service, payload=payload_json)
