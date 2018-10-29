import copy
import csv
import datetime
import hashlib
import http.client
import json
import logging
import math
import os
import requests
import ssl
import time
import pytz
from socket import error as SocketError
import gzip
from scipy import stats


COLORS = ['red', 'green', 'blue', 'orange', 'purple', 'silver', 'black']


def local_time_str_to_utc(date_str, timezone='Europe/Prague', format='%Y/%m/%d %H:%M:%S'):
    # https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/

    datetime_obj_naive = datetime.datetime.strptime(date_str, format)
    datetime_obj_pacific = pytz.timezone(timezone).localize(datetime_obj_naive)

    return datetime_obj_pacific


def utc_timestamp_to_local_time(timestamp, timezone='Europe/Prague'):
    utc = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('UTC'))
    local_time = utc.astimezone(pytz.timezone(timezone))

    return local_time


def utc_timestamp_to_str(timestamp, format):
    local_time = utc_timestamp_to_local_time(timestamp, 'Europe/Prague')

    return local_time.strftime(format)


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

    def __init__(self, host, port, cache=True, cache_folder='../cache'):
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
        filename = self.__cache_folder + '/sensor_info_' + h.hexdigest()

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
        filename = self.__cache_folder + '/history_' + h.hexdigest()

        if os.path.isfile(filename) and self.__cache:
            self.__log.debug('from cache: history, %s, %s, %s, %s - %s (%s - %s)' % (
                gateway,
                device,
                sensor,
                start,
                end,
                utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S'),
                utc_timestamp_to_str(end, '%Y/%m/%d %H:%M:%S')
            ))

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


    def __logout(self):
        if not self.__token_id:
            self.__log.warning('empty token_id')
            return

        endpoint = '/auth'

        req = HTTPClient(self.__host, self.__port, endpoint, "DELETE", False)
        req.authorize(self.__token_id)

        req.perform()

        self.__log.debug('logout was successful')

    def __del__(self):
        self.__logout()

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, key):
        self.__api_key = key


