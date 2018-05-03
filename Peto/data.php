<?php

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


	/**
	 * Vypocet derivacii v case dozadu od zadanej udalosti.
	 * @param $values
	 * @param $eventTime timestamp, tkory obshauje cas udalosti.
	 * @param $interval cas jednotlivych derivacii
	 * @return array Pole zo zoznamom derivacii s danym intervalom, pre dany event.
	 */
	static function calculateDerBefore($values, $eventTime, $interval)
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

	static function calculateDerAfter($values, $eventTime, $interval)
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

	const SHORT_OPTS = "a:g:d:s:e:i:rh";
	const LONG_OPTS = array(
				"access-token:",
				"gateway:",
				"device:",
				"sensor:",
				"event:",
				"interval:",
				"range",
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
		$arguments = new Arguments();

		$options = getopt(self::SHORT_OPTS, self::LONG_OPTS);
		var_dump($options);

		foreach (self::LONG_OPTS as $value) {
			$firstChar = substr($value, 0, 1);
			$value = str_replace(":", "", $value);

			// Duplikace prepinacu
			if (array_key_exists($value, $options) && array_key_exists($firstChar, $options))
				throw new CustomException("Bad input arguments. Try --help.");
			else {
				if (array_key_exists($firstChar, $options)) {
					$options[$value] = $options[$firstChar];
					unset($options[$firstChar]);
				}
			}
		}

		var_dump($options);


		if (array_key_exists('help', $options)) {
			$arguments->isHelp = true;
			return $arguments;
		}

		if (count($options) < 5)
			throw new CustomException("neboli zadane spravne parametre");


		return $arguments;
	}
}



$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNTcwODA5MSwiaWF0IjoxNTI1MzYyNDkxLCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJlbiIsIm5iZiI6MTUyNTM2MjQ5MSwic3ViIjoiQnBDVCtjOWNSbCtndEg5clRKbG1HOWhWZGl2NWVFa0NqczlPcXVYc3NYMD0ifQ.5jCrB9HI0iggZn_w8PKM0-PoLceQPWyZZlX2HMo597s";

$rest = new BeeeOnRest("https://antwork.fit.vutbr.cz", "8010");


$rrr = Util::calculateRange(strtotime("04/15/2018 19:30:03"), 60);

$req = $rest->getSensorHistoryRange(
	$acc,
	"1936931389875594",
	"0xa900000000000002",
	"2",
	$rrr['from'],
	$rrr['to'],
	1
);

// sort array
usort($req['data'], function($a, $b) {
	$retval = $a['at'] <=> $b['at'];
	return $retval;
});


//Util::calculateDerBefore($req['data'], "04/15/2018 19:30:03", 20);
//Util::showLog("\n");
//Util::calculateDerAfter($req['data'], "04/15/2018 19:30:03", 20);
echo "-------\n";

foreach ($req['data'] as $row) {
	//var_dump($row);
	//echo date("H:i:s", $row['at']) ."   ".$row['value']. "\n";
}

$mnau = null;
try {
	$mnau = Arguments::fromInput();
}
catch (CustomException $ex) {
	echo $ex->printError();
	fwrite(STDERR, Arguments::helpMessage());
	return 1;
}

if ($mnau->isHelp) {
	echo $mnau->helpMessage() . "\n";
	return 0;
}
