import json
import logging
import sys
import csv
import datetime as dt
import time
import os
from os.path import dirname, abspath, join
from matplotlib.dates import DateFormatter
from collections import OrderedDict
import matplotlib.pyplot as plt

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DBUtil import DBUtil
from dm.PreProcessing import PreProcessing
from dm.DateTimeUtil import DateTimeUtil
from dm.BeeeOnClient import BeeeOnClient
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage
from dm.CSVUtil import CSVUtil


def simple_graph(filename):
    x1 = []
    raw_t = []
    y1 = []
    with open(filename) as f1:
        csv_reader = csv.DictReader(f1, delimiter=',')
        for row in csv_reader:
            try:
                y1.append(float(row['co2_in_ppm']))
                x1.append(dt.datetime.fromtimestamp(float(row['measured_time'])))
                raw_t.append(float(row['measured_time']))
            except:
                continue

    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(x1, y1, '-r', label='Vonkajšia koncentrácia $CO_2$')

    # nastavenie formatu casu
    formatter = DateFormatter('%m/%d\n%H:%M')
    ax.xaxis.set_major_formatter(formatter)

    ax.grid()
    ax.legend()
    ax.set_xlabel('Čas [h]')
    ax.set_ylabel(r'Koncentrácia $CO_2$ [ppm]')

    # minimum
    ax.set_ylim(min(y1) - 50, max(y1)+50)
    ax.set_xlim(dt.datetime.fromtimestamp(raw_t[0]-5), dt.datetime.fromtimestamp(raw_t[-1]+5))

    filename = simple_graph.__name__ + '.eps'
    fig.canvas.set_window_title(filename)

    # nastavenie, aby sa aj pri malej figsize zobrazoval nazov X osy
    plt.tight_layout()

    fig.savefig(filename, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    con = ConnectionUtil.create_con()

    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 06:00:00').timestamp())
    end = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 09:00:00').timestamp())
    table_name = 'measured_filtered_peto'

    all = Storage.dw_columns_ordered(con, start, end, 'measured_time,co2_in_ppm', table_name)
    CSVUtil.create_csv_file(all, 'test.csv')

    simple_graph('test.csv')

    plt.show()
