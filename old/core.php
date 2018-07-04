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
		if($http_code != 200) {
			throw new Exception("HTTP code: $http_code, request: " . $this->url . $endPoint);
		}

		return $data;
	}
}

class GenerateHTMLGraph {
	static function gen($data, $title, $color = "window.chartColors.blue")
	{
		$timestamps = "";
		$values = "";
		foreach ($data['data'] as $row) {
			if (empty($row['value']))
				continue;

			$timestamps .= "\"". date("H:i:s", $row['at']) .'",';
			$values .= "\"" . $row['value'] . '",';
		}

		$repr = '
<!DOCTYPE html>
<html>
	<head>
		<link href="http://be.mienkofax.eu/css/chart.css" rel="stylesheet">
		<script src="http://be.mienkofax.eu/js/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
		
		
		<script src="http://www.chartjs.org/dist/2.7.2/Chart.bundle.js"></script>
		<script src="http://www.chartjs.org/samples/latest/utils.js"></script>
	</head>
	<body>
		<div style="overflow: auto;">
			<canvas class="custom" id="g1" width="900px" height="500"></canvas>
		</div>
		
		<script>
		var ctx = document.getElementById("g1");
		var myChart1 = new Chart(ctx, {
			type: "line",
			data: {
				labels: ['.$timestamps.'],
				datasets: [
					{
						label: "Value",
						borderColor: ' . $color . ',
						backgroundColor: ' . $color . ',
						fill: false,
						data: ['.$values.'],
						yAxisID: "y-axis-2"
					}
				]
			},
			options: {
				responsive: false,
				hoverMode: "index",
				stacked: false,
				title: {
					display: true,
					text: "'. $title .'"
				},
				scales: {
					yAxes: [
						{
							type: "linear",
							display: true,
							position: "left",
							id: "y-axis-2"
						}]
				}
			}
		});
	</script>
		

	</body>
</html>
';



		return $repr;
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
	public $noEvent = null;
	public $isHelp = false;
	public $count = null;
	public $fileSuffix = null;
	public $filePrefix = null;
	public $graphColor = null;

	const SHORT_OPTS = "a:g:d:s:e:i:r:n:c:f:p:g:h";
	const LONG_OPTS = array(
		"access-token:",
		"gateway:",
		"device:",
		"sensor:",
		"event:",
		"interval:",
		"range:",
		"no-event:",
		"count:",
		"file-suffix:",
		"file-prefix:",
		"graph-color:",
		"help"
	);

	private function __construct()
	{
	}

	static public function helpMessage()
	{
		$repr = "";
		$repr .= "Generovanie csv suborov s derivaciami:\n";
		$repr .= "[--help] - napoveda\n";
		$repr .= "[--access-token=\"xxx\"] - dostupne na: https://antwork.fit.vutbr.cz:8010/tester.html\n";
		$repr .= "[--gateway=1936931389875594] - identifikacia brany\n";
		$repr .= "[--device=0xa900000000000002] - identifikacia zariadenia\n";
		$repr .= "[--sensor=2] - identifikacia senzora 0,1,2,3,..\n";
		$repr .= "[--event=\"04/15/2018 19:30:03\"] - presny cas udalosti\n";
		$repr .= "[--range=60] - rozsah od udalosti dopredu a do zadu v case,\n";
		$repr .= "               pouzite pri pocitani derivacii\n";
		$repr .= "[--interval=20] - cas, po ktorom sa budu pocitat derivacie\n";
		$repr .= "[--no-event=20] - casovy posun od eventu dozadu, v ktorom \n";
		$repr .= "                  sa maju vypocitat hodnoty pre bod, v ktorom\n";
		$repr .= "                  nenastala udalost\n";
		$repr .= "[--count] - pocet derivacii pred a za udalostou\n";
		$repr .= "            dvojica oddelena ciarkou napr. \"2,2\"\n";
		$repr .= "[--file-suffix] - rozsireny nazov suboru (temp, hum, co2, ...)\n";
		$repr .= "[--file-prefix] - rozsireny nazov suboru (temp, hum, co2, ...)\n";
		$repr .= "[--graph-color] - farba grafu\n";

		$repr .= "\nJednotlive casy su uvedene v sekundach.\n";

		return $repr;
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

		if (!array_key_exists("no-event", $options))
			throw new CustomException("nebol zadany prepinac --no-event");
		else
			$args->noEvent = $options['no-event'];

		if (!array_key_exists("access-token", $options))
			throw new CustomException("nebol zadany prepinac --access-token");
		else
			$args->accessToken = $options['access-token'];

		if (!array_key_exists("count", $options))
			throw new CustomException("nebol zadany prepinac --count");
		else
			$args->count = explode(",", $options['count']);

		if (array_key_exists("file-suffix", $options))
			$args->fileSuffix = $options['file-suffix'];

		if (array_key_exists("file-prefix", $options))
			$args->filePrefix = $options['file-prefix'];

		if (array_key_exists("graph-color", $options))
			$args->graphColor = $options['graph-color'];

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

	public function prepare($event)
	{
		$before = $this->calculateDerBefore($this->data['data'], $event, $this->arguments->interval);
		Util::showLog("\n");
		$after = $this->calculateDerAfter($this->data['data'], $event, $this->arguments->interval);
		Util::showLog("-------------------------------------------\n");

		//Util::showLog("nacitane data\n");
		foreach ($this->data['data'] as $row) {
			if (empty($row['value']))
				continue;

			//echo date("H:i:s", $row['at']) . "   " . $row['value'] . "\n";
		}

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
		$lastTimestamp = $eventTime;
		$showInterval = $interval;
		$derivacie = array();
		$header = array();

		$nextDer = $eventTime - $interval;

		// vyhladanie indexu vramci nacitanych udajov
		$index = 0;
		while ($index < count($values)) {
			if ($values[$index]['at'] >= $eventTime)
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
				$repr .= str_pad(round($novaDerivacia, 2), 6, ' ', STR_PAD_LEFT);
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
				array_push($header, $showInterval);
				$nextDer -= $interval;
				$showInterval += $interval;
			}

			$lastValue = $values[$index]['value'];
			$lastTimestamp = $values[$index]['at'];
		}

		return array(
			"header" => $header,
			"values" =>$derivacie,
		);
	}

	private function calculateDerAfter($values, $eventTime, $interval)
	{
		$derivacie = array();
		$lastValue = 0;
		$lastTimestamp = $eventTime;
		$showInterval = $interval;
		$header = array();

		$nextDer = $eventTime + $interval;

		// vyhladanie indexu vramci nacitanych udajov
		$index = 0;
		while ($index < count($values)) {
			if ($values[$index]['at'] >= $eventTime)
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
				$repr .= str_pad(round($novaDerivacia, 2), 6, ' ', STR_PAD_LEFT);
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
				array_push($header, $showInterval);
				$nextDer += $interval;
				$showInterval += $interval;
			}

			$lastValue = $values[$index]['value'];
			$lastTimestamp = $values[$index]['at'];
		}

		return array(
			"header" => $header,
			"values" =>$derivacie,
		);
	}
}

