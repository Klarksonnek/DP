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

$RANGE = 900;
$INTERVAL = 30;
$NO_EVENT = 100;
$PRECISION = 3;
$COUNT="3,3";
$HTML_ALL_FILE="all.html";
$OUTPUT_DIR = "generated/";

$colors = array(
	"window.chartColors.red",
	"window.chartColors.blue",
	"window.chartColors.green",
	"window.chartColors.grey",
);

$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNzkxODAzMSwiaWF0IjoxNTI3NTcyNDMxLCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJjcyIsIm5iZiI6MTUyNzU3MjQzMSwic3ViIjoid0JhQ2o3WEFTY2VMdFZDZFJ2cEk5bkdSSDgvUXRVeGduZWpVQWIyQUk0OD0ifQ.p5xNo19HjLeyh2ogS_X_qVsFBLznGV3tzClXf_n1nyk";

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

$name = array();
$number = 0;
foreach ($arr['events'] as $row) {
	echo $row['description'] . "\n";

	foreach ($row['event'] as $event) {
		if ($event['dev'] == "jablotron")
			continue;
		//if ($row['certainty'] != "1")
			//continue;

		$dev = findDev($arr['devs'], $event['dev']);

		$run = "/usr/bin/php ../core.php";
		$run .= " --gateway=" . $dev['gateway'];
		$run .= " --device=" . $dev['device'];
		$run .= " --sensor=" . $dev['sensor'];
		$run .= " --event=\"" . $event['open'] . "\"";
		$run .= " --range=" . $RANGE;
		$run .= " --interval=" . $INTERVAL;
		$run .= " --no-event=" . $NO_EVENT;
		$run .= " --count=\"" . $COUNT ."\"";
		$run .= " --file-suffix=\"" . $event['dev'] . "\"";
		$run .= " --file-prefix=\"" . str_pad($number, 4, "0", STR_PAD_LEFT) . "\"";
		$run .= " --graph-color=\"" . $colors[$number%4] . "\"";
		$run .= " --access-token=" . $acc;

		$output = shell_exec($run);
		echo $output . "\n";
		echo "+++++++++++++++++++++++++++++++++++++++++++++\n";
		$number++;
	}
}

$allHTMLFiles = preg_grep('~\.(html)$~', scandir($OUTPUT_DIR));

$file = fopen($OUTPUT_DIR . $HTML_ALL_FILE, "w");
fwrite($file, createOneHTMLContent(array_diff($allHTMLFiles, array($HTML_ALL_FILE))));
fclose($file);



/**
 * Arff
 */
$allCSVFiles = preg_grep('~\.(csv)$~', scandir($OUTPUT_DIR));

$repr = "";

/**
 * Header
 */

foreach ($allCSVFiles as $csvFile) {
	$csvData = array_map('str_getcsv', file($OUTPUT_DIR . "/" . $csvFile));

		$suffix = array(
			"inTemp",
			"inHum",
			"outTemp",
			"outHum",
		);

		$repr = "@relation openEvent\n\n";
		$repr .= "@attribute file string\n";

		foreach ($suffix as $suf) {
			// skip timestamp
			for ($i = 1; $i < count($csvData[0]); $i++) {
				if ($i != count($csvData[0]) - 1) {
					$repr .= "@attribute ";
					$repr .= $csvData[0][$i];
					$repr .= "_" . $suf;
					$repr .= " numeric \n";
					continue;
				}
			}
		}

	$repr .= "@attribute class {yes, no}\n";
	$repr .= "\n";
	$repr .= "@data";
	$repr .= "\n";
	$repr .= "\n";

}

$lastClass = "";
$count = 0;

foreach ($allCSVFiles as $csvFile) {
	$csvData = array_map('str_getcsv', file($OUTPUT_DIR . "/" . $csvFile));
	if ($count == 0)
		$repr .= $csvFile.",";
	//event
	for ($i = 1; $i < count($csvData[1]) - 1; $i++) {
		$repr .= round($csvData[1][$i], $PRECISION) . ",";
	}

	if ($count >= 3) {
		$repr .= $csvData[1][count($csvData[1])-1];
		$repr .= "\n";
		$count = 0;
		continue;
	}

	$count++;
}

$count = 0;
foreach ($allCSVFiles as $csvFile) {
	$csvData = array_map('str_getcsv', file($OUTPUT_DIR . "/" . $csvFile));
	if ($count == 0)
		$repr .= $csvFile.",";
	//no event
	for ($i = 1; $i < count($csvData[2]) - 1; $i++) {
		$repr .= round($csvData[2][$i], $PRECISION) . ",";
	}

	if ($count >= 3) {
		$repr .= $csvData[2][count($csvData[2])-1];
		$repr .= "\n";
		$count = 0;
		continue;
	}

	$count++;
}


$file = fopen("test.arff", "w");
fwrite($file, $repr);
fclose($file);
