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
						found = True

				if not found:
					self.__log.warning("device %s not found, event was skipped" % key)

			self.__meta_data.insert(len(self.__meta_data), e)

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
					break

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

	def __convert(slef, data):
		out = []

		for event in data:
			ev = {
				'event_start': {
					'values': [],
					'weather': [],
				},
				#'event_end': {
				#	'values': [],
				#	'weather': [],
				#},
				'no_event_start': {
					'values': [],
					'weather': [],
				},
				#'no_event_end': {
				#	'values': [],
				#	'weather': [],
				#}
			}

			for k, device in event['event']['devices'].items():
				for module in device['modules']:
					ev['event_start']['weather'] = module['weather_event_start']
					ev['event_start']['values'].append(
						{
							'measured': module['measured_value_event_start'],
							'module_id': module['id'],
							'type_id': module['type_id'],
							'name': device['name'],
							'id': device['id'],
						}
					)

					#ev['event_end']['weather'] = module['weather_event_end']
					#ev['event_end']['values'].append(
					#	{
					#		'measured': module['measured_value_event_end'],
					#		'module_id': module['id'],
					#		'type_id': module['type_id'],
					#		'name': device['name'],
					#		'id': device['id']
					#	}
					#)

					ev['no_event_start']['weather'] = module['weather_no_event_start']
					ev['no_event_start']['values'].append(
						{
							'measured': module['measured_value_no_event_start'],
							'module_id': module['id'],
							'type_id': module['type_id'],
							'name': device['name'],
							'id': device['id']
						}
					)

					#ev['no_event_end']['weather'] = module['weather_no_event_end']
					#ev['no_event_end']['values'].append(
					#	{
					#		'measured': module['measured_value_no_event_end'],
					#		'module_id': module['id'],
					#		'type_id': module['type_id'],
					#		'name': device['name'],
					#		'id': device['id']
					#	}
					#)

			out.append(
				{
					'description': event['description'],
					'location': event['location'],
					'people': event['people'],
					'type': event['type'],
					'times': {
						#'event_end': event['event']['end'],
						#'no_event_end': event['event']['end_no_event_time'],
						'event_start': event['event']['start'],
						'no_event_start': event['event']['start_no_event_time']
					},
					'data': ev
				}
			)

		return out

	def download_data(self, shift_before, shift_after, no_event_shift_before=1, no_event_shift_after=1):
		out_json = copy.deepcopy(self.__meta_data)
		w = WeatherData()

		for e in out_json:
			for key, dev in e['event']['devices'].items():
				for module in dev['modules']:
					e_start_before_timestamp = int(float(e['event']['start']) - shift_before)
					e_start_after_timestamp = int(float(e['event']['start']) + shift_after)
					e_end_before_timestamp = int(float(e['event']['end']) - shift_before)
					e_end_after_timestamp = int(float(e['event']['end']) + shift_after)

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
					module['weather_event_end'] = w.weather_data(e_end_before_timestamp, e_end_after_timestamp)

					no_e_start_before_timestamp = int(float(e['event']['start_no_event_time']) - no_event_shift_before)
					no_e_start_after_timestamp = int(float(e['event']['start_no_event_time']) + no_event_shift_after)
					no_e_end_before_timestamp = int(float(e['event']['end_no_event_time']) - no_event_shift_before)
					no_e_end_after_timestamp = int(float(e['event']['end_no_event_time']) + no_event_shift_after)

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
					module['weather_no_event_end'] = w.weather_data(no_e_end_before_timestamp, no_e_end_after_timestamp)

		return self.__convert(out_json)

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

	def __switch_value(self, value):
		out = (int(float(value)))
		if out == 1:
			return str(0.0)
		return str(1.0)

	def ___find_min_max_timestamp(self, event, event_type):
		min_timestamp = None
		max_timestamp = None

		for item in event['data'][event_type]['values']:
			values_cnt = len(item['measured']) - 1
			if len(item['measured']) <= 1 or item['type_id'] == "open_close":
				continue
			if min_timestamp is None:
				min_timestamp = item['measured'][0]['at']
			if max_timestamp is None:
				max_timestamp = item['measured'][values_cnt]['at']
			elif item['measured'][0]['at'] > min_timestamp:
				min_timestamp = item['measured'][0]['at']
			elif item['measured'][values_cnt]['at'] < max_timestamp:
				max_timestamp = item['measured'][values_cnt]['at']

		return min_timestamp, max_timestamp

	def __generate_event_data(self, event, event_type):
		for item in event['data'][event_type]['values']:
			if len(item['measured']) <= 1:
				continue

			out = []
			for i in range(0, len(item['measured']) - 1):
				value_start = float(item['measured'][i]['value'])
				value_end = float(item['measured'][i + 1]['value'])
				if value_start - value_end == 0:
					value_increase = 0
				else:
					value_diff = value_end - value_start
					value_increase = value_diff / (item['measured'][i + 1]['at'] - item['measured'][i]['at'])

				value = value_start
				for j in range(0, item['measured'][i + 1]['at'] - item['measured'][i]['at']):
					out.append({
						"at": item['measured'][i]['at'] + j,
						"value": value
					})
					value = value + value_increase

			out.append({
				"at": item['measured'][len(item['measured']) - 1]['at'],
				"value": value
			})
			item['measured'] = out
		return event

	def __cut_event_data(self, event, min_timestamp, max_timestamp, event_type):
		for item in event['data'][event_type]['values']:
			measured_out = []
			if len(item['measured']) == 0 or (len(item['measured']) == 1 and item['type_id'] != "open_close"):
				continue
			if item['type_id'] == "open_close":
				switch = item['measured'][0]['at']
				orig_value = item['measured'][0]['value']
				do_switch = True
				new_value = 0
				for timestamp in range(min_timestamp, max_timestamp + 1):
					if switch > timestamp:
						if do_switch:
							new_value = self.__switch_value(orig_value)
							measured_out.append({
								"at": timestamp,
								"value": new_value
							})
							do_switch = False
						else:
							measured_out.append({
								"at": timestamp,
								"value": new_value
							})
					else:
						measured_out.append({
							"at": timestamp,
							"value": orig_value
						})

				item['measured'] = measured_out
				return event
			else:
				i = 0
				measured_out = []
				for timestamp in range(min_timestamp, max_timestamp + 1):
					if item['measured'][i]['at'] < timestamp or item['measured'][i]['at'] > timestamp:
						continue
					measured_out.append({
						"at": timestamp,
						"value": item['measured'][i]['value']
					})
					i = i + 1
				item['measured'] = measured_out
		return event

	def compute_event_data(self, data):
		event_type = ["event_start", "no_event_start"]
		new_event = []
		out = []

		for event in data:
			for j in range(0, len(event_type)):
				new_event = self.__generate_event_data(event, event_type[j])
				min_timestamp, max_timestamp = self.___find_min_max_timestamp(new_event, event_type[j])
				new_event = self.__cut_event_data(new_event, min_timestamp, max_timestamp, event_type[j])
			out.append(new_event)
		return out


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


