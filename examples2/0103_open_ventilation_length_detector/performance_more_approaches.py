from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.ConnectionUtil import ConnectionUtil
from dm.DateTimeUtil import DateTimeUtil
from dm.GraphUtil import GraphUtil
import csv
import logging
import os
import time


processes = [
    '//Local Repository/processes/ventilation_prediction/predictor0',
    '//Local Repository/processes/ventilation_prediction/predictor1',
    '//Local Repository/processes/ventilation_prediction/predictor2',
    '//Local Repository/processes/ventilation_prediction/predictor3',
    '//Local Repository/processes/ventilation_prediction/predictor4',
    '//Local Repository/processes/ventilation_prediction/predictor5',
    '//Local Repository/processes/ventilation_prediction/predictor6',
]

OUTPUT_FILENAME = 'out.csv'
BEFORE_TIME = 10 * 60
AFTER_TIME = 10 * 60

def table(length, length_training, vent_5_min, vent_10_min, vent_25_min, true_5, bad_10_true_5, bad_25_true_5, true_10,
          bad_5_true_10, bad_25_true_10, true_25, bad_5_true_25, bad_10_true_25):
    uspesnost = round(((true_5 + true_10 + true_25) / length) * 100, 2)
    uspesnost_modified = round(((true_5 + true_10 + true_25 + (bad_10_true_5 / 2) + (bad_5_true_10 / 2)
                                 + (bad_10_true_25 / 2) + (bad_25_true_10 / 2)) / length) * 100, 2)

    out = ''
    out += '--------------------------------------------------------------------------\n'
    out += '|                         | 5 minutes    | 10 minutes     | 25 minutes   |\n'
    out += '--------------------------------------------------------------------------\n'
    out += '|training records: {0:5}  |{1:5}         |{2:5}           |{3:5}         |\n'.format(length_training,
                                                                                                 vent_5_min,
                                                                                                 vent_10_min,
                                                                                                 vent_25_min)
    out += '--------------------------------------------------------------------------\n'
    out += '|testing records:  {0:5}                                                 |\n'.format(length)
    out += '--------------------------------------------------------------------------\n'
    out += '|accuracy: {0:5}%                                                        |\n'.format(uspesnost)
    out += '--------------------------------------------------------------------------\n'
    out += '|modified accuracy: {0:5}%                                               |\n'.format(uspesnost_modified)
    out += '--------------------------------------------------------------------------\n'
    out += '|                         | true 5     | true 10     | true 25           |\n'
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 5             |{0:5}       |{1:5}        |{2:5}              |\n'.format(true_5,
                                                                                                 bad_5_true_10,
                                                                                                 bad_5_true_25)
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 10            |{0:5}       |{1:5}        |{2:5}              |\n'.format(bad_10_true_5,
                                                                                                 true_10,
                                                                                                 bad_10_true_25)
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 25            |{0:5}       |{1:5}        |{2:5}              |\n'.format(bad_25_true_5,
                                                                                                 bad_25_true_10,
                                                                                                 true_25)
    out += '--------------------------------------------------------------------------\n'

    print(out)

    return true_5 + true_10 + true_25, true_5 + true_10 + true_25 + (bad_10_true_5 / 2) + (bad_5_true_10 / 2) \
           + (bad_10_true_25 / 2) + (bad_25_true_10 / 2), length

   # GraphUtil.gen_stacked_bar_graph((true_5, bad_5_true_10, bad_5_true_25), (bad_10_true_5,
   # true_10, bad_10_true_25), (bad_25_true_5, bad_25_true_10, true_25))


def generate_row(str_process, performance, records, duration1, duration2):
    total = performance['nothing_as_true_nothing']
    total += performance['open_as_true_nothing']
    total += performance['nothing_as_true_open']
    total += performance['open_as_true_open']

    output = str_process
    output += '{0:6.2f}%   '.format(performance['accuracy'])
    output += '{0:7}    '.format(records)
    output += '{0:7} '.format(total)
    output += '{0:12}   '.format(performance['nothing_as_true_nothing'])
    output += '{0:13}   '.format(performance['open_as_true_nothing'])
    output += '{0:14}   '.format(performance['nothing_as_true_open'])
    output += '{0:13}'.format(performance['open_as_true_open'])

    if duration1 != '' and duration2 != '':
        output += '      {0}  {1}'.format(str(duration1)[:9], str(duration2)[:9])

    return output


from subprocess import PIPE, run
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('start')

    launcher = ConnectionUtil.rapid_miner()['launcher']

    true_list = []
    true_mod_list = []
    length_list = []

    for i in range(0, len(processes)):
        process = processes[i]
        out_name = 'out'+str(i)+'.csv'
        if os.path.isfile(out_name):
            os.remove(out_name)

        cmd = [
            launcher,
            process
        ]

        start_time = time.monotonic()
        result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        if os.path.isfile(out_name):
            out = []
            len_training = 0
            vent_5_min = 0
            vent_10_min = 0
            vent_25_min = 0

            with open('training'+str(i)+'.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    len_training += 1
                    if row['VentilationLength_event__'] == "'300'":
                        vent_5_min += 1
                    elif row['VentilationLength_event__'] == "'600'":
                        vent_10_min += 1
                    elif row['VentilationLength_event__'] == "'1500'":
                        vent_25_min += 1

            with open(out_name, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    record = {
                        'datetime': int(DateTimeUtil.local_time_str_to_utc(row['datetime']).timestamp()),
                        'readable': row['datetime'],
                        'ventilation_length': row['VentilationLength_event__'],
                        'prediction': row['prediction(VentilationLength_event__)'],
                    }

                    out.append(record)

            true_5 = 0
            bad_10_true_5 = 0
            bad_25_true_5 = 0
            true_10 = 0
            bad_5_true_10 = 0
            bad_25_true_10 = 0
            true_25 = 0
            bad_5_true_25 = 0
            bad_10_true_25 = 0
            for row in out:
                fail = True

                if row['ventilation_length'] == row['prediction']:
                    if row['ventilation_length'] == "'300'":
                        true_5 += 1
                    elif row['ventilation_length'] == "'600'":
                        true_10 += 1
                    elif row['ventilation_length'] == "'1500'":
                        true_25 += 1
                    else:
                        raise ValueError('chyba')
                else:
                    if row['ventilation_length'] == "'300'" and row['prediction'] == "'600'":
                        bad_10_true_5 += 1
                    elif row['ventilation_length'] == "'300'" and row['prediction'] == "'1500'":
                        bad_25_true_5 += 1
                    elif row['ventilation_length'] == "'600'" and row['prediction'] == "'300'":
                        bad_5_true_10 += 1
                    elif row['ventilation_length'] == "'600'" and row['prediction'] == "'1500'":
                        bad_25_true_10 += 1
                    elif row['ventilation_length'] == "'1500'" and row['prediction'] == "'300'":
                        bad_5_true_25 += 1
                    elif row['ventilation_length'] == "'1500'" and row['prediction'] == "'600'":
                        bad_10_true_25 += 1

            true, mod_true, length = table(
                len(out),
                len_training,
                vent_5_min,
                vent_10_min,
                vent_25_min,
                true_5,
                bad_10_true_5,
                bad_25_true_5,
                true_10,
                bad_5_true_10,
                bad_25_true_10,
                true_25,
                bad_5_true_25,
                bad_10_true_25
            )
            true_list.append(true)
            true_mod_list.append(mod_true)
            length_list.append(length)
        else:
            logging.error('chyba')

    GraphUtil.gen_grouped_barplot(true_list, true_mod_list, length_list, 'save', 'result.eps')