class WeatherData:
    """Weather data extraction from weather.com."""

    def __init__(self, precision=1, cache=True, cache_folder='../cache'):
        self.__precision = precision
        self.__cache = cache
        self.__cache_folder = cache_folder
        self.__log = logging.getLogger(self.__class__.__name__)

        if cache:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)


    def __remove_from_cache(self, start, end):
        day_time_start = utc_timestamp_to_str(start, '%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = utc_timestamp_to_str(end, '%Y%m%d %H:%M:%S')
        day_end = day_time_end[:-9]

        url = 'https://api.weather.com/v1/geocode/49.15139008/16.69388962/observations/'
        url += 'historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e'
        url += '&startDate=' + str(day_start) + '&endDate=' + str(day_end)

        h = hashlib.sha256()
        h.update(url.encode("utf8"))
        filename = self.__cache_folder + '/weather_' + h.hexdigest()

        if os.path.exists(filename):
            os.remove(filename)

    def __download_data(self, start, end):
        day_time_start = utc_timestamp_to_str(start, '%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = utc_timestamp_to_str(end, '%Y%m%d %H:%M:%S')
        day_end = day_time_end[:-9]

        url = 'https://api.weather.com/v1/geocode/49.15139008/16.69388962/observations/'
        url += 'historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e'
        url += '&startDate=' + str(day_start) + '&endDate=' + str(day_end)

        h = hashlib.sha256()
        h.update(url.encode("utf8"))
        filename = self.__cache_folder + '/weather_' + h.hexdigest()

        if os.path.isfile(filename) and self.__cache:
            self.__log.debug('from cache: %s - %s (%s - %s)' % (
                start,
                end,
                utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S'),
                utc_timestamp_to_str(end, '%Y/%m/%d %H:%M:%S')
            ))

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
        max_attempts = 2
        for i in range(0, max_attempts):
            try:
                return self.__weather_data2(start, end)
            except KeyError:
                self.__log.debug('wait')
                self.__remove_from_cache(start, end)
                time.sleep(1)
            except ConnectionResetError as e:
                self.__log.debug('wait (%s)' % str(e))
                time.sleep(1)
            except SocketError as e:
                self.__log.debug('wait (%s)' % str(e))
                time.sleep(1)
            except IndexError as e:
                self.__log.debug('wait (%s)' % str(e))
                time.sleep(1)

        return []

    def __weather_data2(self, start, end):
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

        generate_weather_data = self.__generate_weather_data(out_general, start, end)
        out_detailed = []

        for i in range(0, len(generate_weather_data)):
            weather = generate_weather_data[i]
            if weather['at'] < start or generate_weather_data[i]['at'] > end:
                continue

            out_detailed.append(generate_weather_data[i])

        return out_detailed

    def __generate_weather_data(self, out_general, start, end):
        out_detailed = []

        # odstranenie null hodnot a casov, ktore nie su zarovnane na polhodinu
        out_not_null_value = []
        for item in out_general:
            failed = False

            # ak udaj obsahuje nejaku None hodnotu, vynechame ho
            for key, value in item.items():
                if value is None:
                    failed = True

            # ak udaj obsahuje nezarovnany cas na polhodinu, vynechame ho
            if item['at'] % 1800 != 0:
                failed = True

            if not failed:
                out_not_null_value.append(item)

        tmp = copy.deepcopy(out_not_null_value)
        out_general = []

        last_at = tmp[0]['at']
        for k in range(0, len(tmp)):
            i = copy.deepcopy(tmp[k])

            # ak je rovnaky cas ako predpokladany iba vlozime
            if last_at == i['at']:
                out_general.append(i)
                last_at += 1800
                continue

            while True:
                # ak je last_at mensi ako predpokladany, co znaci, ze chyba polozka
                # tak upravime cas na pozadovany a pridame
                # takto sa duplikuje aktualna polozka, meni sa len cas, hodnoty zostavaju
                if last_at <= tmp[k]['at']:
                    i['at'] = last_at
                    out_general.append(i)
                    last_at += 1800
                else:
                    break

        tmp = copy.deepcopy(out_general)
        out_general = []
        for row in tmp:
            if row['at'] < (start - (start % 1800)):
                continue
            if row['at'] > (end - (end % 1800) + 1800):
                continue

            out_general.append(row)

        # duplikujeme poslednu hodnotu, aby bolo mozne
        # generovat aj rozsah v poslednej polhodine dna
        out_general.append(out_general[-1])

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


class DataStorage:
    def __init__(self, client, weather_client, precision=1, cache=True,
                 cache_folder='../cache/gzip'):
        self.__client = client
        self.__meta_data = []
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__weather_client = weather_client
        self.__precision = precision
        self.__cache = cache
        self.__cache_folder = cache_folder
        self.__events_file = ''

        if cache:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)

    def __parser_date(self, date):
        return local_time_str_to_utc(date).timestamp()

    def __download_sensor_modules(self, gateway, device):
        data = self.__client.sensors_info(gateway, device)

        out = []
        for sensor in data:
            out.append({
                'id': int(sensor['id']),
                'type_id': sensor['type_id']
            })

        return out

    def __requested_modules(self, gateway, device, sensors):
        supported_modules = self.__download_sensor_modules(gateway, device)

        out = []
        for sensor in sensors:
            found = False
            for supported_module in supported_modules:
                if sensor['id'] == supported_module['id']:
                    supported_module['custom_name'] = sensor['custom_name']
                    out.append(supported_module)
                    found = True
                    break

            if not found:
                self.__log.warning("module %s not supported" % sensor)

        return out

    def read_meta_data(self, devices, events):
        self.__events_file = events

        with open(devices) as f:
            j_devices = json.load(f)

        with open(events) as f:
            j_events = json.load(f)

        for event in j_events['events']:
            new = copy.deepcopy(event)
            new['times']['event_start'] = int(
                self.__parser_date(event['times']['event_start']))

            if 'event_end' in new['times']:
                new['times']['event_end'] = int(
                    self.__parser_date(event['times']['event_end']))

            new['data'] = []
            del (new['devices'])

            types = ['event_start']

            for type_id in types:
                one_sensor = {
                    'type': type_id,
                    'weather': [],
                    'values': [],
                }

                for key, device in event['devices'].items():
                    for dev in j_devices['devices']:
                        if dev['id'] != key:
                            continue

                        sensors = self.__requested_modules(dev['gateway'], dev['device'],
                                                           dev['sensors'])

                        for event_device in device:
                            found = False
                            for sensor in sensors:
                                if event_device != sensor['custom_name']:
                                    continue

                                found = True
                                one_sensor['values'].append({
                                    'id': key,
                                    'measured': [],
                                    'module_id': sensor['id'],
                                    'custom_name': sensor['custom_name'],
                                    'type_id': sensor['type_id'],
                                    'gateway': dev['gateway'],
                                    'device': dev['device']
                                })
                                break

                            if not found:
                                self.__log.warning(
                                    'sensor %s not found in input files with devices'
                                    % event_device)

                new['data'].append(one_sensor)
            self.__meta_data.append(new)

    def __filter_not_null(self, data):

        out_data = []
        for row in data:
            if row['value'] is None:
                continue

            out_data.append(row)

        return out_data

    def __cut_normalization(self, start, end, data):
        for i in range(0, len(data['values'])):
            values = data['values'][i]
            out_json = []

            for row in values['measured']:
                if row['at'] < start or row['at'] > end:
                    continue


                out_json.append(row)

            values['measured'] = out_json

        return data

    def filter_downloaded_data(self, item, module1, key1, module2, key2, diff_min, diff_max):
        out = []

        for event in item:
            diff_item1 = None
            diff_item2 = None

            for event_type in event['data']:
                for module in event_type['values']:
                    if module['custom_name'] == module1:
                        diff_item1 = module['measured'][0]

                    if module['custom_name'] == module2:
                        diff_item2 = module['measured'][0]

            diff = abs(diff_item1[key1] - diff_item2[key2])
            if diff_min <= diff <= diff_max:
                out.append(event)

        return out

    def filter_downloaded_data_one_module(self, events, module1, key1, limit):
        out = []

        for event in events:
            for event_type in event['data']:
                for module in event_type['values']:
                    if module['custom_name'] == module1:
                        if module['measured'][0][key1] < limit:
                            out.append(event)

        return out

    def filter_downloaded_data_general_attribute(self, events, attribute, value):
        out = []

        for event in events:
            if event[attribute] == value:
                continue
            out.append(event)

        return out

    def filter_general_attribute_value(self, events, attribute, value):
        out = []

        for event in events:
            if attribute not in event:
                continue

            if event[attribute] != value:
                continue

            out.append(event)

        return out

    def filter_downloaded_data_existing_attribute(self, events, attribute):
        out = []

        for event in events:
            if attribute in event:
                out.append(copy.deepcopy(event))

        return out

    def filter_downloaded_data_two_conditions(self, events, module1, key1, limit, module2, key2, diff_min, diff_max):
        out = []

        for event in events:
            diff_item1 = None
            diff_item2 = None
            for event_type in event['data']:
                for module in event_type['values']:
                    if module['custom_name'] == module1 and module['measured'][0][key1] < limit:
                        out.append(event)
                        continue

                    if module['custom_name'] == module1:
                        diff_item1 = module['measured'][0]

                    if module['custom_name'] == module2:
                        diff_item2 = module['measured'][0]

            if diff_item1 is not None and diff_item2 is not None:
                diff = abs(diff_item1[key1] - diff_item2[key2])
                if diff_min <= diff <= diff_max:
                    out.append(event)

        return out


    def download_data_for_normalization(self, type_id):
        filename = self.__cache_folder + '/' + self.__events_file
        if self.__cache:
            for i in range(0, len(type_id)):
                filename += type_id[i]

                if i != len(type_id) - 1:
                    filename += '_'

            filename += '.gz'

            if os.path.isfile(filename):
                with gzip.GzipFile(filename, 'r') as fin:
                    json_bytes = fin.read()

                json_str = json_bytes.decode('utf-8')
                return json.loads(json_str)

        # 15 minutes
        time_shift = 900

        out_json = copy.deepcopy(self.__meta_data)

        for k in range(0, len(out_json)):
            event = out_json[k]

            for j in range(0, len(event['data'])):
                event_type = event['data'][j]

                s_time = event['times']['event_start']
                e_time = event['times']['event_end']

                if event_type['type'] == 'no_event_start':
                    s_time = event['times']['no_event_start']
                    e_time = event['times']['no_event_start'] + 1

                    if s_time > e_time:
                        s_time, e_time = e_time, s_time

                event_type['weather_dw'] = self.__weather_client.weather_data(s_time, e_time)

                tmp_modules = []
                for i in range(0, len(event_type['values'])):
                    module = event_type['values'][i]

                    if module['custom_name'] in type_id:
                        module['measured'] = self.__client.history(
                            module['gateway'],
                            module['device'],
                            module['module_id'],
                            int(utc_timestamp_to_local_time(s_time).timestamp() - time_shift),
                            int(utc_timestamp_to_local_time(e_time).timestamp() + time_shift)
                        )['data']

                        module['measured'] = self.__filter_not_null(module['measured'])

                        tmp_modules.append(module)

                event_type['values'] = tmp_modules
                event_type = self.__generate_event_data(
                    event_type,
                    int(utc_timestamp_to_local_time(s_time).timestamp()),
                    int(utc_timestamp_to_local_time(e_time).timestamp()))
                self.__cut_normalization(s_time, e_time, event_type)

        out = []
        for event in out_json:
            fail = False

            for event_type in event['data']:
                weather_len = len(event_type['weather_dw'])
                s_time = event['times']['event_start']
                e_time = event['times']['event_end']

                if event_type['type'] == 'no_event_start':
                    s_time = event['times']['no_event_start']
                    e_time = event['times']['no_event_start'] + 1

                    if s_time > e_time:
                        s_time, e_time = e_time, s_time

                for row in event_type['values']:
                    if len(row['measured']) != weather_len:
                        s = 'event '
                        s += utc_timestamp_to_str(s_time, '%Y/%m/%d %H:%M:%S')

                        s += ' - '
                        s += utc_timestamp_to_str(e_time, '%Y/%m/%d %H:%M:%S')

                        s += ' is ignored'
                        s += ' stiahnute data neobsahuju data za dany interval (chyba senzora)'

                        self.__log.warning(s)
                        fail = True
                        break

            if not fail:
                out.append(event)

        if self.__cache:
            with gzip.open(filename, 'wb') as f:
                json_bytes = json.dumps(out).encode('utf-8')
                f.write(json_bytes)

        return out


    def download_data(self, shift_before, shift_after):
        out_json = copy.deepcopy(self.__meta_data)

        for event in out_json:
            for event_type in event['data']:
                e_start_before_timestamp = utc_timestamp_to_local_time(
                    int(event['times'][event_type['type']])).timestamp() - shift_before

                e_start_after_timestamp = utc_timestamp_to_local_time(
                    int(event['times'][event_type['type']])).timestamp() + shift_after

                event_type['weather'] = self.__weather_client.weather_data(
                    e_start_before_timestamp, e_start_after_timestamp)

                for module in event_type['values']:
                    if module['type_id'] == 'open_close':
                        if 'no_event_start' in event_type['type']:
                            module['measured'].append({
                                'at': event['times']['no_event_start'],
                                'value': '1.0'
                            })
                            continue

                    module['measured'] = self.__client.history(
                        module['gateway'],
                        module['device'],
                        module['module_id'],
                        int(e_start_before_timestamp),
                        int(e_start_after_timestamp)
                    )['data']

        return out_json

    def __switch_value(self, value):
        if value == 1:
            return 0

        return 1

    def __generate_event_data(self, event, s_time=None, e_time=None):
        out = copy.deepcopy(event)
        out['values'] = []

        for item in event['values']:
            if s_time is not None and e_time is not None:
                # simple hack for no_event_start, each value is set to 0 by default
                if event['type'] == 'no_event_start' and item['type_id'] == 'open_close':
                    out_values = []

                    for i in range(0, e_time - s_time + 1):
                        out_values.append({
                            "at": s_time + i,
                            "value": 0
                        })

                    item['measured'] = out_values
                    out['values'].append(item)
                    continue

            if len(item['measured']) <= 1:
                if item['type_id'] == 'open_close':
                    out['values'].append(item)
                    continue

                if len(item['measured']) == 0:
                    self.__log.debug(
                        'prazdne hodnoty v modulu: %s, skip' % item['custom_name'])
                    out['values'].append(item)
                    continue

                if len(item['measured']) == 1 and item['type_id'] != 'open_close':
                    self.__log.debug(
                        'len jedna hodnota v modulu: %s, skip' % item['custom_name'])
                    out['values'].append(item)
                    continue

            out_values = []
            last_open_close_value = None
            if item['type_id'] == 'open_close':
                last_open_close_value = float(item['measured'][0]['value'])

            for i in range(0, len(item['measured']) - 1):
                value_start = item['measured'][i]['value']
                value_end = item['measured'][i + 1]['value']

                if value_start is None or value_end is None:
                    continue

                value_start = float(item['measured'][i]['value'])
                value_end = float(item['measured'][i + 1]['value'])

                time_start = item['measured'][i]['at']
                time_end = item['measured'][i + 1]['at']

                if item['type_id'] == 'open_close':
                    for j in range(0, time_end - time_start):
                        out_values.append({
                            "at": time_start + j,
                            "value": round(last_open_close_value, self.__precision)
                        })
                    continue

                if value_start - value_end == 0:
                    value_increase = 0
                else:
                    value_diff = value_end - value_start
                    value_increase = value_diff / (time_end - time_start)

                value = value_start
                for j in range(0, time_end - time_start):
                    out_values.append({
                        "at": time_start + j,
                        "value": round(value, self.__precision)
                    })
                    value = value + value_increase

            if item['type_id'] == 'open_close':
                out_values.append({
                    "at": item['measured'][len(item['measured']) - 1]['at'],
                    "value": 0.0
                })
            else:
                out_values.append({
                    "at": item['measured'][len(item['measured']) - 1]['at'],
                    "value": round(value, self.__precision)
                })

            item['measured'] = out_values
            out['values'].append(item)

        return out

    def __find_before_after_shift(self, events, event_type):
        shift_before = None
        shift_after = None

        for event in events:
            for data in event['data']:
                if data['type'] != event_type:
                    continue

                time = event['times'][event_type]
                for item in data['values']:
                    values_cnt = len(item['measured']) - 1
                    if len(item['measured']) <= 1 or item['type_id'] == "open_close":
                        continue

                    first = item['measured'][0]['at']
                    last = item['measured'][values_cnt]['at']
                    if shift_before is None:
                        shift_before = time - first
                    elif shift_before > time - first:
                        shift_before = time - first

                    if shift_after is None:
                        shift_after = last - time
                    elif last - time < shift_after:
                        shift_after = last - time

        return shift_before, shift_after

    def __cut_common_data(self, event, data, times):
        a, b = self.__find_before_after_shift(data, 'event_start')
        c, d = self.__find_before_after_shift(data, 'no_event_start')

        event = self.__generate_event_data(event)

        local_min = None
        local_max = None

        out = []
        for item in event['values']:
            measured_out = []

            if event['type'] == 'event_start':
                local_min = times['event_start'] - a
                local_max = times['event_start'] + b
            elif event['type'] == 'no_event_start':
                local_min = times['no_event_start'] - c
                local_max = times['no_event_start'] + d

            if item['type_id'] == "open_close":
                value = 0
                switch = True

                if event['type'] == 'no_event_start':
                    switch = False

                for timestamp in range(local_min, local_max + 1):
                    if timestamp >= item['measured'][0]['at'] and switch:
                        value = self.__switch_value(value)
                        switch = False

                    measured_out.append({
                        "at": timestamp,
                        "value": round(float(value), self.__precision)
                    })

                item['measured'] = measured_out
            else:
                measured_out = []
                for value in item['measured']:
                    if value['at'] < local_min or value['at'] > local_max:
                        continue

                    measured_out.append(value)

                item['measured'] = measured_out
            out.append(item)

        weather_out = []
        for item in event['weather']:
            if item['at'] < local_min or item['at'] > local_max:
                continue

            weather_out.append(item)

        event['values'] = out
        event['weather'] = weather_out

        return event

    def common_data(self, data):
        out = []
        for row in data:
            out_row = copy.deepcopy(row)
            out_row['data'] = []

            for event_type in row['data']:
                values = self.__cut_common_data(event_type, data, row['times'])
                out_row['data'].append(values)

            out.append(out_row)

        return out

    def __common_count(self, events, event_type):
        count_before = None
        count_after = None

        for event in events:
            for data in event['data']:
                if data['type'] != event_type:
                    continue

                local_before = 0
                local_after = 0
                for value in data['values'][0]['measured']:
                    if value['tag'] == 'before':
                        local_before += 1
                    elif value['tag'] == 'after':
                        local_after += 1
                    else:
                        print('skip')

                if count_before is None:
                    count_before = local_before
                else:
                    count_before = min(count_before, local_before)

                if count_after is None:
                    count_after = local_after
                else:
                    count_after = min(count_after, local_after)

        return count_before, count_after

    def set_no_event_time(self, no_event_start_time_shift):
        """
        Vytvorenie casovej znacky, kde sa event nevyskytoval. Znacka sa vytvori pre zaciatok a
        koniec eventu osobitne. Hodnoty pre zaciatok a koniec eventu sa vypocitaju posunom
        o zadanu hodnotu dopredu (kladna hodnota) alebo dozadu (zaporna hodnota). Dopredu je
        mysleny cas, ktory je vacsi ako aktualny.
        """

        for i in range(0, len(self.__meta_data)):
            event = self.__meta_data[i]

            new_value = event['times']['event_start'] + no_event_start_time_shift
            event['times']['no_event_start'] = new_value

            no_event_start = copy.deepcopy(event['data'][0])
            no_event_start['type'] = 'no_event_start'

            event['data'].append(no_event_start)

    @property
    def meta_data(self):
        return self.__meta_data


class Derivation:
    def __is_increasing(self, data):
        if data[0]['at'] < data[1]['at']:
            return True
        return False

    def __compute_before(self, data, difference_interval):
        next_difference = float(data[0]['at'])
        interval = 0
        str_out = ""
        last_value = float(data[0]['value'])
        out = []

        for item in data:
            last_timestamp = float(item['at']) - 1
            new_value = (last_value + float(item['value'])) / 2.0

            if (next_difference - float(item['at'])) >= 0:
                new_difference = float(data[0]['value']) - new_value
                str_out += str(round(interval, 2)).rjust(3, ' ')
                str_out += " s, "
                str_out += "prumer v casech: "
                str_out += utc_timestamp_to_str(float(item['at']), '%H:%M:%S') + " "
                str_out += " - "
                str_out += utc_timestamp_to_str(last_timestamp, '%H:%M:%S') + " "
                str_out += str(round(float(item['value']), 2)).rjust(6, ' ')
                str_out += " - "
                str_out += str(round(last_value, 2)).rjust(6, ' ') + " "
                str_out += "nova hodnota: "
                str_out += str(round(new_value, 2)).rjust(6, ' ') + " "
                str_out += "derivace: "
                str_out += str(round(new_difference, 2)).rjust(6, ' ') + " "
                last_value = float(item['value'])

                if new_difference == 0:
                    str_out += "-"
                elif new_difference > 0:
                    str_out += '\u2197'
                else:
                    str_out += '\u2198'
                str_out += "\n"

                next_difference -= difference_interval
                interval += difference_interval
                out.append(new_difference)
        return out

    def __compute_after(self, data, difference_interval):
        next_difference = float(data[0]['at'])
        interval = 0
        str_out = ""
        last_value = float(data[0]['value'])
        out = []

        for item in data:
            last_timestamp = float(item['at']) + 1
            new_value = (last_value + float(item['value'])) / 2.0

            if (next_difference - float(item['at'])) <= 0:
                new_difference = new_value - float(data[0]['value'])
                str_out += str(round(interval, 2)).rjust(3, ' ')
                str_out += " s, "
                str_out += "prumer v casech: "
                str_out += utc_timestamp_to_str(float(item['at']), '%H:%M:%S') + " "
                str_out += " - "
                str_out += utc_timestamp_to_str(last_timestamp, '%H:%M:%S') + " "
                str_out += str(round(last_value, 2)).rjust(6, ' ')
                str_out += " - "
                str_out += str(round(float(item['value']), 2)).rjust(6, ' ') + " "
                str_out += "prumer: "
                str_out += str(round(new_value, 2)).rjust(6, ' ') + " "
                str_out += "derivace: "
                str_out += str(round(new_difference, 2)).rjust(6, ' ') + " "
                last_value = float(item['value'])

                if new_difference == 0:
                    str_out += "-"
                elif new_difference > 0:
                    str_out += '\u2197'
                else:
                    str_out += '\u2198'
                str_out += "\n"

                next_difference += difference_interval
                interval += difference_interval
                out.append(new_difference)
        return out

    def compute(self, data, difference_interval):
        if self.__is_increasing(data[:2]):
            return self.__compute_after(data, difference_interval)

        return self.__compute_before(data, difference_interval)


class Graph:
    def __init__(self, path):
        self.__path = path
        self.__log = logging.getLogger(self.__class__.__name__)

    def gen(self, data, output, scale_padding_min=0, scale_padding_max=0,
            g_type='line', min_value=None, max_value=None, global_range=False):
        f = open(output, 'w')

        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('	<head>\n')
        f.write('		<link href="' + self.__path + '/chart.css" rel="stylesheet">\n')
        f.write('		<script src="' + self.__path + '/jquery-3.2.1.slim.min.js"></script>\n')
        f.write('		<script src="' + self.__path + '/Chart.bundle.js"></script>\n')
        f.write('		<script src="' + self.__path + '/utils.js"></script>\n')
        f.write('	</head>\n')
        f.write('	<body>\n')

        if (max_value is not None or min_value is not None) and global_range:
            raise ValueError('Moze byt bud pouzity parameter global_range alebo min+max')

        global_min = {}
        global_max = {}

        if global_range:
            for i in range(0, len(data)):
                row = data[i]

                for g in row['graphs']:
                    numbers = g['values']

                    if row['group'] not in global_min:
                        global_min[row['group']] = min(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_min[row['group']])
                        global_min[row['group']] = min(tmp)

                    if row['group'] not in global_max:
                        global_max[row['group']] = max(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_max[row['group']])
                        global_max[row['group']] = max(tmp)

        id = 0
        for i in range(0, len(data)):
            row = data[i]
            id += 1
            canvas_id = 'g' + str(id)

            f.write('		<div style="overflow: auto;float:left">\n')
            f.write('			<canvas class="custom" id="g' + str(canvas_id))
            f.write('" width="900px" height="500" style="float:left"></canvas>\n')

            if 'stat' in row:
                f.write('		<div width="900px" height="500" style="padding: 50px; float: left">\n')

                for key, value in row['stat']:
                    sep = ':'
                    if not key and not value:
                        sep = '&nbsp;'

                    f.write("<div>%s %s %s</div>" % (key, sep, value))
                f.write('		</div>\n')

            f.write('		</div>\n')

            all_min = None
            all_max = None

            if min_value is not None and max_value is not None:
                all_min = min_value
                all_max = max_value
            elif not global_range:
                for g in row['graphs']:
                    numbers = g['values']

                    if not numbers:
                        self.__log.warning('graph \'%s\' with label \'%s\' does not any value' %
                                         (data[i]['title'], g['label_x']))

                    if all_min is None:
                        all_min = min(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(all_min)
                        all_min = min(tmp)

                    if all_max is None:
                        all_max = max(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(all_max)
                        all_max = max(tmp)

            if global_range:
                all_min = global_min[row['group']]
                all_max = global_max[row['group']]

            all_min -= scale_padding_min
            all_max += scale_padding_max

            str_dataset = ""
            g_id = 0
            for g in row['graphs']:
                str_dataset += '						{\n'
                str_dataset += '							label: "' + g['label_x'] + '",\n'
                str_dataset += '							borderColor: "' + g['color'] + '",\n'
                str_dataset += '							backgroundColor: "' + g['color'] + '",\n'
                str_dataset += '							fill: false,\n'
                str_dataset += '							data: ' + str(g['values']) + ',\n'
                str_dataset += '							yAxisID: "y-axis-' + str(g_id) + '"\n'
                str_dataset += '						},\n'

            str_options = ""
            str_options += '							{\n'
            str_options += '								type: "linear",\n'
            str_options += '								display: true,\n'
            str_options += '								position: "left",\n'
            if g_type == 'bar':
                str_options += '								stacked: true,\n'
            else:
                str_options += '								stacked: false,\n'
            str_options += '								id: "y-axis-' + str(g_id) + '",\n'
            str_options += '								ticks: {\n'
            str_options += '									min: ' + str(all_min) + ',\n'
            str_options += '									max: ' + str(all_max) + '\n'
            str_options += '								}\n'
            str_options += '							},\n'

            f.write('		<script>\n')
            f.write('			var ctx = document.getElementById("g' + str(canvas_id) + '");\n')
            f.write('			var myChart1 = new Chart(ctx, {\n')
            f.write('				type: "' + g_type + '",\n')
            f.write('				data: {\n')
            f.write('					labels: ' + str(row['graphs'][0]['timestamps']) + ',\n')
            f.write('					datasets: [\n')
            f.write(str_dataset)
            f.write('					]\n')
            f.write('				},\n')
            f.write('				options: {\n')
            f.write('					responsive: false,\n')
            f.write('					hoverMode: "index",\n')

            if g_type == 'bar':
                f.write('					stacked: true,\n')
            else:
                f.write('					stacked: false,\n')

            f.write('					title: {\n')
            f.write('						display: true,\n')
            f.write('						text: "' + row['title'] + '"\n')
            f.write('					},\n')

            if g_type == 'bar':
                f.write('					tooltips: {\n')
                f.write('						mode: \'index\',\n')
                f.write('						intersect: false\n')
                f.write('					},\n')

            f.write('					scales: {\n')

            f.write('						yAxes: [\n')
            f.write(str_options)
            f.write('						],\n')
            f.write('						xAxes: [{\n')
            f.write('							stacked: true\n')
            f.write('						}],\n')

            f.write('					}\n')
            f.write('				}\n')
            f.write('			});\n')
            f.write('		</script>\n')

        f.write('	</body>\n')
        f.write('</html>\n')
        f.close()


def api_key(filename='api_key.config'):
    with open(filename) as file:
        for line in file:
            return line.strip()

    raise EnvironmentError('api key not found')


def to_weka_file(data, filename='weka.arff', class_name='open_close'):
    file = open(filename, 'w')
    file.write('@relation events\n\n')

    # write headers
    for item in data:
        if item['title'] == class_name:
            file.write('@attribute class {yes, no}\n')
            continue

        file.write('@attribute %s numeric\n' % item['title'])

    file.write('\n')

    # write data
    file.write('@data\n\n')
    for i in range(0, len(data[0]['data'])):
        for j in range(0, len(data)):
            val = data[j]['data'][i]

            if data[j]['title'] == class_name:
                if val == 1:
                    val = 'yes'
                else:
                    val = 'no'

            file.write('%s, ' % val)
        file.write('\n')

    file.close()


def gen_simple_graph(measured, color='blue', label='x value', key='value',
                     output_records=None):
    x = []
    y = []
    length = len(measured)

    step = 1
    if output_records is not None:
        step = length // output_records

        # ak je step nula, znamena to, ze nie je dostatok udajov, vykreslime
        # vsetky dostupne data so step jedna
        if step == 0:
            step = 1

        if step > 1:
            step += 1

    for i in range(0, length):
        value = measured[i]

        if i % step != 0:
            continue

        if key not in value:
            break

        x.append(utc_timestamp_to_str(value['at'], '%H:%M:%S'))
        y.append(value[key])

    return {
        'timestamps': x,
        'values': y,
        'label_x': label,
        'color': color,
    }


def normalization(data, local_min, local_max, key):
    for i in range(0, len(data)):
        if local_max - local_min == 0 and local_min == 0:
            data[i][key + "_norm"] = 0
            continue

        if local_max - local_min == 0:
            data[i][key + "_norm"] = 0.5
            continue

        data[i][key + "_norm"] = (data[i][key] - local_min) / (local_max - local_min)

    return data


def compute_norm_values(measured):
    measured = list(measured)

    keys = []
    for key, item in measured[0].items():
        if key == 'at':
            continue

        keys.append(key)

    for key in keys:
        only_measured = []
        for i in range(0, len(measured)):
            row = measured[i]

            only_measured.append(row[key])

        l_min = min(only_measured)
        l_max = max(only_measured)

        measured = normalization(measured, l_min, l_max, key)

    return measured


def weather_for_histogram(weather):
    out = copy.deepcopy(weather)

    p = 0
    t = 0
    ws = 0
    rh = 0
    for row in out:
        p += row['pressure']
        t += row['temperature']
        ws += row['wind_speed']
        rh += row['relative_humidity']

    p = p/len(out)
    t = t/len(out)
    ws = ws/len(out)
    rh = rh/len(out)

    for i in range(0, len(out)):
        row = out[i]

        row['pressure'] = p
        row['temperature'] = t
        row['wind_speed'] = ws
        row['relative_humidity'] = rh

    return out


def histogram_data(data, time_step, time_limit):
    histogram = []

    for row in data:
        values = row['data'][0]['values'][0]['measured']
        id = 0

        w = weather_for_histogram(row['data'][0]['weather_dw'])

        for j in range(0, len(values)):
            if j % time_step != 0:
                continue

            if j > time_limit:
                break

            if len(histogram) <= id:
                histogram.append({
                    'start_time': j,
                    'time_step': time_step,
                    'values': []
                })

            val = values[j]

            if 'wind' in row:
                val['wind'] = row['wind']
            else:
                val['wind'] = row['weather']

            val['weather_dw'] = w[j]

            histogram[id]['values'].append(val)

            id += 1

    return histogram


def gen_histogram(data, time_step, interval_start, interval_end, step, key, time_limit=1000):
    his_data = histogram_data(data, time_step, time_limit)

    for j in range(0, len(his_data)):
        his = his_data[j]

        histogram = []

        k = interval_start
        while True:
            if k > interval_end - step:
                break

            histogram.append({
                'start_interval': round(k, 5),
                'step': step,
                'histogram': []
            })

            k = k + step

        his['histogram'] = histogram

    for j in range(0, len(his_data)):
        values = his_data[j]

        for k in range(0, len(values['values'])):
            value = values['values'][k]

            for m in range(0, len(values['histogram'])):
                row = values['histogram'][m]

                if m == 0:
                    if row['start_interval'] <= value[key] <= row['start_interval'] + step:
                        row['histogram'].append(value)
                else:
                    if row['start_interval'] < value[key] <= row['start_interval'] + step:
                        row['histogram'].append(value)

    return copy.deepcopy(his_data)


def gen_histogram_graph(data):
    precision = 2
    graphs = []

    for row in data:
        x = []
        y = []
        for his in row['histogram']:
            if his['start_interval'] == 0:
                label_x = str(round(his['start_interval'], precision))
                label_x += ' - '
                label_x += str(round(his['start_interval'] + his['step'], precision))
            else:
                label_x = str(round(his['start_interval'] + his['step']/10, precision))
                label_x += ' - '
                label_x += str(round(his['start_interval'] + his['step'], precision))

            x.append(label_x)
            y.append(len(his['histogram']))

        title = 'Histogram hodnot v case ' + str(row['start_time']) + 's'

        graphs.append({
            'title': title,
            'graphs': [
                {
                    'timestamps': x,
                    'values': y,
                    'label_x': 'Pocet hodnot',
                    'color': 'red',
                },
            ],
            'group': 'one'
        })

    return graphs


def his_first_value(his):
    for row in his:
        if len(row['histogram']) == 0:
            continue

        return row['histogram'][0]


def his_to_data_for_normalization(histogram, func):
    test_start_time = 1525240923
    values = []

    for row in histogram:
        val = func(row['histogram'])

        values.append({
            'at': test_start_time + row['start_time'],
            'value': val
        })

    # rozgenerovanie
    out_values = []
    last_timestamp = values[0]['at']
    for val in values:

        for i in range(last_timestamp, val['at']):
            out_values.append({
                'at': i,
                'value': val['value']
            })

        last_timestamp = val['at']

    out = {
        'times': {
            'event_start': test_start_time,
            'event_end': test_start_time + histogram[-1]['start_time'] + histogram[-1]['time_step']
        },
        'data': [
            {
                'values': [
                    {
                        'measured': out_values,
                        'custom_name': 'estimate'
                    }
                ]
            }
        ],
    }

    return out


def norm_all(data):
    events = copy.deepcopy(data)

    for i in range(0, len(events)):
        event = events[i]

        for j in range(0, len(event['data'])):
            event_data = event['data'][j]

            for k in range(0, len(event_data['values'])):
                device_value = event_data['values'][k]
                measured = device_value['measured']

                device_value['measured'] = compute_norm_values(measured)

    return events


def filter_data(events, allow_items):
    """Filter umoznuje vybrat pozadovane moduly so zadanym custom_name.

    :param events: stiahnute normalizovane data
    :param allow_items: zoznam custom_name
    """

    out = copy.deepcopy(events)

    for i in range(0, len(out)):
        event = out[i]

        for j in range(0, len(event['data'])):
            event_data = event['data'][j]

            filtered_device_values = []
            for k in range(0, len(event_data['values'])):
                device_value = event_data['values'][k]
                measured = device_value['measured']

                if device_value['custom_name'] not in allow_items:
                    continue

                device_value['measured'] = compute_norm_values(measured)
                filtered_device_values.append(device_value)

            event_data['values'] = filtered_device_values

    return out


def filter_one_values(event, allow_item):
    """Filter umoznuje vybrat s pozadovaneho modulu zoznam nameranych hodnot.
    """

    for j in range(0, len(event['data'])):
        event_data = event['data'][j]

        for k in range(0, len(event_data['values'])):
            device_value = event_data['values'][k]
            measured = copy.deepcopy(device_value['measured'])

            if device_value['custom_name'] == allow_item:
                return measured

    return {}


def convert_relative_humidity_to_partial_pressure(events, temp_module, hum_module):
    a0 = 6.107799961
    a1 = 4.436518521e-1
    a2 = 1.428945805e-2
    a3 = 2.650648471e-4
    a4 = 3.031240396e-6
    a5 = 2.034080948e-8
    a6 = 6.136820929e-11

    for i in range(0, len(events)):
        event_data = events[i]['data']

        for j in range(0, len(event_data)):
            device_values = event_data[j]['values']

            measured_temp = None
            measured_hum = None
            for k in range(0, len(device_values)):
                module = device_values[k]

                if temp_module == module['custom_name']:
                    measured_temp = module['measured']

                if hum_module == module['custom_name']:
                    measured_hum = module['measured']

            for k in range(0, len(measured_temp)):
                temp = measured_temp[k]['value']
                hum = measured_hum[k]['value']
                res = (a0 + temp * (a1 + temp * (a2 + temp * (a3 + temp * (a4 + temp * (a5 + temp * a6)))))) * hum / 100
                measured_hum[k]['partial_pressure'] = res

    return events


def convert_relative_humidity_to_absolute_humidity(events, temp_module, hum_module):

    for i in range(0, len(events)):
        event_data = events[i]['data']

        for j in range(0, len(event_data)):
            device_values = event_data[j]['values']

            measured_temp = None
            measured_hum = None
            for k in range(0, len(device_values)):
                module = device_values[k]

                if temp_module == module['custom_name']:
                    measured_temp = module['measured']

                if hum_module == module['custom_name']:
                    measured_hum = module['measured']

            for k in range(0, len(measured_temp)):
                temp = measured_temp[k]['value']
                hum = measured_hum[k]['value']
                res = (6.112 * math.exp((17.67 * temp) / (temp + 243.5)) * hum * 2.1674)/(273.15 + temp)
                measured_hum[k]['absolute_humidity'] = res

    return events


def convert_absolute_humidity_to_relative_humidity(events, temp_module, hum_module):
    for i in range(0, len(events)):
        event_data = events[i]['data']

        for j in range(0, len(event_data)):
            device_values = event_data[j]['values']

            measured_temp = None
            measured_hum = None
            for k in range(0, len(device_values)):
                module = device_values[k]

                if temp_module == module['custom_name']:
                    measured_temp = module['measured']

                if hum_module == module['custom_name']:
                    measured_hum = module['measured']

            for k in range(0, len(measured_temp)):
                temp = measured_temp[k]['value']
                hum = measured_hum[k]['absolute_humidity']
                res = (hum * (273.15 + temp)) / (6.112 * math.exp((17.67 * temp) / (temp + 243.5)) * 2.1674)
                measured_hum[k]['relative_humidity_in'] = res

    return events


def convert_relative_humidity_to_specific_humidity(events, temp_module, hum_module):
    for i in range(0, len(events)):
        event_data = events[i]['data']

        for j in range(0, len(event_data)):
            device_values = event_data[j]['values']

            measured_temp = None
            measured_hum = None
            for k in range(0, len(device_values)):
                module = device_values[k]

                if temp_module == module['custom_name']:
                    measured_temp = module['measured']

                if hum_module == module['custom_name']:
                    measured_hum = module['measured']

            for k in range(0, len(measured_temp)):
                temp = measured_temp[k]['value']
                hum = measured_hum[k]['value']
                saturated_partial_pressure = math.exp(23.58 - (4044.6/(235.63 + temp)))
                partial_pressure = (hum * saturated_partial_pressure) / 100
                res = (622 * partial_pressure) / (101500 - partial_pressure)
                measured_hum[k]['specific_humidity'] = res

    return events


def calculate_discharge_coefficient(wind):
    Lv = 0.503
    h = 1.364
    alpha = 90
    us = wind
    mi = 1.825e-5
    ro = 1.204
    e = 0.00018

    pore_h = 0.0016
    pore_w = 0.0014
    pore_area = pore_w * pore_h

    num_pores_w = Lv / (pore_w + e)
    num_pores_h = h / (pore_h + e)

    pore_area_total = (num_pores_w * num_pores_h) * pore_area
    window_area_total = Lv * h

    porosity = pore_area_total / window_area_total

    a = porosity
    K = 3.44e-9 * pow(a, 1.6)
    Y = 4.3e-2 * pow(a, -2.13)

    rep = math.sqrt(K) * us * ro / mi
    if rep == 0:
        f = 2 * e / pow(K, 0.5) * Y
    else:
        f = 2 * e / pow(K, 0.5) * (1 / rep + Y)
    c_dF = 1/pow(f, 0.5)
    tmp = 1.9 + 0.7 * math.exp(-Lv / (32.5 * h * math.sin(alpha)))
    c_dLH = pow(tmp, -0.5)
    res = math.sqrt(1/(1/pow(c_dF, 2) + 1/pow(c_dLH, 2)))

    return res


def calculate_air_flow_1(cd, width, height, temp_out, temp_diff):
    return (cd * width * height / 3) * math.sqrt(9.81 * height * temp_diff / (temp_out + 273.15))


def calculate_air_flow_2(width, height, temp_diff):
    return (width * height / 2) * math.sqrt(0.0035 * height * temp_diff)


def calculate_air_flow_3(width, height, wind_speed, wind_turbulence, meteo_wind_speed, stack_effect, temp_in, temp_out):
    mean_wind_speed = wind_turbulence + wind_speed * pow(meteo_wind_speed, 2) + stack_effect * height * abs(temp_in - temp_out)
    return (3.6 * 500 * width * height * pow(mean_wind_speed, 0.5)) / 3600


def estimate_relative_humidity(events, hum_module_in, hum_module_out, temp_module_in):
    out = copy.deepcopy(events)

    for i in range(0, len(out)):
        event_data = out[i]['data']
        wind = out[i]['wind_speed']
        for j in range(0, len(event_data)):
            device_values = event_data[j]['values']

            measured_hum_in = None
            measured_hum_out = None
            measured_temp_in = None
            for k in range(0, len(device_values)):
                module = device_values[k]

                if hum_module_in == module['custom_name']:
                    measured_hum_in = module['measured']

                if hum_module_out == module['custom_name']:
                    measured_hum_out = module['measured']

                if temp_module_in == module['custom_name']:
                    measured_temp_in = module['measured']

            discharge_coefficient = calculate_discharge_coefficient(wind)
            for k in range(0, len(measured_hum_in)):
                temp_diff = abs(out[i]['data'][j]['values'][2]['measured'][0]['value']
                                - out[i]['data'][j]['values'][0]['measured'][0]['value'])
                air_flow_1 = calculate_air_flow_1(discharge_coefficient, 0.503, 1.364,
                                out[i]['data'][j]['values'][0]['measured'][0]['value'], temp_diff)
                air_flow_2 = calculate_air_flow_2(0.503, 1.364, temp_diff)
                air_flow_3 = calculate_air_flow_3(0.503, 1.364, 0.001, 0.01, wind, 0.0035,
                                out[i]['data'][j]['values'][2]['measured'][0]['value'],
                                out[i]['data'][j]['values'][0]['measured'][0]['value'])
                hum_in = measured_hum_in[0]['specific_humidity']
                hum_out = measured_hum_out[0]['specific_humidity']
                #without heating
                #res = (hum_out + (hum_in - hum_out) * math.exp(-air_flow_1 / 52.4 *
                # (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])))
                res1 = hum_out + (hum_in - hum_out) * math.exp(-air_flow_1 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])) + \
                         (0 / 3600) / air_flow_1 * (1 - math.exp(-air_flow_1 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])))
                res2 = hum_out + (hum_in - hum_out) * math.exp(-air_flow_2 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])) + \
                         (0 / 3600) / air_flow_2 * (1 - math.exp(-air_flow_2 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])))
                res3 = hum_out + (hum_in - hum_out) * math.exp(-air_flow_3 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])) + \
                         (0 / 3600) / air_flow_3 * (1 - math.exp(-air_flow_3 / 52.4 *
                         (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])))
                res4 = (hum_in * math.exp(-(measured_hum_in[k]['at'] - measured_hum_in[0]['at']) * air_flow_1 / 52.4) + (0 / (air_flow_1 * 1.2) + hum_out) * (1 - math.exp(-(measured_hum_in[k]['at'] - measured_hum_in[0]['at']) * air_flow_1 / 52.4)))
                res5 = (((0 + air_flow_1 * hum_out - air_flow_1 * hum_in) * (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])) / 52.4)
                res6 = (hum_in - hum_out) * math.exp(-air_flow_1 / 52.4 * (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])) + hum_out + (0 / air_flow_1) * (1 - math.exp(-air_flow_1 / 52.4 * (measured_hum_in[k]['at'] - measured_hum_in[0]['at'])))

                saturated_partial_pressure = math.exp(23.58 - (4044.6 / (235.63 + measured_temp_in[0]['value'])))
                measured_hum_in[k]['hum_in_estimated1'] = ((res1 * 101500) / (res1 + 622)) / saturated_partial_pressure * 100
                measured_hum_in[k]['hum_in_estimated2'] = ((res2 * 101500) / (res2 + 622)) / saturated_partial_pressure * 100
                measured_hum_in[k]['hum_in_estimated3'] = ((res3 * 101500) / (res3 + 622)) / saturated_partial_pressure * 100
                measured_hum_in[k]['hum_in_estimated4'] = ((res4 * 101500) / (res4 + 622)) / saturated_partial_pressure * 100
                measured_hum_in[k]['hum_in_estimated5'] = (((hum_in + res5) * 101500) / ((hum_in + res5) + 622)) / saturated_partial_pressure * 100
                measured_hum_in[k]['hum_in_estimated6'] = ((res6 * 101500) / (res6 + 622)) / saturated_partial_pressure * 100
    return out


