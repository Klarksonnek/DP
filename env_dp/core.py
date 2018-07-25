import hashlib
import http.client
import json
import logging
import os
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


class BeeeOnClient:
    """Client for communication with server supporting BeeeOn api."""

    def __init__(self, host, port, cache=True, cache_folder='cache'):
        self.__host = host
        self.__port = port
        self.__api_key = ""
        self.__token_id = ""
        self.__cache_folder = cache_folder
        self.__cache = cache
        self.__log = logging.getLogger(self.__class__.__name__)

        if cache:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)

    def refresh_token(self):
        data = {'key': self.__api_key, 'provider': 'apikey'}
        try:
            req = HTTPClient(self.__host, self.__port, "/auth", "POST", False)
            req.body(json.dumps(data))
            res, body = req.perform()
        except Exception as e:
            self.__log.error(e)
            return

        json_res = json.loads(body)

        if 'code' not in json_res:
            raise LookupError('return code not found')

        if int(json_res['code']) != 200:
            self.__log.warning("invalid token_id")
            exit(1)
            return

        return json_res['data']['id']

    def sensors_info(self, gateway_id, device_id):
        if not self.__token_id:
            self.__token_id = self.refresh_token()

        endpoint = '/gateways/' + str(gateway_id) + '/devices/' + str(
            device_id) + '/sensors'

        h = hashlib.sha256()
        h.update(endpoint.encode("utf8"))
        filename = self.__cache_folder + '/cache_sensor_info_' + h.hexdigest()

        if os.path.isfile(filename) and self.__cache:
            self.__log.debug('from cache: sensor_info, %s, %s' % (gateway_id, device_id))
            with open(filename) as f:
                for line in f:
                    return json.loads(line.strip())

        req = HTTPClient(self.__host, self.__port, endpoint, "GET", False)
        req.authorize(self.__token_id)

        res, body = req.perform()

        if self.__cache:
            file = open(filename, 'w')
            file.write(json.dumps(json.loads(body)['data']))
            file.close()

        return json.loads(body)['data']

    def history(self, gateway, device, sensor, start, end, interval=1, aggregation='avg'):
        if not self.__token_id:
            self.__token_id = self.refresh_token()

        endpoint = '/gateways/' + gateway
        endpoint += '/devices/' + device
        endpoint += '/sensors/' + str(sensor)
        endpoint += '/history'
        endpoint += '?range=' + str(start) + ',' + str(end)
        endpoint += '&interval=' + str(interval)
        endpoint += '&aggregation=' + aggregation

        h = hashlib.sha256()
        h.update(endpoint.encode("utf8"))
        filename = self.__cache_folder + '/cache_history_' + h.hexdigest()

        if os.path.isfile(filename) and self.__cache:
            self.__log.debug('from cache: history, %s, %s, %s, %s - %s' % (
                gateway, device, sensor, start, end))
            with open(filename) as f:
                for line in f:
                    return json.loads(line.strip())

        req = HTTPClient(self.__host, self.__port, endpoint, "GET", False)
        req.authorize(self.__token_id)

        res, body = req.perform()

        if self.__cache:
            file = open(filename, 'w')
            file.write(body)
            file.close()

        return json.loads(body)

    def logout(self):
        if not self.__token_id:
            return

        endpoint = '/auth'

        req = HTTPClient(self.__host, self.__port, endpoint, "DELETE", False)
        req.authorize(self.__token_id)

        req.perform()

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, key):
        self.__api_key = key


def main():
    pass
