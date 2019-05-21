"""

"""
from dm.HTTPClient import HTTPClient
import json
import logging

__author__ = ''
__email__ = ''


class BeeeOnClient:
    """Client for communication with server supporting BeeeOn api."""

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__api_key = ""
        self.__token_id = ""
        self.__log = logging.getLogger(self.__class__.__name__)

    def refresh_token(self):
        logging.debug('obtaining token id')
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

        req = HTTPClient(self.__host, self.__port, endpoint, "GET", False)
        req.authorize(self.__token_id)

        res, body = req.perform()

        return json.loads(body)

    def sensors_info(self, gateway_id, device_id):
        if not self.__token_id:
            self.__token_id = self.refresh_token()

        endpoint = '/gateways/' + str(gateway_id) + '/devices/' + str(
            device_id) + '/sensors'

        req = HTTPClient(self.__host, self.__port, endpoint, "GET", False)
        req.authorize(self.__token_id)
        res, body = req.perform()

        return json.loads(body)['data']

    def __logout(self):
        if not self.__token_id:
            self.__log.warning('token is not set')
            return

        endpoint = '/auth'

        req = HTTPClient(self.__host, self.__port, endpoint, "DELETE", False)
        req.authorize(self.__token_id)

        req.perform()

        self.__log.debug('logout was successful')

    def __del__(self):
        try:
            self.__logout()
        except:
            logging.error('problem with logout')

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, key):
        self.__api_key = key

    @property
    def token_id(self):
        if not self.__token_id:
            self.__token_id = self.refresh_token()

        return self.__token_id

    @token_id.setter
    def token_id(self, token):
        if self.__token_id:
            logging.warning('token is set')
        else:
            self.__token_id = token