def gen_histogram_graph_with_factor(data):
    """
    https://www.windows2universe.org/earth/Atmosphere/wind_speeds.html
    """
    precision = 2
    graphs = []
    wind_desc = ['<1', '1-5', '6-11', '12-19', '20-28', '29-']


    for row in data:
        stacked = [[], [], [], [], [], []]

        x = y = []

        for his in row['histogram']:
            c0 = c1 = c2 = c3 = c4 = c5 = 0

            if his['start_interval'] == 0:
                label_x = str(round(his['start_interval'], precision))
                label_x += ' - '
                label_x += str(round(his['start_interval'] + his['step'], precision))
            else:
                label_x = str(round(his['start_interval'] + his['step']/10, precision))
                label_x += ' - '
                label_x += str(round(his['start_interval'] + his['step'], precision))

            x.append(label_x)

            for item in his['histogram']:
                f = item['weather_dw']['wind_speed']

                if f < 1:
                    c0 += 1
                elif f <= 5:
                    c1 += 1
                elif f <= 11:
                    c2 += 1
                elif f <= 19:
                    c3 += 1
                elif f <= 28:
                    c4 += 1
                else:
                    c5 += 1

            stacked[0].append(c0)
            stacked[1].append(c1)
            stacked[2].append(c2)
            stacked[3].append(c3)
            stacked[4].append(c4)
            stacked[5].append(c5)

        title = 'Histogram hodnot v case ' + str(row['start_time']) + 's'

        gg = []
        for i in range(0, len(stacked)):
            gg.append({
                'timestamps': x,
                'values': stacked[i],
                'label_x': wind_desc[i],
                'color': COLORS[i],
            })

        graphs.append({
            'title': title,
            'graphs': gg
        })

    return graphs


