from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
import csv


def table(length, true_nothing, bad_true_nothing, true_open, bad_true_open, event_type):
    uspesnost = round(((true_nothing + true_open) / length) * 100, 2)

    if event_type == 'open':
        event_type = ' ' + event_type

    out = ''
    out += '-------------------------------------------------------------------------\n'
    out += '|records: {0:5}                                                         |\n'.format(length)
    out += '-------------------------------------------------------------------------\n'
    out += '|accuracy: {0:5}%                                                       |\n'.format(uspesnost)
    out += '-------------------------------------------------------------------------\n'
    out += '|                         | true nothing         | true {0}           |\n'.format(event_type)
    out += '-------------------------------------------------------------------------\n'
    out += '|prediction nothing       |{0:20}  |{1:20}  |\n'.format(true_nothing, bad_true_nothing)
    out += '-------------------------------------------------------------------------\n'
    out += '|prediction {0}         |{1:20}  |{2:20}  |\n'.format(event_type, bad_true_open, true_open)
    out += '-------------------------------------------------------------------------\n'

    print(out)


OUTPUT_FILENAME = '0202_open_detector/out.csv'
BEFORE_TIME = 2 * 60
AFTER_TIME = 3 * 60

if __name__ == '__main__':
    out = []

    intervals = []
    event_type = None
    event_types = {}

    with open(OUTPUT_FILENAME, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            record = {
                'datetime': int(DateTimeUtil.local_time_str_to_utc(row['datetime']).timestamp()),
                'readable': row['datetime'],
                'event': row['event'],
                'prediction': row['prediction(event)'],
            }

            out.append(record)
            event_types[row['event']] = None

    if len(event_types) == 2:
        if 'open' in event_types and 'nothing' in event_types:
            event_type = 'open'
        elif 'close' in event_types and 'nothing' in event_types:
            event_type = 'close'
        else:
            raise ValueError('%s must contains only 2 type of event column')
    else:
        raise ValueError('%s must contains only 2 type of event column')

    for row in out:
        if row['event'] == event_type:
            t = row['datetime']
            intervals.append((t - BEFORE_TIME, t, t + AFTER_TIME))

    true_nothing = 0
    bad_true_nothing = 0
    true_open = 0
    bad_true_open = 0
    for row in out:
        fail = True

        if row['event'] == row['prediction']:
            if row['event'] == event_type:
                true_open += 1
            elif row['event'] == 'nothing':
                true_nothing += 1
            else:
                raise ValueError('chyba')
        else:
            if row['event'] == 'nothing' and row['prediction'] == event_type:
                bad_true_nothing += 1
            else:
                bad_true_open += 1

    table(
        len(out),
        true_nothing,
        bad_true_open,
        true_open,
        bad_true_nothing,
        event_type
    )

    true_nothing = 0
    bad_true_nothing = 0
    true_open = 0
    bad_true_open = 0
    extended = {}
    for row in intervals:
        extended[row[1]] = []

    for row in out:
        found = False
        for interval in intervals:
            if interval[0] < row['datetime'] < interval[2]:
                extended[interval[1]].append(row['prediction'])
                found = True

        if not found:
            if row['event'] == row['prediction']:
                if row['event'] == event_type:
                    true_open += 1
                elif row['event'] == 'nothing':
                    true_nothing += 1
                else:
                    raise ValueError('chyba')
            else:
                if row['event'] == 'nothing' and row['prediction'] == event_type:
                    bad_true_nothing += 1
                else:
                    bad_true_open += 1

    for _, interval in extended.items():
        found = False
        for row in interval:

            if row == event_type:
                found = True
                break

        if not found:
            bad_true_open += 1
        else:
            true_open += 1

        true_nothing += len(interval) - 1

    table(
        len(out),
        true_nothing,
        bad_true_open,
        true_open,
        bad_true_nothing,
        event_type
    )