class Graph:
	def __init__(self, output, data, path, same_scale=True, scale_padding_min=0, scale_padding_max=0):
		self.__output = output
		self.__data = data
		self.__same_scale = same_scale
		self.__scale_padding_min = scale_padding_min
		self.__scale_padding_max = scale_padding_max
		self.__path = path
		self.__data = data

	def gen(self):
		f = open(self.__output, 'w')

		f.write('<!DOCTYPE html>\n')
		f.write('<html>\n')
		f.write('	<head>\n')
		f.write('		<link href="' + self.__path + '/chart.css" rel="stylesheet">\n')
		f.write('		<script src="' + self.__path + '/jquery-3.2.1.slim.min.js"></script>\n')
		f.write('		<script src="' + self.__path + '/Chart.bundle.js"></script>\n')
		f.write('		<script src="' + self.__path + '/utils.js"></script>\n')
		f.write('	</head>\n')
		f.write('	<body>\n')

		for canvas_id, data in self.__data.items():
			f.write('		<div style="overflow: auto;">\n')
			f.write('			<canvas class="custom" id="g' + str(canvas_id) + '" width="900px" height="500"></canvas>\n')
			f.write('		</div>\n')

			all_min = None
			all_max = None
			for g in data['graphs']:
				numbers = list(map(int, g['values'].split(',')))

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

			all_min -= self.__scale_padding_min
			all_max += self.__scale_padding_max

			str_dataset = ""
			g_id = 0
			for g in data['graphs']:
				str_dataset += '						{\n'
				str_dataset += '							label: "' + g['label_x'] + '",\n'
				str_dataset += '							borderColor: "' + g['color'] + '",\n'
				str_dataset += '							backgroundColor: "' + g['color'] + '",\n'
				str_dataset += '							fill: false,\n'
				str_dataset += '							data: [' + g['values'] + '],\n'
				str_dataset += '							yAxisID: "y-axis-' + str(g_id) + '"\n'
				str_dataset += '						},\n'

			str_options = ""
			str_options += '							{\n'
			str_options += '								type: "linear",\n'
			str_options += '								display: true,\n'
			str_options += '								position: "left",\n'
			str_options += '								id: "y-axis-' + str(g_id) + '",\n'
			str_options += '								ticks: {\n'
			str_options += '									min: ' + str(all_min) + ',\n'
			str_options += '									max: ' + str(all_max) + '\n'
			str_options += '								}\n'
			str_options += '							},\n'

			f.write('		<script>\n')
			f.write('			var ctx = document.getElementById("g' + str(canvas_id) + '");\n')
			f.write('			var myChart1 = new Chart(ctx, {\n')
			f.write('				type: "line",\n')
			f.write('				data: {\n')
			f.write('					labels: [' + data['graphs'][0]['timestamps'] + '],\n')
			f.write('					datasets: [\n')
			f.write(str_dataset)
			f.write('					]\n')
			f.write('				},\n')
			f.write('				options: {\n')
			f.write('					responsive: false,\n')
			f.write('					hoverMode: "index",\n')
			f.write('					stacked: false,\n')
			f.write('					title: {\n')
			f.write('						display: true,\n')
			f.write('						text: "' + data['title'] + '"\n')
			f.write('					},\n')
			f.write('					scales: {\n')
			f.write('						yAxes: [\n')
			f.write(str_options)
			f.write('						]\n')
			f.write('					}\n')
			f.write('				}\n')
			f.write('			});\n')
			f.write('		</script>\n')

		f.write('	</body>\n')
		f.write('</html>\n')
		f.close()


