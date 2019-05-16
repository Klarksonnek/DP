from os.path import dirname, abspath, join
import sys
import csv
import time
from datetime import timedelta
import logging
import argparse
from shutil import copyfile
from subprocess import PIPE, run
from collections import OrderedDict

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ConnectionUtil import ConnectionUtil
from dm.Attributes import *


def list_of_processes(directory='ventilation_length'):
    return [
       # '//DIP/{0}/DecisionTree'.format(directory),
       # '//DIP/{0}/DeepLearning'.format(directory),
       # '//DIP/{0}/SVM'.format(directory),
        '//DIP/{0}/RandomForest'.format(directory),
       # '//DIP/{0}/NaiveBayes'.format(directory),
        '//DIP/{0}/NeuralNet'.format(directory),
    ]


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    logging.info('start')

    launcher = ConnectionUtil.rapid_miner()['launcher']

    out_s_maskou = []
    out_s_exp = []

    all = []
    for proc in list_of_processes():
        proc_name = proc.split('/')[-1]
        row_klasicky = [('nazov', proc_name), ('pristup', 'klasicky')]
        row_s_maskou = [('nazov', proc_name), ('pristup', 's_maskou')]
        row_s_exp = [('nazov', proc_name), ('pristup', 's_exp')]

        for bin in range(2, 33):
            cmd = [
                launcher,
                proc,
                '-Mnumber={0}'.format(bin),
            ]

            result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            output = str(run(['python3', 'performance_2.py'],  stdout=PIPE, universal_newlines=True).stdout).strip()
            p1 = output.split('\n')[1].split(' ')[2]
            p2 = output.split('\n')[bin + 4].split(' ')[2]
            row_klasicky.append(('bin_{0}'.format(bin), p1))
            row_s_maskou.append(('bin_{0}'.format(bin), p2))

            output = str(run(['python3', 'performance_1.py'], stdout=PIPE, universal_newlines=True).stdout).strip()
            p3 = str(output).strip()

            logging.info('{0}: {1}, {2}, {3}, {4}'.format(proc_name, bin, p1, p2, p3))
            row_s_exp.append(('bin_{0}'.format(bin), p3))

        out_s_maskou.append(OrderedDict(row_klasicky))
        out_s_maskou.append(OrderedDict(row_s_maskou))

        out_s_exp.append(OrderedDict(row_klasicky))
        out_s_exp.append(OrderedDict(row_s_exp))

        all.append(OrderedDict(row_klasicky))
        all.append(OrderedDict(row_s_maskou))
        all.append(OrderedDict(row_s_exp))

    CSVUtil.create_csv_file(out_s_maskou, 's_maskou.csv')
    CSVUtil.create_csv_file(out_s_exp, 's_exp.csv')
    CSVUtil.create_csv_file(all, 'all.csv')

