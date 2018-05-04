<?php

$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNTcwODA5MSwiaWF0IjoxNTI1MzYyNDkxLCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJlbiIsIm5iZiI6MTUyNTM2MjQ5MSwic3ViIjoiQnBDVCtjOWNSbCtndEg5clRKbG1HOWhWZGl2NWVFa0NqczlPcXVYc3NYMD0ifQ.5jCrB9HI0iggZn_w8PKM0-PoLceQPWyZZlX2HMo597s";

class BeeeOnRest {
	private $url;
	private $port;

	public function __construct($url, $port)
	{
		$this->url = $url;
		$this->port = $port;
	}

	public function getSensorHistoryRange(
		$accessToken,
		$gatewayID,
		$deviceID,
		$sensorID,
		$from,
		$to,
		$interval = 1,
		$aggregation = "avg")
	{
		$endPoint = "";

		$endPoint .= "/gateways/";
		$endPoint .= $gatewayID;

		$endPoint .= "/devices/";
		$endPoint .= $deviceID;

		$endPoint .= "/sensors/";
		$endPoint .= $sensorID;

		$endPoint .= "/history";

		$request = "?range=". $from . "," . $to;
		$request .= "&interval=" . $interval;
		$request .= "&aggregation=" . $aggregation;

		return $this->post(
			$endPoint,
			$accessToken,
			$request);
	}

	private function post($endPoint, $accessToken, $data = "") {
		$ch = curl_init();

		$url = $this->url . ":" . $this->port;

		if (!empty($data))
			$endPoint .= $data;

		curl_setopt($ch, CURLOPT_URL, $url . $endPoint);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', 'Accept: application/json'));
		curl_setopt($ch, CURLOPT_VERBOSE, true);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array('Authorization: Bearer '. $accessToken));
		curl_setopt($ch, CURLINFO_HEADER_OUT, true);
		$data = json_decode(curl_exec($ch), true);

		$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		if($http_code != 200)
			throw new Exception('HTTP code: ' . $this->url . $endPoint);

		return $data;
	}
}

class GenerateHTMLGraph {
	static function gen($data)
	{

	}
}

class Util {
	public static function showLog($data)
	{
		echo $data;
	}

	/**
	 * Vygenerovanie rozsahu na zaklade zadaneho casu eventu.
	 */
	public static function calculateRange($eventTime, $range)
	{
		return array(
			"from" => $eventTime - $range,
			"to" => $eventTime + $range
		);
	}

	static function sortData($data)
	{
		usort($data['data'], function ($a, $b) {
			return $a['at'] <=> $b['at'];
		});

		return $data;
	}
}

class CustomException extends Exception {
	public $message;

	public function __construct($message) {
		$this->message = $message."\n";
	}

	/* Vypis chyby na stderr */
	public function printError() {
		fwrite(STDERR, $this->message);
	}
}

class Arguments {
	public $accessToken = null;
	public $gatewayID = null;
	public $deviceID = null;
	public $sensorID = null;
	public $from = null;
	public $event = null;
	public $interval = null;
	public $range = null;
	public $isHelp = false;

	const SHORT_OPTS = "a:g:d:s:e:i:r:h";
	const LONG_OPTS = array(
				"access-token:",
				"gateway:",
				"device:",
				"sensor:",
				"event:",
				"interval:",
				"range:",
				"help"
			);

	private function __construct()
	{
	}

	static public function helpMessage()
	{
		return "help";
	}

	public static function fromInput()
	{
		$args = new Arguments();

		$options = getopt(self::SHORT_OPTS, self::LONG_OPTS);

		foreach (self::LONG_OPTS as $value) {
			$firstChar = substr($value, 0, 1);
			$value = str_replace(":", "", $value);

			// Duplikacia prepinacov
			if (array_key_exists($value, $options) && array_key_exists($firstChar, $options))
				throw new CustomException("invalid input arguments");
			else {
				if (array_key_exists($firstChar, $options)) {
					$options[$value] = $options[$firstChar];
					unset($options[$firstChar]);
				}
			}
		}

		if (array_key_exists('help', $options)) {
			$args->isHelp = true;
			return $args;
		}

		if (!array_key_exists("gateway", $options))
			throw new CustomException("nebol zadany prepinac --gateway");
		else
			$args->gatewayID = $options['gateway'];

		if (!array_key_exists("device", $options))
			throw new CustomException("nebol zadany prepinac --device");
		else
			$args->deviceID = $options['device'];

		if (!array_key_exists("sensor", $options))
			throw new CustomException("nebol zadany prepinac --sensor");
		else
			$args->sensorID = $options['sensor'];

		if (!array_key_exists("event", $options))
			throw new CustomException("nebol zadany prepinac --event");
		else
			$args->event = $options['event'];

		if (!array_key_exists("range", $options))
			throw new CustomException("nebol zadany prepinac --range");
		else
			$args->range = $options['range'];

		if (!array_key_exists("interval", $options))
			throw new CustomException("nebol zadany prepinac --interval");
		else
			$args->interval = $options['interval'];

		var_dump($options);

		return $args;
	}
}

class Derivacie {
	/** @var Arguments */
	private $arguments;
	private $data;

	public function __construct($options, $data)
	{
		$this->arguments = $options;
		$this->data = $data;
	}

	public function prepare()
	{
		$before = $this->calculateDerBefore($this->data['data'], $this->arguments->event, $this->arguments->interval);
		Util::showLog("\n");
		$after = $this->calculateDerBefore($this->data['data'], $this->arguments->event, $this->arguments->interval);
		Util::showLog("-------------------------------------------\n");

		Util::showLog("nacitane data\n");
		foreach ($this->data['data'] as $row)
			echo date("H:i:s", $row['at']) ."   ".$row['value']. "\n";

		return array(
			"before" => $before,
			"after" => $after,
		);
	}

