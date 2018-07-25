<?php

require_once "../core.php";

$token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyODE5MzQ3MiwiaWF0IjoxNTI3ODQ3ODcyLCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJlbiIsIm5iZiI6MTUyNzg0Nzg3Miwic3ViIjoiQnBDVCtjOWNSbCtndEg5clRKbG1HOWhWZGl2NWVFa0NqczlPcXVYc3NYMD0ifQ.CpDnnEb6e-h3Hly6KHVCdTcc9BtHdly1GCM7xUvEvXI";


$begin = new DateTime('05/01/2018 00:00:00');
$end = new DateTime('06/04/2018 00:00:00');

$interval = DateInterval::createFromDateString('1 day');
$period = new DatePeriod($begin, $interval, $end);

$pocetDni = 0;
$rest = new BeeeOnRest("https://antwork.fit.vutbr.cz", "8010");
$predchadzajucaHodnota = NULL;
$count = 0;

foreach ($period as $dt) {
	if (is_null($predchadzajucaHodnota)) {
		$predchadzajucaHodnota = $dt;
		continue;
	}

	$req = $rest->getSensorHistoryRange(
		$token,
		"1816820318180747",
		"0xa9004a4a147d0001",
		"2",
		strtotime($predchadzajucaHodnota->format("m/d/Y H:i:s")),
		strtotime($dt->format("m/d/Y H:i:s")),
		1
	);

	echo $dt->format("m/d/Y H:i:s") . ": " . count($req['data']) . "\n";
	$pocetDni++;
	$predchadzajucaHodnota = $dt;
	$count += count($req['data']);
}

echo "Pocet dni: " . $pocetDni . "\n";
echo "Celkovy pocet udajov: $count\n";

echo "-------------------------------------------------------";
$pocetDni = 0;
$rest = new BeeeOnRest("https://antwork.fit.vutbr.cz", "8010");
$predchadzajucaHodnota = NULL;
$count = 0;

foreach ($period as $dt) {
	if (is_null($predchadzajucaHodnota)) {
		$predchadzajucaHodnota = $dt;
		continue;
	}

	$req = $rest->getSensorHistoryRange(
		$token,
		"1908402624139667",
		"0x900000000197053",
		"0",
		strtotime($predchadzajucaHodnota->format("m/d/Y H:i:s")),
		strtotime($dt->format("m/d/Y H:i:s")),
		1
	);

	echo $dt->format("m/d/Y H:i:s") . ": " . count($req['data']) . "\n";
	$pocetDni++;
	$predchadzajucaHodnota = $dt;
	$count += count($req['data']);
}

echo "Pocet dni: " . $pocetDni . "\n";
echo "Celkovy pocet udajov: $count\n";