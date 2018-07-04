import copy
import datetime
import http.client
import json
import logging
import requests
import ssl


class Rest:
	"""Simple rest api client."""

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
			conn = http.client.HTTPSConnection(self.__host, self.__port, context=ssl._create_unverified_context(), timeout=10)

		conn.request(self.__method, self.__end_point, headers=self.__headers, body=self.__body)

		response = conn.getresponse()
		content = str(response.read(), 'utf-8')
		conn.close()
		return response, content


class BeeeOnClient:
	"""Client for communication with server supporting BeeeOn api."""

	def __init__(self, host, port):
		self.__host = host
		self.__port = port
		self.__api_key = ""
		self.__token_id = ""
		self.__log = logging.getLogger(self.__class__.__name__)

	def refresh_token(self):
		data = {'key': self.api_key, 'provider': 'apikey'}
		try:
			req = Rest(self.__host, self.__port, "/auth", "POST", False)
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

		endpoint = '/gateways/' + str(gateway_id) + '/devices/' + str(device_id) + '/sensors'

		req = Rest(self.__host, self.__port, endpoint, "GET", False)
		req.authorize(self.__token_id)

		res, body = req.perform()

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

		req = Rest(self.__host, self.__port, endpoint, "GET", False)
		req.authorize(self.__token_id)

		res, body = req.perform()

		return json.loads(body)

	def gateways(self):
		if not self.__token_id:
			self.__token_id = self.refresh_token()

		endpoint = '/gateways'

		req = Rest(self.__host, self.__port, endpoint, "GET", False)
		req.authorize(self.__token_id)

		res, body = req.perform()

		return json.loads(body)['data']

	def logout(self):
		if not self.__token_id:
			return

		endpoint = '/auth'

		req = Rest(self.__host, self.__port, endpoint, "DELETE", False)
		req.authorize(self.__token_id)

		req.perform()

	@property
	def rest_host(self):
		return self.__host

	@property
	def rest_port(self):
		return self.__port

	@property
	def api_key(self):
		return self.__api_key

	@api_key.setter
	def api_key(self, key):
		self.__api_key = key


