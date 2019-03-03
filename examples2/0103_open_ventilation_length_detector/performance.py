from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
import csv


def table(length, true_5, bad_10_true_5, bad_25_true_5, true_10, bad_5_true_10, bad_25_true_10,
          true_25, bad_5_true_25, bad_10_true_25):
    uspesnost = round(((true_5 + true_10 + true_25) / length) * 100, 2)

    out = ''
    out += '-------------------------------------------------------------------------\n'
    out += '|records: {0:5}                                                         |\n'.format(length)
    out += '-------------------------------------------------------------------------\n'
    out += '|accuracy: {0:5}%                                                       |\n'.format(uspesnost)
    out += '-------------------------------------------------------------------------\n'
    out += '|                         | true 5         | true 10         | true 25            |\n'
    out += '-------------------------------------------------------------------------\n'
    out += '|prediction 5       |{0:20}  |{1:20}  |{2:20}  |\n'.format(true_5, bad_5_true_10, bad_5_true_25)
    out += '-------------------------------------------------------------------------\n'
    out += '|prediction 10          |{0:20}  |{1:20}  |{2:20}  |\n'.format(bad_10_true_5, true_10, bad_10_true_25)
    out += '-------------------------------------------------------------------------\n'
    out += '|prediction 25          |{0:20}  |{1:20}  |{2:20}  |\n'.format(bad_25_true_5, bad_25_true_10, true_25)
    out += '-------------------------------------------------------------------------\n'

    print(out)


if __name__ == '__main__':
    out = []

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

    table(
        len(out),
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
        if row['ventilation_length'] == row['prediction']:
            if row['ventilation_length'] == "'300'":
                true_5 += 1
            elif row['ventilation_length'] == "'600'":
                true_10 += 1
            elif row['ventilation_length'] == "'1500'":
                true_25 += 1
        elif row['ventilation_length'] == "'300'" and row['prediction'] == "'600'":
            true_5 += 1
        elif row['ventilation_length'] == "'600'" and row['prediction'] == "'300'":
            true_10 += 1
        elif row['ventilation_length'] == "'300'" and row['prediction'] == "'1500'":
            bad_25_true_5 += 1
        elif row['ventilation_length'] == "'600'" and row['prediction'] == "'1500'":
            bad_25_true_10 += 1
        elif row['ventilation_length'] == "'1500'" and row['prediction'] == "'300'":
            bad_5_true_25 += 1
        elif row['ventilation_length'] == "'1500'" and row['prediction'] == "'600'":
            bad_10_true_25 += 1

    table(
        len(out),
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
