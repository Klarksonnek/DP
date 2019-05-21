"""

"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.DateTimeUtil import DateTimeUtil
import csv

__author__ = ''
__email__ = ''


def table(length, length_training, vent_5_min, vent_10_min, vent_15_min, true_5, bad_10_true_5, bad_15_true_5, true_10,
          bad_5_true_10, bad_15_true_10, true_15, bad_5_true_15, bad_10_true_15):
    uspesnost = round(((true_5 + true_10 + true_15) / length) * 100, 2)

    out = ''
    out += '--------------------------------------------------------------------------\n'
    out += '|                         | 5 minutes    | 10 minutes     | 15 minutes   |\n'
    out += '--------------------------------------------------------------------------\n'
    out += '|training records: {0:5}  |{1:5}         |{2:5}           |{3:5}         |\n'.format(length_training,
                                                                                                 vent_5_min,
                                                                                                 vent_10_min,
                                                                                                 vent_15_min)
    out += '--------------------------------------------------------------------------\n'
    out += '|testing records:  {0:5}                                                 |\n'.format(length)
    out += '--------------------------------------------------------------------------\n'
    out += '|accuracy: {0:5}%                                                        |\n'.format(uspesnost)
    out += '--------------------------------------------------------------------------\n'
    out += '|                         | true 5     | true 10     | true 15           |\n'
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 5             |{0:5}       |{1:5}        |{2:5}              |\n'.format(true_5,
                                                                                                 bad_5_true_10,
                                                                                                 bad_5_true_15)
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 10            |{0:5}       |{1:5}        |{2:5}              |\n'.format(bad_10_true_5,
                                                                                                 true_10,
                                                                                                 bad_10_true_15)
    out += '--------------------------------------------------------------------------\n'
    out += '|prediction 15            |{0:5}       |{1:5}        |{2:5}              |\n'.format(bad_15_true_5,
                                                                                                 bad_15_true_10,
                                                                                                 true_15)
    out += '--------------------------------------------------------------------------\n'

    print(out)


if __name__ == '__main__':
    out = []

    len_training = 0
    vent_5_min = 0
    vent_10_min = 0
    vent_15_min = 0

    with open('training.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            len_training += 1
            if row['VentilationLength_event__'] == "'300'":
                vent_5_min += 1
            elif row['VentilationLength_event__'] == "'600'":
                vent_10_min += 1
            elif row['VentilationLength_event__'] == "'900'":
                vent_15_min += 1

    with open('out.csv', mode='r') as csv_file:
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
    bad_15_true_5 = 0
    true_10 = 0
    bad_5_true_10 = 0
    bad_15_true_10 = 0
    true_15 = 0
    bad_5_true_15 = 0
    bad_10_true_15 = 0
    for row in out:
        fail = True

        if row['ventilation_length'] == row['prediction']:
            if row['ventilation_length'] == "'300'":
                true_5 += 1
            elif row['ventilation_length'] == "'600'":
                true_10 += 1
            elif row['ventilation_length'] == "'900'":
                true_15 += 1
            else:
                raise ValueError('chyba')
        else:
            if row['ventilation_length'] == "'300'" and row['prediction'] == "'600'":
                bad_10_true_5 += 1
            elif row['ventilation_length'] == "'300'" and row['prediction'] == "'900'":
                bad_15_true_5 += 1
            elif row['ventilation_length'] == "'600'" and row['prediction'] == "'300'":
                bad_5_true_10 += 1
            elif row['ventilation_length'] == "'600'" and row['prediction'] == "'900'":
                bad_15_true_10 += 1
            elif row['ventilation_length'] == "'900'" and row['prediction'] == "'300'":
                bad_5_true_15 += 1
            elif row['ventilation_length'] == "'900'" and row['prediction'] == "'600'":
                bad_10_true_15 += 1

    table(
        len(out),
        len_training,
        vent_5_min,
        vent_10_min,
        vent_15_min,
        true_5,
        bad_10_true_5,
        bad_15_true_5,
        true_10,
        bad_5_true_10,
        bad_15_true_10,
        true_15,
        bad_5_true_15,
        bad_10_true_15
    )

    true_5 = 0
    bad_10_true_5 = 0
    bad_15_true_5 = 0
    true_10 = 0
    bad_5_true_10 = 0
    bad_15_true_10 = 0
    true_15 = 0
    bad_5_true_15 = 0
    bad_10_true_15 = 0
    for row in out:
        if row['ventilation_length'] == row['prediction']:
            if row['ventilation_length'] == "'300'":
                true_5 += 1
            elif row['ventilation_length'] == "'600'":
                true_10 += 1
            elif row['ventilation_length'] == "'900'":
                true_15 += 1
        elif row['ventilation_length'] == "'600'" and row['prediction'] == "'900'":
            true_10 += 1
        elif row['ventilation_length'] == "'900'" and row['prediction'] == "'600'":
            true_15 += 1
        elif row['ventilation_length'] == "'300'" and row['prediction'] == "'900'":
            bad_15_true_5 += 1
        elif row['ventilation_length'] == "'300'" and row['prediction'] == "'600'":
            bad_10_true_5 += 1
        elif row['ventilation_length'] == "'600'" and row['prediction'] == "'300'":
            bad_5_true_10 += 1
        elif row['ventilation_length'] == "'900'" and row['prediction'] == "'300'":
            bad_5_true_15 += 1

    table(
        len(out),
        len_training,
        vent_5_min,
        vent_10_min,
        vent_15_min,
        true_5,
        bad_10_true_5,
        bad_15_true_5,
        true_10,
        bad_5_true_10,
        bad_15_true_10,
        true_15,
        bad_5_true_15,
        bad_10_true_15
    )