class DataStorage:
	def __init__(self, client):
		self.__client = client
		self.__meta_data = []
		self.__log = logging.getLogger(self.__class__.__name__)

	def read_meta_data(self, devices, events):
		with open(devices) as f:
			json_devices = json.load(f)

		with open(events) as f:
			json_events = json.load(f)

		for e in json_events['events']:
			e['event']['start'] = self.__parser_date(e['event']['start'])
			e['event']['end'] = self.__parser_date(e['event']['end'])

			for key, dev in e['event']['devices'].items():

				found = False
				for d_dev in json_devices['devices']:
					if d_dev['id'] == key:
						modules = e['event']['devices'][key]
						e['event']['devices'][key] = d_dev
						e['event']['devices'][key]['modules'] = self.requested_modules(d_dev['gateway'], d_dev['device'], modules)

						self.__meta_data.insert(len(self.__meta_data), e)
						found = True

				if not found:
					self.__log.warning("device %s not found, event was skipped" % key)

	def __parser_date(self, date):
		return datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S").timestamp()

	def requested_modules(self, gateway, device, modules):
		supported_modules = self.download_sensor_modules(gateway, device)

		out = []
		for module in modules:
			found = False
			for supported_module in supported_modules:
				if module == supported_module['type_id']:
					out.append(supported_module)
					found = True

			if not found:
				self.__log.warning("module %s not supported" % module)

		return out

	def download_sensor_modules(self, gateway, device):
		data = self.__client.sensors_info(gateway, device)

		out = []
		for sensor in data:
			out.append({
				'id': sensor['id'],
				'type_id': sensor['type_id']
			})

		return out

	def download_data(self, interval_before, interval_after, no_event_interval_before=1, no_event_interval_after=1):
		out_json = copy.deepcopy(self.__meta_data)
		w = WeatherData()

		for e in out_json:
			for key, dev in e['event']['devices'].items():
				for module in dev['modules']:
					e_start_before_timestamp = int(float(e['event']['start']) - interval_before)
					e_start_after_timestamp = int(float(e['event']['start']) + interval_after)
					e_end_before_timestamp = int(float(e['event']['end']) - interval_before)
					e_end_after_timestamp = int(float(e['event']['end']) + interval_after)

					module['measured_value_event_start'] = self.__client.history(
						dev['gateway'],
						dev['device'],
						module['id'],
						e_start_before_timestamp,
						e_start_after_timestamp
					)['data']

					module['measured_value_event_end'] = self.__client.history(
						dev['gateway'],
						dev['device'],
						module['id'],
						e_end_before_timestamp,
						e_end_after_timestamp
					)['data']

					module['weather_event_start'] = w.weather_data(e_start_before_timestamp, e_start_after_timestamp)
					module['weather_event_start'] = w.weather_data(e_end_before_timestamp, e_end_after_timestamp)

					no_e_start_before_timestamp = int(float(e['event']['start_no_event_time']) - no_event_interval_before)
					no_e_start_after_timestamp = int(float(e['event']['start_no_event_time']) + no_event_interval_after)
					no_e_end_before_timestamp = int(float(e['event']['end_no_event_time']) - no_event_interval_before)
					no_e_end_after_timestamp = int(float(e['event']['end_no_event_time']) + no_event_interval_after)

					module['measured_value_no_event_start'] = self.__client.history(
						dev['gateway'],
						dev['device'],
						module['id'],
						no_e_start_before_timestamp,
						no_e_start_after_timestamp
					)['data']

					module['measured_value_no_event_end'] = self.__client.history(
						dev['gateway'],
						dev['device'],
						module['id'],
						no_e_end_before_timestamp,
						no_e_end_after_timestamp
					)['data']

					module['weather_no_event_start'] = w.weather_data(no_e_start_before_timestamp, no_e_start_after_timestamp)
					module['weather_no_event_start'] = w.weather_data(no_e_end_before_timestamp, no_e_end_after_timestamp)

		return out_json

	def set_no_event_time(self, start_time, end_time):
		"""
		Vytvorenie casovej znacky, kde sa event nevyskytoval. Znacka sa vytvori pre zaciatok a
		koniec eventu osobitne. Hodnoty pre zaciatok a koniec eventu sa vypocitaju posunom
		o zadanu hodnotu dopredu (kladna hodnota) alebo dozadu (zaporna hodnota). Dopredu je
		mysleny cas, ktory je vacsi ako aktualny.
		"""

		for e in self.__meta_data:
			e['event']['start_no_event_time'] = e['event']['start'] + start_time
			e['event']['end_no_event_time'] = e['event']['end'] + end_time

	@property
	def meta_data(self):
		return self.__meta_data


class WeatherData:
	"""Weather data extraction."""

	def weather_data(self, start, end):
		day_time_start = datetime.datetime.fromtimestamp(start).strftime('%Y%m%d %H:%M:%S')
		day_start = day_time_start[:-9]
		day_time_end = datetime.datetime.fromtimestamp(end).strftime('%Y%m%d %H:%M:%S')
		day_end = day_time_end[:-9]

		url = 'https://api.weather.com/v1/geocode/49.15139008/16.69388962/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&startDate=' + str(day_start) + '&endDate=' + str(day_end)
		json_data = requests.get(url).text
		python_obj = json.loads(json_data)

		out_general = []
		for element in python_obj['observations']:
			out_general.append({
						'time': element['valid_time_gmt'],
						'temperature': element['temp'],
						'relative_humidity': element['rh'],
						'pressure': element['pressure'],
						'wind_speed': element['wspd']
					})

		generate_weather_data = self.__generate_weather_data(out_general)

		out_detailed = []
		for i in range(0, len(generate_weather_data)):
			if generate_weather_data[i]['time'] < start or generate_weather_data[i]['time'] > end:
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
				pressure_diff = pressure_end- pressure_start
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
					'time': int(out_general[i]['time']) + j,
					'temperature': temp,
					'relative_humidity': rh,
					'pressure': pressure,
					'wind_speed': wind_speed
				})
				temp = temp + temp_increase
				rh = rh + rh_increase
				pressure = pressure + pressure_increase
				wind_speed = wind_speed + wspd_increase
		return out_detailed


def main():
	beeeon_cl = BeeeOnClient("ant-work.fit.vutbr.cz", 8010)
	beeeon_cl.api_key = "thaegeshecaz1EN9lutho0laeku1ahsh9eec5waeg0aiqua2buo7ieyoo0Shoow9ahpoosomie0weiqu"