def to_csv_file(event, module_name, cols, write_each=1, filename='out.csv',
                time_format='%H:%M:%S'):

    separator = ';'

    # header
    header = ''
    for i in range(0, len(cols)):
        col = cols[i]
        header += col

        if i != len(cols) - 1:
            header += separator
        else:
            header += '\n'

    # body
    body = ''
    for module in event['data'][0]['values']:
        if module['custom_name'] != module_name:
            continue

        for i in range(0, len(module['measured'])):
            value = module['measured'][i]

            if i % write_each != 0:
                continue

            for k in range(0, len(cols)):
                key = cols[k]

                if key == 'at':
                    body += utc_timestamp_to_str(value[key], time_format)
                else:
                    body += str(value[key])

                if k != len(cols) - 1:
                    body += separator
                else:
                    body += '\n'

    out = (header + body).replace('.', ',')

    with open(filename, 'w') as f:
        f.write(out)

    return out


def cut_events(events, start, end):
    out = copy.deepcopy(events)

    for i in range(0, len(out)):
        event = out[i]

        # new times in events
        s = event['times']['event_start'] = event['times']['event_start'] + start
        e = event['times']['event_end'] = event['times']['event_start'] + end

        # cut values between start and end
        for j in range(0, len(event['data'][0]['values'])):
            module = event['data'][0]['values'][j]

            new_values = []
            for k in range(0, len(module['measured'])):
                value = module['measured'][k]

                if s <= value['at'] < e:
                    new_values.append(value)

            module['measured'] = new_values

        # cut weather
        new_weather = []
        for j in range(0, len(event['data'][0]['weather_dw'])):
            weather = event['data'][0]['weather_dw'][j]

            if s <= weather['at'] < e:
                new_weather.append(weather)

        event['data'][0]['weather_dw'] = new_weather

    return out


