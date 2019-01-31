from collections import OrderedDict
from os.path import dirname, abspath, join
import sys
import logging
import os
from subprocess import call

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage
from dm.Differences import Differences
from dm.CSVUtil import CSVUtil
from scipy import stats


def prepare_file_2(events: list):
    out = []

    for event in events:
        start = event['e_start']['timestamp']
        derivation = event['derivation']

        item = [
            #('datetime', DateTimeUtil.utc_timestamp_to_str(start, '%Y-%m-%d %H:%M:%S')),
            ('event', 'open')
        ]
        Differences.prepare_one_row(derivation, 'before', 'before', item)
        Differences.prepare_one_row(derivation, 'after', 'after', item)
        out.append(OrderedDict(item))

        t = start + event['no_event_time_shift']
        item2 = [
            # ('datetime', DateTimeUtil.utc_timestamp_to_str(t, '%Y-%m-%d %H:%M:%S')),
             ('event', 'nothing')
        ]
        Differences.prepare_one_row(derivation, 'before', 'no_event_before', item2)
        Differences.prepare_one_row(derivation, 'after', 'no_event_after', item2)
        out.append(OrderedDict(item2))

    return out


def liner_reg_before(event: dict, column: str):
    values = event['measured'][column]

    x = []
    y = []

    for i in range(0, event['start_shift']*(-1)):
        x.append(i)
        y.append(values[i])

    slope, intercept, _, _, _ = stats.linregress(x, y)

    return slope, intercept


def linear_reg_after(event: dict, column: str):
    values = event['measured'][column]

    x = []
    y = []

    t = len(values) - event['end_shift']
    for i in range(t, len(values)):
        x.append(i - t)
        y.append(values[i])

    slope, intercept, _, _, _ = stats.linregress(x, y)

    return slope, intercept


def linear_reg(sensor1_events: list, input_attr_name: str, output_attr_name: str):
    for i in range(0, len(sensor1_events)):
        event = sensor1_events[i]

        slope_b, intercept_b = liner_reg_before(event, input_attr_name)
        slope_a, intercept_a = linear_reg_after(event, input_attr_name)

        out = []
        values = event['measured']['rh_in2_specific_g_kg']
        for k in range(0, len(values)):
            if k < (event['start_shift'] * (-1)):
                out.append(intercept_b + slope_b * k)
                continue

            if k > (len(values) - event['end_shift']):
                out.append(intercept_a + slope_a * (k - (len(values) - event['end_shift'])))
                continue

            out.append(None)

        event['measured'][output_attr_name] = out


def main(events_file: str, interval_before: list, interval_after: list,
         no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_klarka'

    shift = max(interval_after)

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, -shift, shift, 'rh_in2_absolute_g_m3')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    filtered = FilterUtil.temperature_diff(filtered, 5, 100)
    filtered = FilterUtil.temperature_out_max(filtered, 15)
    filtered = FilterUtil.humidity(filtered, 6, 1.6, 100)
    logging.info('events after applying the filter: %d' % len(filtered))

    linear_reg(filtered, 'rh_in2_specific_g_kg', 'linear2_sh')

    # pocitanie derivacii
    logging.info('start computing of derivation')
    Differences.prepare_derivation_lin_reg(con, filtered, interval_before, interval_after, table_name,
                                   10, 'rh_in2_specific_g_kg', (60, 60))
    logging.info('end computing of derivation')

    # aplikovanie filtra na overenie spravnosti eventov po vypocitani derivacii
    # dovodom nevalidneho eventu po tejto operacii moze byt napr. chybaju hodnota
    # v case, z ktoreho sa mala pocitat derivacia
    filtered = FilterUtil.only_valid_events(filtered)
    logging.info('events after applying the filter (invalid derivation): %d' % len(filtered))

    # aplikovanie filtra na nenulove derivacie
    filtered = FilterUtil.derivation_not_zero(filtered)
    logging.info('events after applying the filter (non zero derivation): %d' % len(filtered))

    logging.info('start preparing file with number: 2')
    data_2 = prepare_file_2(filtered)
    CSVUtil.create_csv_file(data_2, 'f2.csv')
    logging.info('end preparing file with number: 2')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    possibilities = [
        [120, 180, 240],
    ]

    for interval in possibilities:
        dir_name = '.'
        files = os.listdir(dir_name)
        for item in files:
            if item.endswith(".csv"):
                os.remove(os.path.join(dir_name, item))

        main('examples/events_klarka.json', interval, interval, -500)

        if ConnectionUtil.is_testable_system():
            continue

        cmd = [
            ConnectionUtil.rapid_miner()['launcher'],
            ConnectionUtil.rapid_miner()['repository.processes.path'] + 'p',
        ]
        call(cmd)

        with open('res.res', 'r') as f:
            content = []
            for line in f:
                content.append(line.strip())

        out = {}
        for k in range(0, len(content), 9):
            filename = content[k + 1]
            accuracy = float(content[k + 3].split(':')[1].replace('%', '').strip())
            file = os.path.basename(filename)[:-4]

            logging.info(file, accuracy)
