"""Calculated accuracy using standard approach and accuracy considering a tolerance interval.
"""
from dm.DateTimeUtil import DateTimeUtil
import csv

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


def count(z, val):
    return len([i for i, x in enumerate(z) if x == val])


class Performance:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = []
        self.count = 0
        self.__event_type = None

    def __read(self):
        event_types = {}

        with open(self.__filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                record = {
                    'datetime': int(DateTimeUtil.local_time_str_to_utc(row['datetime']).timestamp()),
                    'readable': row['datetime'],
                    'event': row['event'],
                    'prediction': row['prediction(event)'],
                    'valid': row['valid']
                }

                if record['prediction'] == '':
                    record['valid'] = 'no'

                if row['valid'] == 'no':
                    self.count -= 1

                if record['prediction'] == '' and record['event'] == 'nothing':
                    continue

                self.__data.append(record)
                event_types[row['event']] = None

        self.count += len(self.__data)

        if len(event_types) == 2:
            if 'open' in event_types and 'nothing' in event_types:
                self.__event_type = 'open'
            elif 'close' in event_types and 'nothing' in event_types:
                self.__event_type = 'close'
            else:
                raise ValueError('%s must contains only 2 types of event column')
        elif len(event_types) == 1 and 'nothing' in event_types:
            self.__event_type = 'open'
        else:
            raise ValueError('%s must contains only 2 types of event column')

    def __simple_table(self, res):
        if self.__event_type == 'open':
            event_type = ' ' + self.__event_type
        else:
            event_type = self.__event_type

        out = ''
        out += '-------------------------------------------------------------------------\n'
        out += '|records: {0:6}                                                        |\n'.format(res['records'])
        out += '-------------------------------------------------------------------------\n'
        out += '|accuracy: {0:6.2f}%                                                      |\n'.format(res['accuracy'])
        out += '-------------------------------------------------------------------------\n'
        out += '|                         | true nothing         | true {0}           |\n'.format(event_type)
        out += '-------------------------------------------------------------------------\n'
        out += '|prediction nothing       |{0:20}  |{1:20}  |\n'.format(res['nothing_as_true_nothing'], res['nothing_as_true_open'])
        out += '-------------------------------------------------------------------------\n'
        out += '|prediction {0}         |{1:20}  |{2:20}  |\n'.format(event_type, res['open_as_true_nothing'], res['open_as_true_open'])
        out += '-------------------------------------------------------------------------\n'
        return out

    def simple(self):
        nothing_as_true_nothing = 0
        open_as_true_nothing = 0
        open_as_true_open = 0
        nothing_as_true_open = 0
        wrong_prediction = []

        if self.__data == []:
            self.__read()

        for row in self.__data:
            if row['valid'] == 'no':
                continue

            if row['event'] == row['prediction']:
                if row['event'] == self.__event_type:
                    open_as_true_open += 1
                elif row['event'] == 'nothing':
                    nothing_as_true_nothing += 1
                else:
                    raise ValueError('error')
            else:
                if row['event'] == 'nothing' and row['prediction'] == self.__event_type:
                    open_as_true_nothing += 1

                    if row['event'] != self.__event_type:
                        wrong_prediction.append(row['readable'])
                elif row['prediction'] != '':
                    nothing_as_true_open += 1

        res = {
            'records': self.count,
            'accuracy': round(((nothing_as_true_nothing + open_as_true_open) / self.count) * 100, 2),
            'nothing_as_true_nothing': nothing_as_true_nothing,
            'open_as_true_nothing': open_as_true_nothing,
            'open_as_true_open': open_as_true_open,
            'nothing_as_true_open': nothing_as_true_open,
        }
        res['sum'] = res['nothing_as_true_nothing'] + res['open_as_true_nothing'] + res['open_as_true_open'] \
                     + res['nothing_as_true_open']

        return self.__simple_table(res), wrong_prediction, res

    def with_delay(self, before, after):
        nothing_as_true_nothing = 0
        open_as_true_nothing = 0
        open_as_true_open = 0
        nothing_as_true_open = 0
        extended = {}
        invalid = {}
        wrong_prediction = []

        if self.__data == []:
            self.__read()

        intervals = []
        for row in self.__data:
            if row['event'] == self.__event_type:
                t = row['datetime']
                intervals.append((t - before, t, t + after))

        intervals.sort()
        for i in range(1, len(intervals)):
            if intervals[i - 1][2] > intervals[i][0]:
                t1 = DateTimeUtil.utc_timestamp_to_str(intervals[i - 1][1], '%d.%m. %H:%M:%S')
                t2 = DateTimeUtil.utc_timestamp_to_str(intervals[i][1], '%d.%m. %H:%M:%S')
                print('prekryvajuce sa intervaly {0} a {1}'.format(t1, t2))

        for row in intervals:
            extended[row[1]] = []
            invalid[row[1]] = []

        for row in self.__data:
            found = False
            for interval in intervals:
                if interval[0] < row['datetime'] < interval[2]:
                    extended[interval[1]].append(row['prediction'])
                    invalid[interval[1]].append(row['valid'])
                    found = True

            if found or row['valid'] == 'no':
                continue

            if row['event'] == row['prediction']:
                if row['event'] == self.__event_type:
                    open_as_true_open += 1
                elif row['event'] == 'nothing':
                    nothing_as_true_nothing += 1
                else:
                    raise ValueError('error')
            else:
                if row['event'] == 'nothing' and row['prediction'] == self.__event_type:
                    open_as_true_nothing += 1

                    if row['event'] != self.__event_type:
                        wrong_prediction.append(row['readable'])
                elif row['prediction'] != '':
                    nothing_as_true_open += 1

        for key, interval in extended.items():
            if len(interval) == 1 and 'no' in invalid[key]:
                continue

            found = False
            for k in range(0, len(interval)):
                row = interval[k]
                if row == self.__event_type:
                    found = True
                    break

            if found:
                if 'no' not in invalid[key]:
                    open_as_true_open += 1
            else:
                if 'no' not in invalid[key]:
                    nothing_as_true_open += 1

            nothing_as_true_nothing += len(interval) - 1

        res = {
            'records': self.count,
            'accuracy': round(((nothing_as_true_nothing + open_as_true_open) / self.count) * 100, 2),
            'nothing_as_true_nothing': nothing_as_true_nothing,
            'open_as_true_nothing': open_as_true_nothing,
            'open_as_true_open': open_as_true_open,
            'nothing_as_true_open': nothing_as_true_open,
        }
        res['sum'] = res['nothing_as_true_nothing'] + res['open_as_true_nothing'] + res['open_as_true_open'] \
                     + res['nothing_as_true_open']

        return self.__simple_table(res), wrong_prediction, res
