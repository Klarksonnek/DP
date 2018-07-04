import http.client
import json
import logging
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


def main():
	beeeon_cl = BeeeOnClient("ant-work.fit.vutbr.cz", 8010)
	beeeon_cl.api_key = "thaegeshecaz1EN9lutho0laeku1ahsh9eec5waeg0aiqua2buo7ieyoo0Shoow9ahpoosomie0weiqu"
