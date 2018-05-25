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
$INTERVAL = 20;
$NO_EVENT = 20;
$COUNT="3,3";
$HTML_ALL_FILE="all.html";
$OUTPUT_DIR = "generated/";

$acc = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiQmVlZU9uIl0sImV4cCI6MTUyNzU5MDQyOSwiaWF0IjoxNTI3MjQ0ODI5LCJpc3MiOiJCZWVlT24iLCJsb2NhbGUiOiJjcyIsIm5iZiI6MTUyNzI0NDgyOSwic3ViIjoid0JhQ2o3WEFTY2VMdFZDZFJ2cEk5bkdSSDgvUXRVeGduZWpVQWIyQUk0OD0ifQ.hUrAhkytnPIbTwaYmpmXDrmEmP_I4e_DfoL7rrA9OD4";


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

	foreach ($row['event'] as $event) {
		if ($event['dev'] == "jablotron")
			continue;

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
		$run .= " --access-token=" . $acc;

		$output = shell_exec($run);
		echo $output . "\n";
		echo "+++++++++++++++++++++++++++++++++++++++++++++\n";
	}
}

$allHTMLFiles = preg_grep('~\.(html)$~', scandir($OUTPUT_DIR));

$file = fopen($OUTPUT_DIR . $HTML_ALL_FILE, "w");
fwrite($file, createOneHTMLContent(array_diff($allHTMLFiles, array($HTML_ALL_FILE))));
fclose($file);





