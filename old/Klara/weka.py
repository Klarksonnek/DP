#!/usr/bin/env python3

import csv

tempIn = {}
humIn = {}
tempOut = {}
humOut = {}
openClose = {}

i = 0
with open('report.csv', newline='') as csvFile:
	reader = csv.DictReader(csvFile)

	for row in reader:
		tempIn[i] = row['temp_in']
		humIn[i] = row['hum_in']
		tempOut[i] = row['temp_out']
		humOut[i] = row['hum_out']
		openClose[i] = row['open_close']
		i = i + 1

with open ('out.arff', 'w') as csvFile:
	fieldnames = [
		'derivationTempIn_2point',
		'derivationTempIn_3point',

		'derivationHumIn_2point',
		'derivationHumIn_3point',


		'derivationTempOut_2point',
		'derivationTempOut_3point',

		'derivationHumOut_2point',
		'derivationHumOut_3point',

		'open_close',
	]
	writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

	#writer.writeheader()

	for k in range(10, i):
		val = None
		if openClose[k] == '0':
			val ="c0"
		else:
			val = "c1"

		writer.writerow({
			'derivationTempIn_2point': round((float(tempIn[k]) - float(tempIn[k-1]))/ (k - (k - 1)), 4),
			'derivationTempIn_3point': round((float(tempIn[k]) - float(tempIn[k-2]))/ (k - (k - 2)), 4),


			'derivationHumIn_2point': round((float(humIn[k]) - float(humIn[k-1]))/ (k - (k - 1)), 4),
			'derivationHumIn_3point': round((float(humIn[k]) - float(humIn[k-2]))/ (k - (k - 2)), 4),


			'derivationTempOut_2point': round((float(tempOut[k]) - float(tempOut[k-1]))/ (k - (k - 1)), 4),
			'derivationTempOut_3point': round((float(tempOut[k]) - float(tempOut[k-2]))/ (k - (k - 2)), 4),


			'derivationHumOut_2point': round((float(humOut[k]) - float(humOut[k-1]))/ (k - (k - 1)), 4),
			'derivationHumOut_3point': round((float(humOut[k]) - float(humOut[k-2]))/ (k - (k - 2)), 4),

			'open_close': val,
		})
