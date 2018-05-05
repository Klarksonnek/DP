<?php

function findDev($devs, $id)
{
	foreach ($devs as $row) {
		if ($row['id'] == $id)
			return $row;
	}
}

function createOneHTMLContent($arr)
{
	$repr = "";
	$repr .= '<html><body>' . "\n";
	foreach ($arr as $row) {
		$repr .= '<iframe scrolling="no" width="920px" height="500px" src="';
		$repr .= $row ;
		$repr .= '"></iframe>' . "\n";
	}
	$repr .= '</body></html>';

	return $repr;
}

$RANGE = 300;
$INTERVAL = 30;
$NO_EVENT = 90;
$COUNT="2,2";
$HTML_ALL_FILE="all.html";
$OUTPUT_DIR = "generated/";

$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNTcwODA5MSwiaWF0IjoxNTI1MzYyNDkxLCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJlbiIsIm5iZiI6MTUyNTM2MjQ5MSwic3ViIjoiQnBDVCtjOWNSbCtndEg5clRKbG1HOWhWZGl2NWVFa0NqczlPcXVYc3NYMD0ifQ.5jCrB9HI0iggZn_w8PKM0-PoLceQPWyZZlX2HMo597s";


if (file_exists($OUTPUT_DIR)) {
	system("/bin/rm -rf ".escapeshellarg($OUTPUT_DIR));
	mkdir($OUTPUT_DIR);
}

$jsonFile = "events.json";
$jsonData = file_get_contents($jsonFile);

$arr = json_decode($jsonData, true); // true nemusi byt
//var_dump($arr);

$name = array();
foreach ($arr['events'] as $row) {
	echo $row['description'] . "\n";

	$dev = findDev($arr['devs'], $row['event'][1]['dev']);
	$event = $row['event'][1];

	$run = "/usr/bin/php data.php";
	$run .= " --gateway=" . $dev['gateway'];
	$run .= " --device=" . $dev['device'];
	$run .= " --sensor=" . $dev['sensor'];
	$run .= " --event=\"" . $event['open'] . "\"";
	$run .= " --range=" . $RANGE;
	$run .= " --interval=" . $INTERVAL;
	$run .= " --no-event=" . $NO_EVENT;
	$run .= " --count=" . $COUNT;
	$run .= " --access-token=" . $acc;

	//echo $run;
	$output = shell_exec($run);
	echo $output . "\n";
	echo "+++++++++++++++++++++++++++++++++++++++++++++\n";
}

$allHTMLFiles = preg_grep('~\.(html)$~', scandir($OUTPUT_DIR));

$file = fopen($OUTPUT_DIR . $HTML_ALL_FILE, "w");
fwrite($file, createOneHTMLContent(array_diff($allHTMLFiles, array($HTML_ALL_FILE))));
fclose($file);





