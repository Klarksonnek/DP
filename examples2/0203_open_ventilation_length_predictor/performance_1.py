"""Performance based on distance.
"""
import csv
from dm.DateTimeUtil import DateTimeUtil

__author__ = ''
__email__ = ''


def extract_interval(value, def_min=None, def_max=None):
    # example: 'range2 [7.400 - 11.800]'
    interval_str = value.split('[')[1].replace(':', '').replace(']', '')
    first_second_interval = filter(None, interval_str.split('-'))

    res = {
        'from': def_min,
        'to': def_max,
    }
    first_option = True
    for row in first_second_interval:
        if first_option:
            first_option = False

            try:
                res['from'] = round(float(row.strip()), 1)
            except:
                pass
        else:
            try:
                res['to'] = round(float(row.strip()), 1)
            except:
                pass

    return res


if __name__ == '__main__':

    performance_file = 'performance.txt'
    output_example_set = 'out.csv'
    intervals = []
    with open(performance_file, 'r') as f:
        for i, line in enumerate(f):
            if i <= 4:
                continue

            row = line.split('\t')
            for k in range(0, len(row)):
                column = row[k].strip()
                if column == '':
                    continue

                if k == 0:
                    intervals.append(extract_interval(column))

    if len(intervals) > 2:
        interval_diff = intervals[1]['to'] - intervals[1]['from']
        default_min = intervals[0]['to'] - interval_diff
        default_max = intervals[-1]['from'] + interval_diff
    else:
        interval_diff = 0
        default_min = 0
        default_max = 0

    intervals[0]['from'] = intervals[0]['to'] - interval_diff
    intervals[-1]['to'] = intervals[-1]['from'] + interval_diff

    for k in range(0, len(intervals)):
        interval = intervals[k]
        interval['avg'] = round((interval['to'] - interval['from']) / 2 + interval['from'], 3)

    out = []
    with open(output_example_set, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            predicted_param = extract_interval(row['prediction(Regression_co2_in_ppm_before_0)'], default_min, default_max)

            record = {
                'datetime': int(DateTimeUtil.local_time_str_to_utc(row['datetime']).timestamp()),
                'readable': row['datetime'],
                'event': extract_interval(row['Regression_co2_in_ppm_before_0'], default_min, default_max),
                'prediction': predicted_param,
                'measured': float(row['actual_value']),
                'co2_start': float(row['co2_start']),
            }

            out.append(record)

    for k in range(0, len(out)):
        interval = out[k]['prediction']
        interval['avg'] = round((interval['to'] - interval['from'])/2 + interval['from'], 3)

    medzisucet = 0
    count = 0
    for i in range(0, len(out)):
        row = out[i]
        mi = row['prediction']['avg']
        avg = row['event']['from'] + (row['event']['to'] - row['event']['from'])/2
        ma = intervals[-1]['avg']

        chyba = abs(mi - avg)/ma
        medzisucet += chyba
        count += 1

    print(round((1 - medzisucet/count) * 100, 2))
    # print(json.dumps(intervals, indent=4))
