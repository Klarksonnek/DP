import csv
import logging
from dm.CSVUtil import CSVUtil
import csv
import math

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    data = []

    with open('tmp_one.csv') as f1:
        csv_reader = csv.DictReader(f1, delimiter=';')
        for row in csv_reader:
            try:
                data.append({
                    'value': float(row['hodnota']),
                    'class': row['event'],
                })
            except:
                continue

    out = []
    data = data[:10]
    data = sorted(data, key = lambda k:k['value'])
    values = []
    triedy = []
    for item in data:
        values.append(item['value'])
        triedy.append(item['class'])

    for k in range(0, len(values) - 1):
        print('{0} - {1} = {2}'.format(values[k], values[k + 1], (values[k] + values[k + 1])/2))
        splitpoint = (values[k] + values[k + 1])/2

        mensie = []
        mensie_open = 0
        mensie_nothing = 0

        vacsie = []
        vacsie_open = 0
        vacsie_nothing = 0

        for m in range(0, len(values)):
            if values[m] <= splitpoint:
                mensie.append(values[m])

                if triedy[m] == 'open':
                    mensie_open += 1
                else:
                    mensie_nothing += 1
            else:
                vacsie.append(values[m])

                if triedy[m] == 'open':
                    vacsie_open += 1
                else:
                    vacsie_nothing += 1

        infoS_mensie = 0
        for j in range(0, len(values)):
            tmp = 0

            pi = mensie_open / len(mensie)
            if pi != 0.0:
                tmp = pi * math.log2(pi)

            pi = mensie_nothing / len(mensie)
            if pi != 0.0:
                tmp += pi * math.log2(pi)

            infoS_mensie = -tmp

        infoS_vacsie = 0
        for j in range(0, len(values)):
            tmp = 0

            pi = vacsie_open / len(vacsie)
            if pi != 0.0:
                tmp = pi * math.log2(pi)

            pi = vacsie_nothing / len(vacsie)
            if pi != 0.0:
                tmp += pi * math.log2(pi)

            infoS_vacsie = -tmp

        infoA = len(mensie) / len(values) * infoS_mensie
        infoA += len(vacsie) / len(values) * infoS_vacsie


        out.append({
            'split': splitpoint,
            'infoA': infoA,
        })

    out = sorted(out, key=lambda k: k['split'])
    for row in out:
        print('{0:7.3f}, {1}'.format(row['split'], row['infoA']))

    print(values)