/**
 *
 *
 *
 */
$arguments = null;
$OUTPUT_DIR = "generated/";
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

$rest = new BeeeOnRest("https://ant-work.fit.vutbr.cz", "8010");
$range = Util::calculateRange(strtotime($arguments->event), $arguments->range);
$req = $rest->getSensorHistoryRange(
	$arguments->accessToken,
	$arguments->gatewayID,
	$arguments->deviceID,
	$arguments->sensorID,
	$range['from'],
	$range['to'],
	1
);

$req = Util::sortData($req);
$derivacie = new Derivacie($arguments, $req);

Util::showLog("event: " . $arguments->event . "\n");
$derEvent = $derivacie->prepare(strtotime($arguments->event));

// vypocet udalosti predtym, ktora je posunuta o no-event hodnotu
$noEventValueTimestamp = 0;
{
	$eventIndex = 0;
	for (; $eventIndex < count($req['data']); $eventIndex++) {
		if ($req['data'][$eventIndex]['at'] == strtotime($arguments->event))
			break;
	}

	$tim = strtotime($arguments->event) - $arguments->noEvent;
	for ($i = $eventIndex; $i >= 0; $i--) {
		if ($req['data'][$i]['at'] <= $tim) {
			$noEventValueTimestamp = $req['data'][$i]['at'];
			break;
		}
	}

	Util::showLog("no-event: " . date("H:i:s", $noEventValueTimestamp) . "\n");
}

