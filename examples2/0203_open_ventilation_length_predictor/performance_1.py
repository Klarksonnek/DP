import csv
import json
from dm.DateTimeUtil import DateTimeUtil
from dm.Attributes import SimpleExpRegression


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

    interval_diff = intervals[1]['to'] - intervals[1]['from']
    default_min = intervals[0]['to'] - interval_diff
    default_max = intervals[-1]['from'] + interval_diff

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
        row['real_minus_predicted_diff'] = {}

        f = SimpleExpRegression.gen_f(float(row['co2_start']), 350)
        tmp = []
        for j in range(0, len(intervals)):
            v1 = f(5*60, intervals[j]['avg']/3600.0)
            v = abs(row['measured'] - v1)

            row['real_minus_predicted_diff'][j] = v
            tmp.append(v)

        mi = row['prediction']['avg']
        ma = max(tmp)
        medzisucet += mi/ma
        count += 1

    print(round(1 - medzisucet/count, 4))
    print(json.dumps(intervals, indent=4))
