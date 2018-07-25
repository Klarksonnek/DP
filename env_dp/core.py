import datetime
import hashlib
import http.client
import json
import logging
import os
import requests
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


class WeatherData:
    """Weather data extraction from weather.com."""

    def __init__(self, precision=1, cache=True, cache_folder='cache'):
        self.__precision = precision
        self.__cache = cache
        self.__cache_folder = cache_folder
        self.__log = logging.getLogger(self.__class__.__name__)

        if cache:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)

    def __download_data(self, start, end):
        day_time_start = datetime.datetime.fromtimestamp(start).strftime('%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = datetime.datetime.fromtimestamp(end).strftime('%Y%m%d %H:%M:%S')
        day_end = day_time_end[:-9]

        url = 'https://api.weather.com/v1/geocode/49.15139008/16.69388962/observations/'
        url += 'historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e'
        url += '&startDate=' + str(day_start) + '&endDate=' + str(day_end)

        h = hashlib.sha256()
        h.update(url.encode("utf8"))
        filename = self.__cache_folder + '/cache_weather_' + h.hexdigest()

        if os.path.isfile(filename) and self.__cache:
            self.__log.debug('from cache: %s - %s' % (start, end))
            with open(filename) as f:
                for line in f:
                    return line.strip()

        json_data = requests.get(url).text

        if self.__cache:
            file = open(filename, 'w')
            file.write(json_data)
            file.close()

        return json_data

    def weather_data(self, start, end):
        json_data = self.__download_data(start, end)

        python_obj = json.loads(json_data)

        out_general = []
        for element in python_obj['observations']:
            out_general.append({
                'at': element['valid_time_gmt'],
                'temperature': element['temp'],
                'relative_humidity': element['rh'],
                'pressure': element['pressure'],
                'wind_speed': element['wspd']
            })

        generate_weather_data = self.__generate_weather_data(out_general)
        out_detailed = []

        for i in range(0, len(generate_weather_data)):
            weather = generate_weather_data[i]
            if weather['at'] < start or generate_weather_data[i]['at'] > end:
                continue

            out_detailed.append(generate_weather_data[i])

        return out_detailed

    def __generate_weather_data(self, out_general):
        out_detailed = []
        for i in range(0, len(out_general) - 1):
            temp_start = out_general[i]['temperature']
            temp_end = out_general[i + 1]['temperature']
            if temp_start - temp_end == 0:
                temp_increase = 0
            else:
                temp_diff = temp_end - temp_start
                temp_increase = temp_diff / 1800.0

            rh_start = out_general[i]['relative_humidity']
            rh_end = out_general[i + 1]['relative_humidity']
            if rh_start - rh_end == 0:
                rh_increase = 0
            else:
                rh_diff = rh_end - rh_start
                rh_increase = rh_diff / 1800.0

            pressure_start = out_general[i]['pressure']
            pressure_end = out_general[i + 1]['pressure']
            if pressure_start - pressure_end == 0:
                pressure_increase = 0
            else:
                pressure_diff = pressure_end - pressure_start
                pressure_increase = pressure_diff / 1800.0

            wspd_start = out_general[i]['wind_speed']
            wspd_end = out_general[i + 1]['wind_speed']
            if wspd_start - wspd_end == 0:
                wspd_increase = 0
            else:
                wspd_diff = wspd_end - wspd_start
                wspd_increase = wspd_diff / 1800.0

            temp = temp_start
            rh = rh_start
            pressure = pressure_start
            wind_speed = wspd_start
            for j in range(0, 1800):
                out_detailed.append({
                    'at': int(out_general[i]['at']) + j,
                    'temperature': round(float(temp), self.__precision),
                    'relative_humidity': round(float(rh), self.__precision),
                    'pressure': round(float(pressure), self.__precision),
                    'wind_speed': round(float(wind_speed), self.__precision),
                })
                temp = temp + temp_increase
                rh = rh + rh_increase
                pressure = pressure + pressure_increase
                wind_speed = wind_speed + wspd_increase

        return out_detailed


def api_key(filename='api_key.config'):
    with open(filename) as file:
        for line in file:
            return line.strip()

    raise EnvironmentError('api key not found')


def main():
    pass
