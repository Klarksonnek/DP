from abc import ABC, abstractmethod
from collections import OrderedDict

from os.path import dirname, abspath, join
import os
from functools import reduce
import sys
import logging
import math
import csv

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.CSVUtil import CSVUtil
from dm.Storage import Storage
from dm.ValueUtil import ValueUtil
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fractions import Fraction
from sympy import *
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull

DATA_CACHE = None


class AttributeUtil:
    @staticmethod
    def training_data_without_opposite(con, table_name, events, func,
                                       row_selector, interval_selector):

        attrs = []
        for k in range(0, len(events)):
            event = events[k]
            start = event['e_start']['timestamp']
            end = event['e_end']['timestamp']

            try:
                data1 = func(con, table_name, start, row_selector, interval_selector, end)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                attrs.append(OrderedDict(data1))
            except Exception as e:
                # logging.error(str(e))
                continue

        return attrs

    @staticmethod
    def cached_training_data(con, table_name, events, func, row_selector, interval_selector,
                             event_type, file_path, print_each=10):

        attrs = []
        ev = []

        if not os.path.exists(file_path):
            attrs, ev = AttributeUtil.training_data(con, table_name, events, func, row_selector,
                                                    interval_selector, event_type, print_each)
            CSVUtil.create_csv_file(attrs, file_path)
        else:
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f, delimiter=',')
                for row in csv_reader:
                    attrs.append(row)

        return attrs, ev


    @staticmethod
    def training_data(con, table_name, events, func, row_selector, interval_selector,
                      event_type, print_each=10):
        """Generovanie trenovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param events: zoznam eventov
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        training_events = []
        attrs = []
        for k in range(0, len(events)):
            event = events[k]
            start = event['e_start']['timestamp']
            end = event['e_end']['timestamp']
            no_event_start = start + event['no_event_time_shift']
            no_event_end = end - event['no_event_time_shift']

            if k % print_each == 0:
                logging.debug('{0}/{1} events'.format(k, len(events)))

            if event_type == 'open':
                event_time = start
                no_event_time = no_event_start
            elif event_type == 'close':
                event_time = end
                no_event_time = no_event_end
            else:
                raise ValueError('event type must be: open or close')

            try:
                data1 = func(con, table_name, event_time, row_selector, interval_selector)
                data2 = func(con, table_name, no_event_time, row_selector, interval_selector)

                time = DateTimeUtil.utc_timestamp_to_str(event_time, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', event_type))
                attrs.append(OrderedDict(data1))

                no_time = DateTimeUtil.utc_timestamp_to_str(no_event_time, '%Y/%m/%d %H:%M:%S')
                data2.insert(0, ('datetime', no_time))
                data2.insert(1, ('event', 'nothing'))
                attrs.append(OrderedDict(data2))
                training_events.append(event)
            except Exception as e:
                # logging.error(str(e))
                continue

        return attrs, training_events

    @staticmethod
    def additional_training_set(con, table_name, no_event_records, func, row_selector, interval_selector,
                                print_each=10):
        """Dodatocne generovanie trenovacich dat, zo zadanych casov.

        :param con:
        :param table_name: nazov tabulky
        :param no_event_records: zoznam dvojic, z ktorych sa maju vygenerovat atributy
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        attrs = []
        for k in range(0, len(no_event_records)):
            row = no_event_records[k]

            if k % print_each == 0:
                logging.debug('{0}/{1} events'.format(k, len(no_event_records)))

            if row[0] == '':
                logging.warning('empty row in additional sets')
                continue

            start = int(DateTimeUtil.local_time_str_to_utc(row[0]).timestamp())

            try:
                data1 = func(con, table_name, start, row_selector, interval_selector)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', row[1]))
                attrs.append(OrderedDict(data1))
            except Exception as e:
                logging.error(str(e))
                continue

        return attrs

    @staticmethod
    def testing_data_with_write(con, table_name, start, end, write_each, func, row_selector,
                                interval_selector, event_type, output_filename,
                                row_count=2048, log_every_hour=1):
        """Generovanie testovacich dat s moznostou priebezneho zapisu do suboru.

        Ak bude row_selector nastaveny na None, vytvori sa pre kazdy zapis vlastny selector,
        ktory sa uvolni po zapise do intervalu.

        :param con:
        :param table_name: nazov tabulky
        :param start: interval, od ktoreho sa budu generovat testovacie data
        :param end: interval, do ktoreho sa budu generovat testovacie data
        :param write_each:
        :param func:
        :param row_selector:
        :param interval_selector:
        :param event_type: typ eventu open alebo close
        :param output_filename: subor, do ktoreho sa maju ukladat testovacie data
        :param row_count: pocet riadkov, ktore sa ma naraz zapisat do suboru
        :return:
        """

        step = row_count * write_each
        records = 0

        if os.path.isfile(output_filename):
            os.remove(output_filename)

        last_timestamp = start
        for timestamp in range(start + step, end + step, step):
            if timestamp > end:
                timestamp = timestamp - (timestamp - end)

            if row_selector is None:
                selector = CachedDiffRowWithIntervalSelector(con, table_name, last_timestamp, timestamp)
            else:
                selector = row_selector

            tr = AttributeUtil.testing_data(con, table_name, last_timestamp, timestamp, write_each, func,
                                            selector, interval_selector, event_type, log_every_hour)
            CSVUtil.create_csv_file(tr, output_filename, enable_append=True)
            last_timestamp = timestamp
            records += len(tr)

            if row_selector is None:
                selector.clear()

        return records

    @staticmethod
    def testing_data(con, table_name, start, end, write_each, func, row_selector, interval_selector,
                     event_type, log_every_hour=3):
        """Generovanie testovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param start: interval, od ktoreho sa budu generovat testovacie data
        :param end: interval, do ktoreho sa budu generovat testovacie data
        :param write_each:
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        attrs = []
        bad_open_type_events = []
        global DATA_CACHE

        for t in range(start, end):
            if t % (log_every_hour * 3600) == 0:
                logging.debug(DateTimeUtil.utc_timestamp_to_str(t))

            act_row = None
            if act_row is None:
                previous_row = Storage.one_row(con, table_name, 'open_close', t - 1)
            else:
                previous_row = act_row
            act_row = Storage.one_row(con, table_name, 'open_close', t)

            if event_type not in ['open', 'close']:
                raise ValueError('event type must be: open or close')

            if previous_row is None or act_row is None:
                continue

            open_state = 'nothing'
            if event_type == 'open' and previous_row[0] == 0 and act_row[0] == 1:
                open_state = event_type
            elif event_type == 'close' and previous_row[0] == 1 and act_row[0] == 0:
                open_state = event_type

            if open_state == 'nothing':
                if t % write_each != 0:
                    continue

            try:
                DATA_CACHE = func(con, table_name, t, row_selector, interval_selector)
            except Exception as e:
                # logging.error(str(e))

                if open_state in ['open', 'close']:
                    bad_open_type_events.append(t)
                continue

            time = DateTimeUtil.utc_timestamp_to_str(t, '%Y/%m/%d %H:%M:%S')
            DATA_CACHE.insert(0, ('datetime', time))
            DATA_CACHE.insert(1, ('event', open_state))
            DATA_CACHE.append(('valid', 'yes'))
            attrs.append(OrderedDict(DATA_CACHE))

        if DATA_CACHE is None:
            logging.warning('any {0} events can be skipped'.format(event_type))
        else:
            tmp = {}
            for item in DATA_CACHE:
                key = item[0]
                tmp[key] = None

            tmp['event'] = event_type
            tmp['valid'] = 'no'
            for timestamp in bad_open_type_events:
                tmp['datetime'] = DateTimeUtil.utc_timestamp_to_str(timestamp, '%Y/%m/%d %H:%M:%S')
                attrs.append(OrderedDict(tmp))

        return attrs

    @staticmethod
    def balance_set(training_set, additional_training_set):
        out = []

        index = 0
        for row in training_set:
            if row['event'] == 'nothing' and index < len(additional_training_set):
                out.append(additional_training_set[index])
                index += 1
                continue

            out.append(row)


        return out
