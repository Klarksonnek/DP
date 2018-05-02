#!/usr/bin/env python3

import csv

co2 = {}
open_close = [
0,0,0,0,0,0,0,0,0,0,0,0,0,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
]

i = 0
with open('report.csv', newline='') as csvFile:
	reader = csv.DictReader(csvFile)

	for row in reader:
		co2[i] = row['co2']
		i = i + 1

with open ('out.arff', 'w') as csvFile:
	fieldnames = [
		#'co2',
		'derivationCO2_2point',
		'derivationCO2_3point',
		'derivationCO2_4point',
		'open_close',
	]
	writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

	#writer.writeheader()

	for k in range(10, i):
		val = None
		if open_close[k] == 0:
			val ="yes"
		else:
			val = "no"


		writer.writerow({
		#	'co2': co2[k],
			'derivationCO2_2point': round((float(co2[k]) - float(co2[k-1]))/ (k - (k - 1)), 4),
			'derivationCO2_3point': round((float(co2[k]) - float(co2[k-2]))/ (k - (k - 2)), 4),
			'derivationCO2_4point': round((float(co2[k]) - float(co2[k-2]))/ (k - (k - 3)), 4),
			'open_close': val
		})
