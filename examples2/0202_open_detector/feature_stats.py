from os.path import dirname, abspath, join
import sys
import csv
import time
from datetime import timedelta
import logging
from subprocess import PIPE, run

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ConnectionUtil import ConnectionUtil
from dm.Performance import Performance
from dm.Attributes import *


processes = [
    '//DIP/clean/clean/DeepLearning',
    '//DIP/clean/clean/SVM',
    '//DIP/clean/clean/DecisionTree',
    '//DIP/clean/clean/RandomForest',
    '//DIP/clean/clean/NaiveBayes',
    '//DIP/clean/clean/NeuralNet',
]

backward = [
    '//DIP/clean/wrapper/backward/SVM',
    '//DIP/clean/wrapper/backward/DecisionTree',
    '//DIP/clean/wrapper/backward/DeepLearning',
    '//DIP/clean/wrapper/backward/NaiveBayes',
    '//DIP/clean/wrapper/backward/RandomForest',
]

forward = [
    '//DIP/clean/wrapper/forward/SVM',
    '//DIP/clean/wrapper/forward/DecisionTree',
    '//DIP/clean/wrapper/forward/DeepLearning',
    '//DIP/clean/wrapper/forward/NaiveBayes',
    '//DIP/clean/wrapper/forward/RandomForest',
]

filters = [
    '//DIP/clean/filter/correlation/SVM',
    '//DIP/clean/filter/correlation/DecisionTree',
    '//DIP/clean/filter/correlation/DeepLearning',
    '//DIP/clean/filter/correlation/NaiveBayes',
    '//DIP/clean/filter/correlation/RandomForest',

    '//DIP/clean/filter/gain_ratio/SVM',
    '//DIP/clean/filter/gain_ratio/DecisionTree',
    '//DIP/clean/filter/gain_ratio/DeepLearning',
    '//DIP/clean/filter/gain_ratio/NaiveBayes',
    '//DIP/clean/filter/gain_ratio/RandomForest',

    '//DIP/clean/filter/pca/SVM',
    '//DIP/clean/filter/pca/DecisionTree',
    '//DIP/clean/filter/pca/DeepLearning',
    '//DIP/clean/filter/pca/NaiveBayes',
    '//DIP/clean/filter/pca/RandomForest',

    '//DIP/clean/filter/relief/SVM',
    '//DIP/clean/filter/relief/DecisionTree',
    '//DIP/clean/filter/relief/DeepLearning',
    '//DIP/clean/filter/relief/NaiveBayes',
    '//DIP/clean/filter/relief/RandomForest',

    '//DIP/clean/filter/svm/SVM',
    '//DIP/clean/filter/svm/DecisionTree',
    '//DIP/clean/filter/svm/DeepLearning',
    '//DIP/clean/filter/svm/NaiveBayes',
    '//DIP/clean/filter/svm/RandomForest',

    '//DIP/clean/clean/NeuralNet',
    '//DIP/clean/filter/correlation/NeuralNet',
    '//DIP/clean/filter/gain_ratio/NeuralNet',
    '//DIP/clean/filter/pca/NeuralNet',
    '//DIP/clean/filter/relief/NeuralNet',
    '//DIP/clean/filter/svm/NeuralNet',
]

OUTPUT_FILENAME = 'out.csv'
BEFORE_TIME = 2 * 60
AFTER_TIME = 3 * 60
ENABLE_SHOW_WRONG_RECORDS = False


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
    output += '{0:14}   '.format(performance['open_as_true_open'])
    output += '{0:13}'.format(performance['nothing_as_true_open'])

    if duration1 != '' and duration2 != '':
        output += '      {0}  {1}'.format(str(duration1)[:9], str(duration2)[:9])

    return output


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('start')

    launcher = ConnectionUtil.rapid_miner()['launcher']
    out = {}
    header = '{0:50} '.format('               filter')
    header += '{0:8}   '.format('accuracy')
    header += '{0:7}   '.format('records')
    header += '  {0:3}      '.format('sum')
    header += '{0:12}   '.format('not_true_not')
    header += '{0:13}   '.format('open_true_not')
    header += '{0:14}   '.format('open_true_open')
    header += '{0:13}   '.format('not_true_open')

    header += '{0:9}  '.format('duration')
    header += '{0:9}'.format('duration')

    logging.debug(header)

    wrong_all = []
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
        duration1 = timedelta(seconds=end_time - start_time)

        str_process = '{0:50} '.format(process)

        if os.path.isfile('out.csv'):
            start_time2 = time.monotonic()
            p = Performance(abspath(OUTPUT_FILENAME))
            _, _, p1 = p.simple()
            table2, wrong2, p2 = p.with_delay(BEFORE_TIME, AFTER_TIME)
            end_time2 = time.monotonic()
            wrong_all += wrong2 + ['-------------------']

            duration2 = timedelta(seconds=end_time2 - start_time2)
            logging.debug(generate_row(str_process, p1, p.count, duration1, duration2))
            logging.debug(generate_row(str_process, p2, p.count, '', ''))

            if ENABLE_SHOW_WRONG_RECORDS:
                for row in wrong2:
                    logging.info(row)

            logging.debug('')
        else:
            logging.error('{0:190} {1}  0:00:00.0'.format(process, str(duration1)[:9]))
