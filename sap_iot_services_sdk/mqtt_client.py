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
        messageInfos = json.loads(message.payload.decode("utf-8"))
        report = []
        for msgInfo in messageInfos:
            if msgInfo.get('code') != 200 and msgInfo.get('code') != 202:
                error = {}
                error['message'] = self._message_buffer[msgInfo['id']]
                error['error'] = ' '.join(msgInfo['messages'])
                report.append(error)
            del self._message_buffer[msgInfo['id']]

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

    def publish(self, capability_alternate_id: str, sensor_alternate_id: str, measures: list, device_alternate_id: str = None, timestamp: int = None) -> mqtt.MQTTMessageInfo:
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
        measureMessageId = str(uuid.uuid4())
        payload = {
            "timestamp": current_milli_time(),
            "capabilityAlternateId": capability_alternate_id,
            "sensorAlternateId": sensor_alternate_id,
            "measureMessageId": measureMessageId,
            "measures": measures
        }

        if timestamp is not None:
            payload['timestamp'] = timestamp            

        self._message_buffer[measureMessageId] = payload
        payload_json = json.dumps(payload)
        return super(MQTTClient, self).publish(service, payload=payload_json)

    def simulate(self, device_alternate_id: str, capability_alternate_id: str, sensor_alternate_id: str, measures: list, interval=1, runtime=60):
        """Simulate measures for device
        
        Arguments:
            device_alternate_id {str} --  Alternate ID of the device you want to simulate data for
            capability_alternate_id {str} -- Alternate ID of the capability you want to simulate data for
            sensor_alternate_id {str} -- Alternate ID of the sensor you want to simulate data for
            measures {list} -- List of dicts with one dict for each measure. You need to provide the field 'key' with the respective key of the measure you want to simulate. In 'dataType' you need to provide the respective data type. The function supports 'string', 'double', 'integer', 'boolean', and 'binary'. For data types 'double' and 'integer' you need to provide 'min' and 'max'. For data types 'string' and 'binary' you need to provide a list of allowed strings in 'allowedStrings', from which is randomly chosen. 
        
        Keyword Arguments:
            interval {int} -- The interval in seconds in which the data should be send (default: {1})
            runtime {int} -- Defines how long the simulation should be run in seconds (default: {60})
        """
        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < runtime:
            try:
                simulated_measures = []
                for measure in measures:
                    simulated_measure = {}
                    value = None
                    if (measure['dataType'] == 'string'):
                        value = measure['allowedStrings'][random.randint(0, len(measure['allowedStrings']))]
                    elif (measure['dataType'] == 'double' or measure['dataType'] == 'float' or measure['dataType'] == 'long'):
                        value = random.uniform(measure['min'], measure['max'])
                    elif (measure['dataType'] == 'integer'):
                        value = random.randint(measure['min'], measure['max'])
                    elif (measure['dataType'] == 'boolean'):
                        value = bool(random.getrandbits(1))
                    elif (measure['dataType'] == 'binary'):
                        value = base64.b64encode(measure['allowedStrings'][random.randint(0, len(measure['allowedStrings']))])
                    simulated_measure[measure['key']] = value
                    simulated_measures.append(simulated_measure)
                self.publish(device_alternate_id, capability_alternate_id, sensor_alternate_id, simulated_measures)
                time.sleep(interval)
            except IOError:
                print("Error while sending measures to SAP IoT Service.")