def filter_number_events(events, count):
    out = []

    for event in events:
        if len(event['data'][0]['weather_dw']) == count:
            out.append(copy.deepcopy(event))

    return out


def find_module_measured(event, module_name):
    modules = event['data'][0]['values']

    for module in modules:
        if module_name == module['custom_name']:
            return module['measured']

    raise ValueError('unknown module %s' % module_name)


def find_module(event, module_name):
    modules = event['data'][0]['values']

    for i in range(0, len(modules)):
        module = modules[i]

        if module_name == module['custom_name']:
            return module

    raise ValueError('unknown module %s' % module_name)


def extract_value(modules, module_name, value_index):
    """Funkcia vyberie zo zoznamu modulov pozadovany modul a nasledne hodnotu na zadanom indexe.
    """
    for row in modules:
        if row['custom_name'] == module_name:
            return row['measured'][value_index]

    raise ValueError('unknown module %s' % module_name)


def to_zzn_csv(events, sep, header, func_row, write_each=15):
    """Funkcia na vygenerovanie troch suborov so zadanych eventov.
    Prvy (f1) subor obsahuje len udalosti otvorenia okna.
    Druhy (f2) subor obsahuje udalosti otvorenia okna a udaje z no_event_start,
    co sluzi na rozdelenie dat tak, aby 50 % boli udalosti s otvorenim okna a
    zvysnych 50 % udalosti, kedy k otvoreniu okna nedoslo.
    Treti (f3) subor obsahuje vsetky namerane udaje pocas otvorenia okna.

    :param events: zoznam vsetkych eventov
    :param sep: znak, ktory oddeluje stlpce
    :param header: hlavicka csv suboru
    :param func_row: funkcia, ktora spracuje data a vrati jeden riadok nameranych dat
    :param write_each: zapise sa len kazda x-ta hodnota
    :return:
    """

    # file with data related to window opening from event_start
    f1 = 'open.csv'
    f1_content = header

    # file with data related to window opening from event_start and window closing from
    # no_event_start
    f2 = 'open_close.csv'
    f2_content = header

    # file with event_start data without last value that contains window closing date
    f3 = 'all.csv'
    f3_content = header

    for event in events:
        for event_type in event['data']:
            modules = event_type['values']
            value_count = len(event_type['weather_dw'])

            for i in range(0, value_count):
                # potrebujeme poznat aj poslednu polozku, takze ju nepreskocime
                if i % write_each != 0 and i != value_count - 1:
                    continue

                row = func_row(
                    event,
                    modules,
                    i,
                    sep,
                    value_count,
                    event['times'][event_type['type']],
                    event_type['type']
                ) + '\n'

                # write only window opening date
                if i == 0 and event_type['type'] == 'event_start':
                    f1_content += row
                    f2_content += row

                # write only window closing data
                elif i == value_count - 1 and event_type['type'] == 'no_event_start':
                    f2_content += row

                # write all event_start data
                if event_type['type'] == 'event_start':
                    f3_content += row

    with open(f1, 'w') as f:
        f.write(f1_content)

    with open(f2, 'w') as f:
        f.write(f2_content)

    with open(f3, 'w') as f:
        f.write(f3_content)

    return f1_content, f2_content, f3_content


