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
		'temp_in',
		'derivationTempIn_2point',
		'derivationTempIn_3point',

		'hum_in',
		'derivationHumIn_2point',
		'derivationHumIn_3point',


		'temp_out',
		'derivationTempOut_2point',
		'derivationTempOut_3point',

		'hum_out',
		'derivationHumOut_2point',
		'derivationHumOut_3point',

		'open_close',
	]
	writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

	writer.writeheader()

	for k in range(10, i):
		writer.writerow({
			'temp_in': tempIn[k],
			'derivationTempIn_2point': round((float(tempIn[k]) - float(tempIn[k-1]))/ (k - (k - 1)), 4),
			'derivationTempIn_3point': round((float(tempIn[k]) - float(tempIn[k-2]))/ (k - (k - 2)), 4),

			'hum_in': humIn[k],
			'derivationHumIn_2point': round((float(humIn[k]) - float(humIn[k-1]))/ (k - (k - 1)), 4),
			'derivationHumIn_3point': round((float(humIn[k]) - float(humIn[k-2]))/ (k - (k - 2)), 4),

			'temp_out': tempOut[k],
			'derivationTempOut_2point': round((float(tempOut[k]) - float(tempOut[k-1]))/ (k - (k - 1)), 4),
			'derivationTempOut_3point': round((float(tempOut[k]) - float(tempOut[k-2]))/ (k - (k - 2)), 4),

			'hum_out': humOut[k],
			'derivationHumOut_2point': round((float(humOut[k]) - float(humOut[k-1]))/ (k - (k - 1)), 4),
			'derivationHumOut_3point': round((float(humOut[k]) - float(humOut[k-2]))/ (k - (k - 2)), 4),

			'open_close': openClose[k],
		})