class Differences:
	def __is_increasing(self, data):
		if data[0]['time'] < data[1]['time']:
			return True
		return False

	def __compute_differences_before(self, data, difference_interval):
		next_difference = float(data[0]['time'])
		interval = 0
		str_out = ""
		last_value = float(data[0]['value'])
		out = []

		for item in data:
			last_timestamp = float(item['time']) - 1
			new_value = (last_value + float(item['value'])) / 2.0

			if (next_difference - float(item['time'])) >= 0:
				new_difference = float(data[0]['value']) - new_value
				str_out += str(round(interval, 2)).rjust(3, ' ')
				str_out += " s, "
				str_out += "prumer v casech: "
				str_out += datetime.datetime.fromtimestamp(float(item['time'])).strftime('%H:%M:%S') + " "
				str_out += " - "
				str_out += datetime.datetime.fromtimestamp(last_timestamp).strftime('%H:%M:%S') + " "
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
				out.append({
					'time': item['time'],
					'difference': new_difference
				})
		return out

	def __compute_differences_after(self, data, difference_interval):
		next_difference = float(data[0]['time'])
		interval = 0
		str_out = ""
		last_value = float(data[0]['value'])
		out = []

		for item in data:
			last_timestamp = float(item['time']) + 1
			new_value = (last_value + float(item['value'])) / 2.0

			if (next_difference - float(item['time'])) <= 0:
				new_difference = new_value - float(data[0]['value'])
				str_out += str(round(interval, 2)).rjust(3, ' ')
				str_out += " s, "
				str_out += "prumer v casech: "
				str_out += datetime.datetime.fromtimestamp(float(item['time'])).strftime('%H:%M:%S') + " "
				str_out += " - "
				str_out += datetime.datetime.fromtimestamp(last_timestamp).strftime('%H:%M:%S') + " "
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
				out.append({
					'time': item['time'],
					'difference': new_difference
				})
		return out

	def compute_differences(self, data, difference_interval):
		if self.__is_increasing(data[:2]):
			return self.__compute_differences_after(data, difference_interval)
		return self.__compute_differences_before(data, difference_interval)


def main():
	w = WeatherData()
	#neděle 8. červenec 2018 20:30:00 - neděle 8. červenec 2018 21:00:00
	#print(w.weather_data(1531067400, 1531069200))

	#neděle 8. červenec 2018 20:15:00 - neděle 8. červenec 2018 20:45:00
	#print(w.weather_data(1531073700, 1531075500))

	#neděle 8. červenec 2018 23:57:00 - pondělí 9. červenec 2018 00:03:00
	#print(w.weather_data(1531087020, 1531087380))

	#neděle 8. červenec 2018 15:00:00 - neděle 8. červenec 2018 20:00:00
	#print(len(w.weather_data(1531054800, 1531072800)))

	data = [
		{
			'time': 1531224000,
			'value': 1492,
		},
		{
			'time': 1531224001,
			'value': 1485,
		},
		{
			'time': 1531224002,
			'value': 1479,
		},
		{
			'time': 1531224003,
			'value': 1487,
		},
		{
			'time': 1531224004,
			'value': 1498,
		},
		{
			'time': 1531224005,
			'value': 1497,
		},
		{
			'time': 1531224006,
			'value': 1495,
		},
		{
			'time': 1531224007,
			'value': 1493,
		},
		{
			'time': 1531224008,
			'value': 1495,
		},
		{
			'time': 1531224009,
			'value': 1496,
		},
		{
			'time': 1531224010,
			'value': 1502,
		}
	]

	d = Differences()
	data.reverse()
	d.compute_differences(data, 5)

	beeeon_cl = BeeeOnClient("ant-work.fit.vutbr.cz", 8010)
	beeeon_cl.api_key = "thaegeshecaz1EN9lutho0laeku1ahsh9eec5waeg0aiqua2buo7ieyoo0Shoow9ahpoosomie0weiqu"

	storage = DataStorage(beeeon_cl)
	storage.read_meta_data('devices.json', 'events.json')
	storage.set_no_event_time(10, 10)

	data = storage.download_data(10, 10)
	beeeon_cl.logout()

	print(json.dumps(data, indent=4, sort_keys=True))
	print(json.dumps(storage.compute_event_data(data), indent=4, sort_keys=True))


	data = {
		'g0': {
			'title': 'title',
			'graphs': [
				{
					'timestamps': '10, 11, 12',
					'values': '5, 20, 7',
					'label_x': 'x label',
					'color': 'red',
				},
				{
					'timestamps': '10, 11, 12',
					'values': '15, 16, 17',
					'label_x': 'x label 2',
					'color': 'blue',
				}
			]
		}
	}
	g = Graph('g.html', data, "./../src/graph", True, 2, 2)
	g.gen()