class UtilCO2:
    CO_MOLECULAR_WEIGHT = 44.0095 # g / mol

    @staticmethod
    # http://www.aresok.org/npg/nioshdbs/calc.htm
    def co2_ppm_to_mg_m3(co2):
        return co2 * UtilCO2.CO_MOLECULAR_WEIGHT / 24.45

    @staticmethod
    # http://www.aresok.org/npg/nioshdbs/calc.htm
    def co2_mg_m3_to_ppm(co2):
        return co2 * 24.45 / UtilCO2.CO_MOLECULAR_WEIGHT

    @staticmethod
    # http://www.umsl.edu/~biofuels/Energy%20Meter%20labs/How%20much%20volume%20does%20a%20kg%20of%20CO2%20occupy.pdf
    # https://www.icbe.com/carbondatabase/CO2volumecalculation.asp
    # https://en.wikipedia.org/wiki/Boyle%27s_law
    # https://en.wikipedia.org/wiki/Atmospheric_pressure
    def co2_g_h_to_l_h(co_weight, temperature=25):
        n = co_weight / UtilCO2.CO_MOLECULAR_WEIGHT
        R = 8.3144598
        P = 1.01325  # tlak v baroch
        T = 275.15 + temperature

        V = (n * R * T) / P

        return V / 100  # prevod do litrov

    @staticmethod
    # http://www.umsl.edu/~biofuels/Energy%20Meter%20labs/How%20much%20volume%20does%20a%20kg%20of%20CO2%20occupy.pdf
    # https://www.icbe.com/carbondatabase/CO2volumecalculation.asp
    # https://en.wikipedia.org/wiki/Boyle%27s_law
    # https: // en.wikipedia.org / wiki / Atmospheric_pressure
    def co2_l_h_to_g_h(V, temperature=25):
        R = 8.3144598
        P = 1.01325  # tlak v baroch
        T = 275.15 + temperature

        n = (V * P) / (R * T)

        return n * UtilCO2.CO_MOLECULAR_WEIGHT * 100

    @staticmethod
    def estimate_time(Ci_t, V, Q, F):
        """
        Odhad casu, za ktory sa dosiahne dana koncentracia CO2.

        :param Ci_t: cielova koncentracia [ppm]
        :param V: objem miestnosti [m^3]
        :param Q: vymena vzduhu medzi dnu/von [m^3/h]
        :param F: rychlost generace [l/h]
        :return: cas, za ktory sa dosiahne dana koncentracia [h]
        """

        Ci_t = UtilCO2.co2_ppm_to_mg_m3(Ci_t)
        F = UtilCO2.co2_l_h_to_g_h(F) * 1000  # g to mg

        return (V / Q) * math.log(F / (F - (Q * Ci_t)))

    @staticmethod
    def estimate_ppm(ti, C0, Ca, V, Q, F):
        """
        Odhad koncentracie CO2, pouzite jednotky mozu byt ppm.

        :param ti: cas [h]
        :param C0: pociatocna koncentracia v case t = 0 [ppm]
        :param Ca: vonkajsia koncentracia [ppm]
        :param V: objem miestnosti [m^3]
        :param Q: vymena vzduhu medzi dnu/von [m^3/h]
        :param F: rychlost generace [l/h]
        :return: koncentrace v case ti [ppm]
        """

        l = Q / V

        diff = (C0 - Ca) * math.exp(-l * ti)
        emission = (F * 1000) / (l * V) * (1 - math.exp(-l * ti))

        return Ca + diff + emission

    @staticmethod
    def estimate_mg_m3(ti, C0, Ca, V, Q, F):
        """
        Odhad koncentracie CO2, pouzite jednotky mozu byt g/m^3.

        :param ti: cas [h]
        :param C0: pociatocna koncentracia v case t = 0 [g/m^3]
        :param Ca: vonkajsia koncentracia [g/m^3]
        :param V: objem miestnosti [m^3]
        :param Q: vymena vzduhu medzi dnu/von [m^3/h]
        :param F: rychlost generace [l/h]
        :return: koncentrace v case ti [g/m^3]
        """

        C0 = UtilCO2.co2_ppm_to_mg_m3(C0)
        Ca = UtilCO2.co2_ppm_to_mg_m3(Ca)
        F = UtilCO2.co2_l_h_to_g_h(F) * 1000  # g to mg

        l = Q / V

        diff = (C0 - Ca) * math.exp(-l * ti)
        emission = F / (l * V) * (1 - math.exp(-l * ti))

        return UtilCO2.co2_mg_m3_to_ppm(Ca + diff + emission)

    @staticmethod
    def generate_time_shift(events, time_interval, threshold):
        """
        Najdenie casoveho posunu, kde pokles CO2 za dany casovy interval je vacsi ako prah.

        :param events:
        :param time_interval: posun, v ktorom sa bude kontrolovat rozdiel hodnot
        :param threshold: rozdiel hodnot CO2
        :return:
        """
        for i in range(0, len(events)):
            event = events[i]

            for j in range(0, len(event['data'][0]['values'])):
                module = event['data'][0]['values'][j]

                if module['custom_name'] != 'co2':
                    continue

                for k in range(0, len(module['measured']) - time_interval):
                    first_value = module['measured'][k]['value'] - threshold
                    second_value = module['measured'][k + time_interval]['value']

                    if first_value > second_value:
                        event['time_shift'] = k
                        break

        return events


