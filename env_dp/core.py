import copy
import csv
import datetime
import hashlib
import http.client
import json
import logging
import os
import requests
import ssl
import time
from socket import error as SocketError

COLORS = ['red', 'green', 'blue', 'orange', 'purple', 'silver', 'black']


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

    def __init__(self, precision=1, cache=True, cache_folder='../cache'):
        self.__precision = precision
        self.__cache = cache
        self.__cache_folder = cache_folder
        self.__log = logging.getLogger(self.__class__.__name__)

        if cache:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)


    def __remove_from_cache(self, start, end):
        day_time_start = datetime.datetime.fromtimestamp(start).strftime('%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = datetime.datetime.fromtimestamp(end).strftime('%Y%m%d %H:%M:%S')
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
        day_time_start = datetime.datetime.fromtimestamp(start).strftime('%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = datetime.datetime.fromtimestamp(end).strftime('%Y%m%d %H:%M:%S')
        day_end = day_time_end[:-9]

        url = 'https://api.weather.com/v1/geocode/49.15139008/16.69388962/observations/'
        url += 'historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e'
        url += '&startDate=' + str(day_start) + '&endDate=' + str(day_end)

        h = hashlib.sha256()
        h.update(url.encode("utf8"))
        filename = self.__cache_folder + '/weather_' + h.hexdigest()

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
        while True:
            try:
                self.__log.info(str(start) + " - " + str(end))
                return self.__weather_data2(start, end)
            except KeyError:
                self.__log.debug('wait')
                self.__remove_from_cache(start, end)
                time.sleep(1)
            except ConnectionResetError:
                self.__log.debug('wait')
                time.sleep(1)
            except SocketError:
                self.__log.debug('wait')
                time.sleep(1)
            except IndexError:
                self.__log.debug('wait')
                time.sleep(1)

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

        tmp = copy.deepcopy(out_general)
        out_general = []
        f = tmp[0]['at']
        for i in tmp:
            if i['at'] % 1800 != 0:
                continue

            while True:
                if f <= i['at']:
                    out_general.append(i)
                    f += 1800
                else:
                    break

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


class WeatherDataRS:
    def __init__(self, file='../klimadata_admas.csv', precision=9):
        self.__file = file
        self.__precision = precision
        self.__log = logging.getLogger(self.__class__.__name__)

    def download_data(self, start, end):
        day_time_start = datetime.datetime.fromtimestamp(start).strftime('%Y%m%d %H:%M:%S')
        day_start = day_time_start[:-9]
        day_time_end = datetime.datetime.fromtimestamp(end).strftime('%Y%m%d %H:%M:%S')
        day_end = day_time_end[:-9]
        out_general = []

        with open(self.__file, newline='') as file:
            reader = csv.DictReader(file, delimiter=';')

            for line in reader:
                date_time = int(time.mktime(datetime.datetime.strptime(line['datum_a_cas'], '%d.%m.%y %H:%M').timetuple()))
                if date_time < start or date_time > end:
                    continue

                out_general.append({
                        'at': int(time.mktime(datetime.datetime.strptime(line['datum_a_cas'], '%d.%m.%y %H:%M').timetuple())),
                        'pressure': round(float(line['atmosfericky_tlak'].replace(',', '.')), self.__precision),
                        'temperature': round(float(line['teplota_vzduchu'].replace(',', '.')), self.__precision),
                        'relative_humidity': round(float(line['relativna_vlhkost'].replace(',', '.')), self.__precision),
                        'wind_direction': round(float(line['smer_vetra'].replace(',', '.')), self.__precision),
                        'wind_speed': round(float(line['rychlost_vetra'].replace(',', '.')), self.__precision),
                        'wind_speed2': round(float(line['rychlost_vetra2'].replace(',', '.')), self.__precision),
                        'intensity_of_sunlight': round(float(line['rychlost_vetra2'].replace(',', '.')), self.__precision),
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
            if out_general[i + 1]['at'] - out_general[i]['at'] == 60:
                pressure_start = out_general[i]['pressure']
                pressure_end = out_general[i + 1]['pressure']
                if pressure_start - pressure_end == 0:
                    pressure_increase = 0
                else:
                    pressure_diff = pressure_start - pressure_end
                    pressure_increase = pressure_diff / 60.0

                temp_start = out_general[i]['temperature']
                temp_end = out_general[i + 1]['temperature']
                if temp_start - temp_end == 0:
                    temp_increase = 0
                else:
                    temp_diff = temp_end - temp_start
                    temp_increase = temp_diff / 60.0

                rh_start = out_general[i]['relative_humidity']
                rh_end = out_general[i + 1]['relative_humidity']
                if rh_start - rh_end == 0:
                    rh_increase = 0
                else:
                    rh_diff = rh_end - rh_start
                    rh_increase = rh_diff / 60.0

                wind_direction_start = out_general[i]['wind_direction']
                wind_direction_end = out_general[i + 1]['wind_direction']
                if wind_direction_start - wind_direction_end == 0:
                    wind_direction_increase = 0
                else:
                    wind_direction_diff = wind_direction_end - wind_direction_start
                    wind_direction_increase = wind_direction_diff / 60.0

                wind_speed_start = out_general[i]['wind_speed']
                wind_speed_end = out_general[i + 1]['wind_speed']
                if wind_speed_start - wind_speed_end == 0:
                    wind_speed_increase = 0
                else:
                    wind_speed_diff = wind_speed_end - wind_speed_start
                    wind_speed_increase = wind_speed_diff / 60.0

                wind_speed2_start = out_general[i]['wind_speed2']
                wind_speed2_end = out_general[i + 1]['wind_speed2']
                if wind_speed2_start - wind_speed2_end == 0:
                    wind_speed2_increase = 0
                else:
                    wind_speed2_diff = wind_speed2_end - wind_speed2_start
                    wind_speed2_increase = wind_speed2_diff / 60.0

                intensity_of_sunlight_start = out_general[i]['intensity_of_sunlight']
                intensity_of_sunlight_end = out_general[i + 1]['intensity_of_sunlight']
                if intensity_of_sunlight_start - intensity_of_sunlight_end == 0:
                    intensity_of_sunlight_increase = 0
                else:
                    intensity_of_sunlight_diff = intensity_of_sunlight_end - intensity_of_sunlight_start
                    intensity_of_sunlight_increase = intensity_of_sunlight_diff / 60.0

                pressure = pressure_start
                temp = temp_start
                rh = rh_start
                wind_direction = wind_direction_start
                wind_speed = wind_speed_start
                wind_speed2 = wind_speed2_start
                intensity_of_sunlight = intensity_of_sunlight_start

                for j in range(0, 60):
                    out_detailed.append({
                        'at': int(out_general[i]['at']) + j,
                        'pressure': round(float(pressure), self.__precision),
                        'temperature': round(float(temp), self.__precision),
                        'relative_humidity': round(float(rh), self.__precision),
                        'wind_direction': round(float(wind_direction), self.__precision),
                        'wind_speed': round(float(wind_speed), self.__precision),
                        'wind_speed2': round(float(wind_speed2), self.__precision),
                        'intensity_of_sunlight': round(float(intensity_of_sunlight), self.__precision),
                    })
                    pressure = pressure + pressure_increase
                    temp = temp + temp_increase
                    rh = rh + rh_increase
                    wind_direction = wind_direction + wind_direction_increase
                    wind_speed = wind_speed + wind_speed_increase
                    wind_speed2 = wind_speed2 + wind_speed2_increase
                    intensity_of_sunlight = intensity_of_sunlight + intensity_of_sunlight_increase
            else:
                continue

        return out_detailed


class DataStorage:
    def __init__(self, client, weather_client, precision=1):
        self.__client = client
        self.__meta_data = []
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__weather_client = weather_client
        self.__precision = precision

    def __parser_date(self, date):
        return datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S").timestamp()

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

            types = ['event_start', 'no_event_start']

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

    def __cut_normalization(self, times, data):
        start = times['event_start']
        end = times['event_end']

        for i in range(0, len(data['values'])):
            values = data['values'][i]
            out_json = []

            for row in values['measured']:
                if row['at'] < start or row['at'] > end:
                    continue


                out_json.append(row)

            values['measured'] = out_json

        return data

    def filter_downloaded_data(self, temp_in, hum_in, temp_out, hum_out, temp_diff_min, temp_diff_max, hum_diff_min,
                               hum_diff_max):
        out_json_temp_in = []
        out_json_temp_out = []
        out_json_hum_in = []
        out_json_hum_out = []

        for i in range(0, len(temp_in)):
            temp_diff = abs(temp_in[i]['data'][0]['values'][0]['measured'][0]['value']
                            - temp_out[i]['data'][0]['values'][0]['measured'][0]['value'])
            hum_diff = abs(hum_in[i]['data'][0]['values'][0]['measured'][0]['partial_pressure']
                           - hum_out[i]['data'][0]['values'][0]['measured'][0]['partial_pressure'])

            if ((temp_diff >= temp_diff_min and temp_diff <= temp_diff_max) and (
                    hum_diff >= hum_diff_min and hum_diff <= hum_diff_max) and (
                    temp_out[i]['data'][0]['values'][0]['measured'][0]['value'] < 30.0) and (
                    temp_in[i]['window'] == "dokoran")):
                if "silny" in temp_in[i]['weather'] and hum_diff <= 3.0:
                    continue

                out_json_temp_in.append(temp_in[i])
                out_json_temp_out.append(temp_out[i])
                out_json_hum_in.append(hum_in[i])
                out_json_hum_out.append(hum_out[i])

        return out_json_temp_in, out_json_hum_in, out_json_temp_out, out_json_hum_out

    def download_data_for_normalization(self, type_id):
        # 15 minutes
        time_shift = 900

        out_json = copy.deepcopy(self.__meta_data)

        for k in range(0, len(out_json)):
            event = out_json[k]
            e_start = event['times']['event_start']
            e_end = event['times']['event_end']

            event['weather_dw'] = self.__weather_client.weather_data(e_start, e_end)

            for j in range(0, len(event['data'])):
                event_type = event['data'][j]

                if event_type['type'] != 'event_start':
                    continue

                tmp_modules = []
                for i in range(0, len(event_type['values'])):
                    module = event_type['values'][i]

                    if module['custom_name'] in type_id:
                        module['measured'] = self.__client.history(
                            module['gateway'],
                            module['device'],
                            module['module_id'],
                            event['times']['event_start'] - time_shift,
                            event['times']['event_end'] + time_shift
                        )['data']

                        module['measured'] = self.__filter_not_null(module['measured'] )

                        tmp_modules.append(module)

                event_type['values'] = tmp_modules

                event['data'] = [event_type]
                event['data'][j] = self.__generate_event_data(event_type)
                event['data'][j] = self.__cut_normalization(event['times'], event['data'][j])

                # sluzi na odfiltrovanie no_event_start
                break

        out = []
        for event in out_json:
            weather_len = len(event['weather_dw'])
            e_start = event['times']['event_start']
            e_end = event['times']['event_end']
            fail = False

            for event_type in event['data']:
                for row in event_type['values']:
                    if len(row['measured']) != weather_len:
                        s = 'event '
                        s += datetime.datetime.fromtimestamp(e_start).strftime('%Y/%m/%d '
                                                                               '%H:%M:%S')
                        s += ' - '
                        s += datetime.datetime.fromtimestamp(e_end).strftime('%Y/%m/%d '
                                                                             '%H:%M:%S')
                        s += ' is ignored'
                        s += ' stiahnute data neobsahuju data za dany interval (chyba senzora)'

                        self.__log.warning(s)
                        fail = True
                        break

            if not fail:
                out.append(event)

        return out


    def download_data(self, shift_before, shift_after):
        out_json = copy.deepcopy(self.__meta_data)

        for event in out_json:
            for event_type in event['data']:
                e_start_before_timestamp = int(
                    float(event['times'][event_type['type']]) - shift_before)
                e_start_after_timestamp = int(
                    float(event['times'][event_type['type']]) + shift_after)

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
                        e_start_before_timestamp,
                        e_start_after_timestamp
                    )['data']

        return out_json

    def __switch_value(self, value):
        if value == 1:
            return 0

        return 1

    def __generate_event_data(self, event):
        out = copy.deepcopy(event)
        out['values'] = []

        for item in event['values']:
            if len(item['measured']) <= 1:
                if item['type_id'] == 'open_close':
                    out['values'].append(item)
                    continue

                if len(item['measured']) == 0:
                    self.__log.debug(
                        'prazdne hodnoty v modulu: %s, skip' % item['custom_name'])
                    continue

                if len(item['measured']) == 1 and item['type_id'] != 'open_close':
                    self.__log.debug(
                        'len jedna hodnota v modulu: %s, skip' % item['custom_name'])
                    continue

            out_values = []
            for i in range(0, len(item['measured']) - 1):
                value_start = item['measured'][i]['value']
                value_end = item['measured'][i + 1]['value']

                if value_start is None or value_end is None:
                    continue

                value_start = float(item['measured'][i]['value'])
                value_end = float(item['measured'][i + 1]['value'])

                time_start = item['measured'][i]['at']
                time_end = item['measured'][i + 1]['at']

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

        for e in self.__meta_data:
            new_value = e['times']['event_start'] + no_event_start_time_shift
            e['times']['no_event_start'] = new_value

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
                str_out += datetime.datetime.fromtimestamp(float(item['at'])).strftime(
                    '%H:%M:%S') + " "
                str_out += " - "
                str_out += datetime.datetime.fromtimestamp(last_timestamp).strftime(
                    '%H:%M:%S') + " "
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
                str_out += datetime.datetime.fromtimestamp(float(item['at'])).strftime(
                    '%H:%M:%S') + " "
                str_out += " - "
                str_out += datetime.datetime.fromtimestamp(last_timestamp).strftime(
                    '%H:%M:%S') + " "
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

        global_min = None
        global_max = None

        if global_range:
            for i in range(0, len(data)):
                row = data[i]

                for g in row['graphs']:
                    numbers = g['values']

                    if global_min is None:
                        global_min = min(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_min)
                        global_min = min(tmp)

                    if global_max is None:
                        global_max = max(numbers)
                    else:
                        tmp = copy.deepcopy(numbers)
                        tmp.append(global_max)
                        global_max = max(tmp)

        id = 0
        for i in range(0, len(data)):
            row = data[i]
            id += 1
            canvas_id = 'g' + str(id)

            f.write('		<div style="overflow: auto;float:left">\n')
            f.write('			<canvas class="custom" id="g' + str(canvas_id))
            f.write('" width="900px" height="500"></canvas>\n')
            f.write('		</div>\n')

            all_min = None
            all_max = None

            if min_value is not None and max_value is not None:
                all_min = min_value
                all_max = max_value
            elif not global_range:
                for g in row['graphs']:
                    numbers = g['values']

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
                all_min = global_min
                all_max = global_max

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


def gen_simple_graph(measured, color='blue', label='x value', key='value'):
    x = []
    y = []
    for value in measured:
        x.append(datetime.datetime.fromtimestamp(value['at']).strftime('%H:%M:%S'))
        y.append(value[key])

    return {
        'timestamps': x,
        'values': y,
        'label_x': label,
        'color': color,
    }


def split_into_intervals(data, interval):
    new = []

    next_cut = data[0]['at'] + interval

    row = []
    for i in data:
        if i['at'] >= next_cut:
            next_cut += interval
            new.append(list(row))
            row.clear()

        row.append(i)

    if len(row) % interval == 0:
        new.append(list(row))

    return new


def normalization(data, local_min, local_max, key):
    for i in range(0, len(data)):
        data[i][key + "_norm"] = (data[i][key] - local_min) / (local_max - local_min)

    return data


def compute_value(data, interval, delay):
    ii = data[0][0]['norm']

    for i in range(0, len(data)):
        if (i + 1) * interval > delay:
            rozdiel = data[i][0]['norm'] - data[i][-1]['norm']
            ii -= rozdiel/interval * (delay % interval)
            break

        ii -= data[i][0]['norm'] - data[i+1][0]['norm']

    return ii


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


def value_estimate(data, interval, color='red', label='x value', key='value'):
    data = copy.deepcopy(data)

    measured = data['data'][0]['values'][0]['measured']
    start = data['times']['event_start']

    only_values = []
    for row in measured:
        only_values.append(row['value'])

    l_min = min(only_values)
    l_max = max(only_values)

    after_normalization = normalization(measured, l_min, l_max, 'value')
    with_intervals = split_into_intervals(after_normalization, interval)

    y = []
    x = []
    end_loop = start + len(with_intervals) * interval
    for i in range(start, end_loop, 1):
        x.append(datetime.datetime.fromtimestamp(i).strftime('%H:%M:%S'))

        computed_value = compute_value(with_intervals, interval, i - start)
        if key == 'value':
            computed_value *= float(l_max - l_min) + l_min

        y.append(computed_value)

    return {
        'timestamps': x,
        'values': y,
        'label_x': label,
        'color': color,
    }


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

        w = weather_for_histogram(row['weather_dw'])

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
            val['weather'] = row['weather']
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
                }
            ]
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


def main():
    pass
