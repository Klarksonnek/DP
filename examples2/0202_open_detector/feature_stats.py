from os.path import dirname, abspath, join
import sys
import csv
import time
from datetime import timedelta
import logging

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ConnectionUtil import ConnectionUtil
from dm.Attributes import *


def performance():
    out = []
    res = {}

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

    res['perf1'] = {
        'records': len(out),
        'accuracy': round(((true_nothing + true_open) / len(out)) * 100, 2),
        'nothing_as_true_nothing': true_nothing,
        'open_as_true_nothing': bad_true_nothing,
        'open_as_true_open': true_open,
        'nothing_as_true_open': bad_true_open,
    }

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

    res['perf2'] = {
        'records': len(out),
        'accuracy': round(((true_nothing + true_open) / len(out)) * 100, 2),
        'nothing_as_true_nothing': true_nothing,
        'open_as_true_nothing': bad_true_nothing,
        'open_as_true_open': true_open,
        'nothing_as_true_open': bad_true_open,
    }

    return res


processes = [
    '//DIP/clean/DecisionTree',
    '//DIP/clean/DeepLearning',
    '//DIP/clean/NaiveBayes',
    '//DIP/clean/RandomForest',
    '//DIP/clean/SVM',

    '//DIP/filter/correlation/DecisionTree',
    '//DIP/filter/correlation/DeepLearning',
    '//DIP/filter/correlation/NaiveBayes',
    '//DIP/filter/correlation/RandomForest',
    '//DIP/filter/correlation/SVM',

    '//DIP/filter/gain_ratio/DecisionTree',
    '//DIP/filter/gain_ratio/DeepLearning',
    '//DIP/filter/gain_ratio/NaiveBayes',
    '//DIP/filter/gain_ratio/RandomForest',
    '//DIP/filter/gain_ratio/SVM',

    '//DIP/filter/pca/DecisionTree',
    '//DIP/filter/pca/DeepLearning',
    '//DIP/filter/pca/NaiveBayes',
    '//DIP/filter/pca/RandomForest',
    '//DIP/filter/pca/SVM',

    '//DIP/filter/relief/DecisionTree',
    '//DIP/filter/relief/DeepLearning',
    '//DIP/filter/relief/NaiveBayes',
    '//DIP/filter/relief/RandomForest',
    '//DIP/filter/relief/SVM',

    '//DIP/filter/svm/DecisionTree',
    '//DIP/filter/svm/DeepLearning',
    '//DIP/filter/svm/NaiveBayes',
    '//DIP/filter/svm/RandomForest',
    '//DIP/filter/svm/SVM',

    '//DIP/clean/NeuralNet',
    '//DIP/filter/correlation/NeuralNet',
    '//DIP/filter/gain_ratio/NeuralNet',
    '//DIP/filter/pca/NeuralNet',
    '//DIP/filter/relief/NeuralNet',
    '//DIP/filter/svm/NeuralNet',

    # '//DIP/wrapper/backward/OptimizeSelectionDecisionTree',
    # '//DIP/wrapper/backward/OptimizeSelectionDeepLearning',
    # '//DIP/wrapper/backward/OptimizeSelectionNaiveBayes',
    # '//DIP/wrapper/backward/OptimizeSelectionNeuralNet',
    # '//DIP/wrapper/backward/OptimizeSelectionSVM',

    # '//DIP/wrapper/forward/OptimizeSelectionDecisionTree',
    # '//DIP/wrapper/forward/OptimizeSelectionDeepLearning',
    # '//DIP/wrapper/forward/OptimizeSelectionNaiveBayes',
    # '//DIP/wrapper/forward/OptimizeSelectionNeuralNet',
    # '//DIP/wrapper/forward/OptimizeSelectionSVM',
]

OUTPUT_FILENAME = 'out.csv'
BEFORE_TIME = 2 * 60
AFTER_TIME = 3 * 60

from subprocess import PIPE, run
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('start')

    launcher = ConnectionUtil.rapid_miner()['launcher']
    out = {}
    header = '{0:40} '.format('               filter')
    header += '{0:8}   '.format('accuracy')
    header += '{0:12}   '.format('not_true_not')
    header += '{0:13}   '.format('open_true_not')
    header += '{0:14}   '.format('open_true_open')
    header += '{0:13}   '.format('not_true_open')

    header += '{0:8}   '.format('accuracy')
    header += '{0:12}   '.format('not_true_not')
    header += '{0:13}   '.format('open_true_not')
    header += '{0:14}   '.format('open_true_open')
    header += '{0:13}   '.format('not_true_open')

    header += '{0:9}  '.format('duration')
    header += '{0:9}  '.format('duration')

    logging.debug(header)

    for process in processes:
        if os.path.isfile('out.csv'):
            os.remove('out.csv')

        cmd = [
            launcher,
            process
        ]

        start_time = time.monotonic()
        result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        end_time = time.monotonic()
        duration = timedelta(seconds=end_time - start_time)

        output = '{0:40} '.format(process)

        if os.path.isfile('out.csv'):
            start_time2 = time.monotonic()
            perform = performance()
            end_time2 = time.monotonic()
            duration2 = timedelta(seconds=end_time2 - start_time2)

            output += '{0:6.2f}%'.format(perform['perf1']['accuracy'])
            output += '{0:12}   '.format(perform['perf1']['nothing_as_true_nothing'])
            output += '{0:13}   '.format(perform['perf1']['open_as_true_nothing'])
            output += '{0:14}   '.format(perform['perf1']['open_as_true_open'])
            output += '{0:13}   '.format(perform['perf1']['nothing_as_true_open'])
            output += '    {0:6.2f}%'.format(perform['perf2']['accuracy'])
            output += '{0:12}   '.format(perform['perf2']['nothing_as_true_nothing'])
            output += '{0:13}   '.format(perform['perf2']['open_as_true_nothing'])
            output += '{0:14}   '.format(perform['perf2']['open_as_true_open'])
            output += '{0:13}   '.format(perform['perf2']['nothing_as_true_open'])
            output += '    {0}  {1}'.format(str(duration)[:9], str(duration2)[:9])
            logging.debug(output)
        else:
            logging.error('{0:190} {1}  0:00:00.0'.format(process, str(duration)[:9]))