	/**
	 * Vypocet derivacii v case dozadu od zadanej udalosti.
	 * @param $values
	 * @param $eventTime timestamp, tkory obshauje cas udalosti.
	 * @param $interval cas jednotlivych derivacii
	 * @return array Pole zo zoznamom derivacii s danym intervalom, pre dany event.
	 */
	private function calculateDerBefore($values, $eventTime, $interval)
	{
		$lastValue = 0;
		$lastTimestamp = strtotime($eventTime);
		$showInterval = $interval;
		$derivacie = array();

		$nextDer = strtotime($eventTime) - $interval;

		// vyhladanie indexu vramci nacitanych udajov
		$index = 0;
		while ($index < count($values)) {
			if ($values[$index]['at'] >= strtotime($eventTime))
				break;

			$index++;
		}

		Util::showLog("derivacie v case dozadu: \n");
		$eventValue = $values[$index]['value'];
		for (; $index >=0; $index--) {
			if (($nextDer - $values[$index]['at']) >= 0) {
				$newValue = ($lastValue + $values[$index]['value']) / 2.0;
				$novaDerivacia = $eventValue - $newValue;

				$repr = "";
				$repr .= str_pad(round($showInterval, 2), 3, ' ', STR_PAD_LEFT);
				$repr .= " s, ";
				$repr .= "priemer v casoch: ";
				$repr .= date("H:i:s", $values[$index]['at']);
				$repr .= " - ";
				$repr .= date("H:i:s", $lastTimestamp);
				$repr .= str_pad(round($eventValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= " - ";
				$repr .= str_pad(round($lastValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= ", nova hodnota: ";
				$repr .= str_pad(round($newValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= ", derivacia: ";
				$repr .= str_pad(round($novaDerivacia, 2), 4, ' ', STR_PAD_LEFT);
				$repr .= "  ";
				if ($novaDerivacia == 0)
					$repr .= "-";
				else if ($novaDerivacia > 0)
					$repr .= "\u{2197}";
				else
					$repr .= "\u{2198}";
				$repr .= "\n";
				Util::showLog($repr);

				array_push($derivacie, $novaDerivacia);
				$nextDer -= $interval;
				$showInterval += $interval;
			}

			$lastValue = $values[$index]['value'];
			$lastTimestamp = $values[$index]['at'];
		}

		return $derivacie;
	}

	private function calculateDerAfter($values, $eventTime, $interval)
	{
		$derivacie = array();
		$lastValue = 0;
		$lastTimestamp = strtotime($eventTime);
		$showInterval = $interval;

		$nextDer = strtotime($eventTime) + $interval;

		// vyhladanie indexu vramci nacitanych udajov
		$index = 0;
		while ($index < count($values)) {
			if ($values[$index]['at'] >= strtotime($eventTime))
				break;

			$index++;
		}

		Util::showLog("derivacie v case dopredu: \n");
		$eventValue = $values[$index]['value'];
		for (; $index < count($values); $index++) {
			if (($nextDer - $values[$index]['at']) <= 0) {
				$newValue = ($lastValue + $values[$index]['value']) / 2.0;
				$novaDerivacia = $newValue - $eventValue;

				$repr = "";
				$repr .= str_pad(round($showInterval, 2), 3, ' ', STR_PAD_LEFT);
				$repr .= " s, ";
				$repr .= "priemer v casoch: ";
				$repr .= date("H:i:s", $lastTimestamp);
				$repr .= " - ";
				$repr .= date("H:i:s", $values[$index]['at']);
				$repr .= str_pad(round($lastValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= " - ";
				$repr .= str_pad(round($eventValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= ", nova hodnota: ";
				$repr .= str_pad(round($newValue, 2), 6, ' ', STR_PAD_LEFT);
				$repr .= ", derivacia: ";
				$repr .= str_pad(round($novaDerivacia, 2), 4, ' ', STR_PAD_LEFT);
				$repr .= "  ";
				if ($novaDerivacia == 0)
					$repr .= "-";
				else if ($novaDerivacia > 0)
					$repr .= "\u{2197}";
				else
					$repr .= "\u{2198}";

				$repr .= "\n";
				Util::showLog($repr);

				array_push($derivacie, $novaDerivacia);
				$nextDer += $interval;
				$showInterval += $interval;
			}

			$lastValue = $values[$index]['value'];
			$lastTimestamp = $values[$index]['at'];
		}

		return $derivacie;
	}
}

/**
 *
 */
$arguments = null;
try {
	$arguments = Arguments::fromInput();
}
catch (CustomException $ex) {
	fwrite(STDERR, $ex->printError());
	fwrite(STDERR, Arguments::helpMessage());
	return 1;
}

if ($arguments->isHelp) {
	echo $arguments->helpMessage() . "\n";
	return 0;
}

$rest = new BeeeOnRest("https://antwork.fit.vutbr.cz", "8010");
$range = Util::calculateRange(strtotime($arguments->event), $arguments->range);
$req = $rest->getSensorHistoryRange(
	$acc,
	$arguments->gatewayID,
	$arguments->deviceID,
	$arguments->sensorID,
	$range['from'],
	$range['to'],
	1
);

$req = Util::sortData($req);
$derivacie = new Derivacie($arguments, $req);

var_dump($derivacie->prepare());