class UtilTempHum:
    @staticmethod
    def generate_time_shift(event, module_name, window_size, threshold_rastuce):
        drop_time = None

        for j in range(0, len(event['data'][0]['values'])):
            module = event['data'][0]['values'][j]

            if module['custom_name'] != module_name:
                continue

            der = []
            for k in range(0, len(module['measured']) - 2):
                value = module['measured'][k]
                next_value = module['measured'][k + 2]

                der.append(Derivation().compute([value, next_value], 1)[1])
            der.append(0)
            der.append(0)

            for k in range(window_size, len(der)):
                derivacie_klesajuce = 0
                derivacie_nulove = 0

                for p in range(0, window_size):
                    if der[k - p] < 0:
                        derivacie_klesajuce += 1

                    if der[k - p] == 0:
                        derivacie_nulove += 1

                if (derivacie_klesajuce + derivacie_nulove) < threshold_rastuce:
                    drop_time = k - (window_size - threshold_rastuce)
                    break

            for k in range(0, len(module['measured'])):
                if k > drop_time:
                    break

                module['measured'][k]['value_for_first_drop'] = module['measured'][k]['value'] + 2


        return drop_time

    @staticmethod
    def lin_reg_first_drop(event):
        start_hum_val = None
        drop_hum_val = None

        for j in range(0, len(event['data'][0]['values'])):
            module = event['data'][0]['values'][j]

            if module['custom_name'] != 'humidity_in':
                continue

            x = []
            y = []

            for k in range(0, len(module['measured'])):
                value = module['measured'][k]

                if 'value_for_first_drop' in value:
                    x.append(k)
                    y.append(value['value_for_first_drop'] - 2)

            if not x:
                continue

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            for k in range(0, len(module['measured'])):
                value = module['measured'][k]

                if 'value_for_first_drop' in value:
                    value['lin_reg'] = intercept + slope * k
                else:
                    drop_hum_val = module['measured'][k - 1]['lin_reg']
                    break

            info = {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err,
                'eq': str(intercept) + ' + (' + str(slope) + ') * x'
            }

            start_hum_val = module['measured'][0]['lin_reg']
            return start_hum_val, drop_hum_val, info

    @staticmethod
    def lin_reg_second_drop(event):
        for j in range(0, len(event['data'][0]['values'])):
            module = event['data'][0]['values'][j]

            if module['custom_name'] != 'humidity_in':
                continue

            x = []
            y = []

            for k in range(0, len(module['measured'])):
                value = module['measured'][k]

                if 'value_for_first_drop' not in value:
                    x.append(k)
                    y.append(value['value'])

            if not x:
                continue

            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            for k in range(0, len(module['measured'])):
                value = module['measured'][k]

                if 'lin_reg' not in value:
                    value['lin_reg'] = intercept + slope * k

            return {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err,
                'eq': str(intercept) + ' + (' + str(slope) + ') * x'
            }

    @staticmethod
    def lin_reg_lomeny_graph(events, module_name, window_size, threshold_rastuce):
        for i in range(0, len(events)):
            event = events[i]

            if event['graph_hum_type_1'] != 'lomeny':
                continue

            drop_time = UtilTempHum.generate_time_shift(event,
                                                        module_name,
                                                        window_size,
                                                        threshold_rastuce)

            start_hum, drop_hum, info = UtilTempHum.lin_reg_first_drop(event)

            module = find_module(event, module_name)
            module['lin_reg'] = {
                'drop_shift': drop_time,
                'hum_val_start' : start_hum,
                'hum_val_drop': drop_hum,
                'first_drop_lin_reg': info,
                'second_drop_lin_reg': UtilTempHum.lin_reg_second_drop(event),
            }

    @staticmethod
    def lin_reg_linearni_graph(events, module_name):
        for i in range(0, len(events)):
            event = events[i]

            if event['graph_hum_type_1'] != 'linearni':
                continue

            start_hum, info = UtilTempHum.lin_reg_whole_curve(event)

            module = find_module(event, module_name)
            module['lin_reg'] = {
                'hum_val_start': start_hum,
                'lin_reg_info': info,
            }


def main():
    pass
