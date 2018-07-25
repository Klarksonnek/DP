import http.client
import ssl


class HTTPClient:
    """Simple http client."""

    def __init__(self, host, port, end_point, method, verify_ssl_cert=True):
        self.__host = host
        self.__port = port
        self.__method = method
        self.__end_point = end_point
        self.__headers = {}
        self.__body = None
        self.__verify_ssl_cert = verify_ssl_cert

    def __setitem__(self, key, value):
        self.__headers[key] = value

    def __getitem__(self, key):
        return self.__headers[key]

    def __delitem__(self, key):
        del self.__headers[key]

    def body(self, body):
        self.__body = body

    def authorize(self, session_id):
        self.__headers['Authorization'] = 'Bearer ' + session_id

    def perform(self):
        if self.__verify_ssl_cert:
            conn = http.client.HTTPSConnection(self.__host, self.__port, timeout=10)
        else:
            conn = http.client.HTTPSConnection(self.__host, self.__port,
                                               context=ssl._create_unverified_context(),
                                               timeout=10)

        conn.request(self.__method, self.__end_point,
                     headers=self.__headers, body=self.__body)

        response = conn.getresponse()
        content = str(response.read(), 'utf-8')
        conn.close()
        return response, content


def main():
    pass
