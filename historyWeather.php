<?php

/**
 * https://www.wunderground.com/history/airport/LKTB/2018/5/10/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=
 */


function genDay($day)
{
	$json = array();
	$json['date'] = $day;
	$json['weather'] = array();

	$url = "https://www.wunderground.com/history/airport/LKTB/" . $day . "/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=";

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
	$html = curl_exec($ch);
	curl_close($ch);

	$dom = new DOMDocument();
	@$dom->loadHTML($html);

	foreach ($dom->getElementsByTagName('table') as $table) {
		if ($table->getAttribute("id") != "obsTable")
			continue;

		$header = true;
		foreach ($table->getElementsByTagName("tr") as $row) {
			if ($header) {
				$header = false;
				continue;
			}
			$allTD = $row->getElementsByTagName("td");

			$jsonRecord = array();
			$jsonRecord += ["Time" => date("G:i", strtotime($allTD->item(0)->nodeValue))];
			$jsonRecord += ["Temperature" => floatval(substr($allTD->item(1)->nodeValue, 0, -4))];
			$jsonRecord += ["DevPoint" => floatval(substr($allTD->item(2)->nodeValue, 0, -4))];
			$jsonRecord += ["Humidity" => floatval(substr($allTD->item(3)->nodeValue, 0, -1))];
			$jsonRecord += ["Pressure" => floatval(substr($allTD->item(4)->nodeValue, 0, -5))];
			$jsonRecord += ["Visibility" => floatval(substr($allTD->item(5)->nodeValue, 0, -4))];
			$jsonRecord += ["WindDirection" => $allTD->item(6)->nodeValue];
			$jsonRecord += ["WindSpeed" => floatval(substr(explode("/", $allTD->item(7)->nodeValue)[0], 0, -4))];
			$jsonRecord += ["GustSpeed" => (trim($allTD->item(8)->nodeValue) == "-") ? "" : $allTD->item(8)->nodeValue];
			$jsonRecord += ["Precip" => (trim($allTD->item(9)->nodeValue) == "-" || trim($allTD->item(9)->nodeValue) == "N/A") ? "" : $allTD->item(8)->nodeValue];
			$jsonRecord += ["Events" => trim($allTD->item(10)->nodeValue)];
			$jsonRecord += ["Conditions" => $allTD->item(11)->nodeValue];

			array_push($json['weather'], $jsonRecord);
		}
		break;
	}

	return $json;
}

$json['data'] = array();

// rok, mesiac, den
// je to interval typu: <x,y)
$begin = new DateTime('2018/5/10');
$end = new DateTime('2018/5/12');

$interval = DateInterval::createFromDateString('1 day');
$period = new DatePeriod($begin, $interval, $end);

foreach ($period as $dt) {
	array_push($json['data'], genDay($dt->format("Y/m/d")));
}

echo json_encode($json, JSON_PRETTY_PRINT);
