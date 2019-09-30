""" Author: Philipp Steinrötter (steinroe) """


class Response(object):
    """Objects contain information received from API"""

    def __init__(self, status_code, response, headers):
        self._status_code = status_code
        self._result = response
        self._headers = headers

    def get_result(self) -> str:
        """Returns the result of the response, e.g. the body of the message

        Returns:
            str -- The body of the response message. Mostly in JSON formatting.
        """
        return self._result

    def get_headers(self) -> str:
        """Returns the header of the response

        Returns:
            str -- The header of the response message.
        """
        return self._headers

    def get_status_code(self) -> int:
        """Status code of the response

        Returns:
            str -- The status code of the HTTP communication
        """
        return self._status_code
