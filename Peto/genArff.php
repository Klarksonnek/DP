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

$RANGE = 600;
$INTERVAL = 25;
$NO_EVENT = 100;
$COUNT="5,5";
$HTML_ALL_FILE="all.html";
$OUTPUT_DIR = "generated/";

$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNzU5MTQyOCwiaWF0IjoxNTI3MjQ1ODI4LCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJlbiIsIm5iZiI6MTUyNzI0NTgyOCwic3ViIjoiQnBDVCtjOWNSbCtndEg5clRKbG1HOWhWZGl2NWVFa0NqczlPcXVYc3NYMD0ifQ.nE6vlbCPc87fcgYgiOoU5IAmCB42hQ6Q7SnhpQOjOek";


if (file_exists($OUTPUT_DIR)) {
	system("/bin/rm -rf ".escapeshellarg($OUTPUT_DIR));
	mkdir($OUTPUT_DIR);
}
else {
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

	$run = "/usr/bin/php ../core.php";
	$run .= " --gateway=" . $dev['gateway'];
	$run .= " --device=" . $dev['device'];
	$run .= " --sensor=" . $dev['sensor'];
	$run .= " --event=\"" . $event['open'] . "\"";
	$run .= " --range=" . $RANGE;
	$run .= " --interval=" . $INTERVAL;
	$run .= " --no-event=" . $NO_EVENT;
	$run .= " --count=\"" . $COUNT . "\"";
	$run .= " --access-token=" . $acc;

	$output = shell_exec($run);
	echo $output . "\n";
	echo "+++++++++++++++++++++++++++++++++++++++++++++\n";
}

$allHTMLFiles = preg_grep('~\.(html)$~', scandir($OUTPUT_DIR));

$file = fopen($OUTPUT_DIR . $HTML_ALL_FILE, "w");
fwrite($file, createOneHTMLContent(array_diff($allHTMLFiles, array($HTML_ALL_FILE))));
fclose($file);


/**
 * Arff
 */
$allCSVFiles = preg_grep('~\.(csv)$~', scandir($OUTPUT_DIR));

$header = false;
$repr = "";
foreach ($allCSVFiles as $csvFile) {
	$csvData = array_map('str_getcsv', file($OUTPUT_DIR . "/" . $csvFile));

	if (!$header) {
		$repr = "@relation openEvent\n\n";

		// skip timestamp
		for ($i = 1; $i < count($csvData[0]); $i++) {

			if ($i != count($csvData[0]) - 1) {
				$repr .= "@attribute ";
				$repr .= $csvData[0][$i];
				$repr .= " numeric \n";
				continue;
			}

			$repr .= "@attribute class {yes, no}\n";
			$repr .= "\n";
			$repr .= "@data";
			$repr .= "\n";
			$repr .= "\n";
		}

		$header = true;
	}

	for ($i = 1; $i < count($csvData[1]); $i++) {
		$repr .= $csvData[1][$i] . ",";
	}
	$repr = substr($repr, 0, -1);
	$repr .= "\n";

	for ($i = 1; $i < count($csvData[2]); $i++) {
		$repr .= $csvData[2][$i] . ",";
	}
	$repr = substr($repr, 0, -1);
	$repr .= "\n";
}

$file = fopen("test.arff", "w");
fwrite($file, $repr);
fclose($file);