$derBeforeEvent = $derivacie->prepare($noEventValueTimestamp);

$filename = $arguments->event;
$filename = str_replace(" ", "-", $filename);
$filename = str_replace(":", "-", $filename);
$filename = str_replace("/", "-", $filename);

if (!is_null($arguments->fileSuffix))
	$filename .= "_" . $arguments->fileSuffix;

if (!is_null($arguments->filePrefix))
	$filename = $arguments->filePrefix . '_' . $filename;

$file = fopen($OUTPUT_DIR . $filename . ".html", "w");

if (!is_null($arguments->graphColor))
	fwrite($file, GenerateHTMLGraph::gen($req, "Event: " . $arguments->event . ", " . $arguments->fileSuffix, $arguments->graphColor));
else
	fwrite($file, GenerateHTMLGraph::gen($req, "Event: " . $arguments->event . ", " . $arguments->fileSuffix));

fclose($file);


/**
 * CSV file
 */
$derBeforeCount = min(
	count($derEvent['before']['header']),
	count($derBeforeEvent['before']['header'])
);

$derAfterCount = min(
	count($derEvent['after']['header']),
	count($derBeforeEvent['after']['header'])
);

$CSVContent = "timestamp";
for ($i = 0; $i < $derBeforeCount && $i < $arguments->count[0]; $i++)
	$CSVContent .= ",before_".$derEvent['before']['header'][$i];

for ($i = 0; $i < $derAfterCount && $i < $arguments->count[1]; $i++)
	$CSVContent .= ",after_".$derEvent['after']['header'][$i];
$CSVContent .= ",event";
$CSVContent .= "\n";

{
	if ($derBeforeCount < $arguments->count[0]) {
		throw new CustomException(
			"bol zadany mensi pocet derivacii (pred), nez sa ich vypocitalo");
	}

	if ($derAfterCount < $arguments->count[1]) {
		throw new CustomException(
			"bol zadany mensi pocet derivacii (po), nez sa ich vypocitalo");
	}
}

// event
$CSVContent .= strtotime($arguments->event);
for ($i = 0; $i < $derBeforeCount && $i < $arguments->count[0]; $i++)
	$CSVContent .= "," . $derEvent['before']['values'][$i];

for ($i = 0; $i < $derAfterCount && $i < $arguments->count[1]; $i++)
	$CSVContent .= "," . $derEvent['after']['values'][$i];
$CSVContent .= ",yes";
$CSVContent .= "\n";

// hodnota pred eventom
$CSVContent .= $noEventValueTimestamp;
for ($i = 0; $i < $derAfterCount && $i < $arguments->count[0]; $i++)
	$CSVContent .= "," . $derBeforeEvent['before']['values'][$i];

for ($i = 0; $i < $derAfterCount && $i < $arguments->count[1]; $i++)
	$CSVContent .= "," . $derBeforeEvent['after']['values'][$i];
$CSVContent .= ",no";
$CSVContent .= "\n";

$file = fopen($OUTPUT_DIR . $filename . ".csv", "w");
fwrite($file, $CSVContent);
fclose($file);
