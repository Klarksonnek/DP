from os.path import dirname, abspath, join
import sys
import logging

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage
from scipy import stats


def lin_reg(values, index):
    x = []
    y = []

    for i in range(0, len(values)):
        x.append(i)
        y.append(values[i])

    slope, intercept, _, _, _ = stats.linregress(x, y)
    return intercept + slope * index


class Differences:
    @staticmethod
    def prepare_derivation(con, events: list, intervals_before: list, intervals_after: list,
                           table_name: str, precision: int, derivation_attr_name: str,
                           derivation_index: int):
        for i in range(0, len(events)):
            event = events[i]

            no_event_shift = event['no_event_time_shift']
            start = event['e_start']['timestamp']
            open_value = event['measured'][derivation_attr_name][0]
            no_event_open_value = event['no_event_values'][derivation_index]

            if no_event_open_value is None:
                t = DateTimeUtil.utc_timestamp_to_str(start + no_event_shift,
                                                      '%Y-%m-%d %H:%M:%S')
                logging.warning('no_event value is None: %s' % t)

            # derivacia pred otvorenim okna
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulosti, ktora je posunuta o zadany interval dozadu
            for interval in intervals_before:
                value_time = start - interval
                value = Storage.one_row(con, table_name, derivation_attr_name, value_time)

                derivation = None
                if value is not None and value[0] is not None:
                    derivation = round((open_value - float(value[0])) / interval, precision)

                event['derivation']['before'].append(derivation)

            # derivacia po otvoreni okna
            # generovanie derviacii medzi hodnotou otvorenia okna a hodnotou niekde,
            # v buducnosti, ktora je posunuta o zadany interval dopredu
            for interval in intervals_after:
                value_time = start + interval
                value = Storage.one_row(con, table_name, derivation_attr_name, value_time)

                derivation = None
                if value is not None and value[0] is not None:
                    derivation = round((float(value[0]) - open_value) / interval, precision)

                event['derivation']['after'].append(derivation)

            # derivacia pred no_event
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulostia, ktora je posunuta o zadany interval dozadu
            # tento cas je posunuty este aj o posun danej udalosti
            for interval in intervals_before:
                value_time = start + no_event_shift - interval
                value = Storage.one_row(con, table_name, derivation_attr_name, value_time)

                derivation = None
                if value is not None and value[
                    0] is not None and no_event_open_value is not None:
                    derivation = round(
                        (float(no_event_open_value) - float(value[0])) / interval,
                        precision)
                else:
                    event['valid_event'] = False

                event['derivation']['no_event_before'].append(derivation)

            # derivacia pred po no_event
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulostia, ktora je posunuta o zadany interval dozadu
            # tento cas je posunuty este aj o posun danej udalosti
            for interval in intervals_after:
                value_time = start + no_event_shift + interval
                value = Storage.one_row(con, table_name, derivation_attr_name, value_time)

                derivation = None
                if value is not None and value[
                    0] is not None and no_event_open_value is not None:
                    derivation = round(
                        (float(value[0]) - float(no_event_open_value)) / interval,
                        precision)
                else:
                    event['valid_event'] = False

                event['derivation']['no_event_after'].append(derivation)

            event['derivation']['intervals_before'] = intervals_before
            event['derivation']['intervals_after'] = intervals_after
            event['derivation']['intervals_no_event_before'] = intervals_before
            event['derivation']['intervals_no_event_after'] = intervals_after

        return events

    @staticmethod
    def prepare_derivation_lin_reg(con, events: list, intervals_before: list, intervals_after: list,
                           table_name: str, precision: int, derivation_attr_name: str, lin_window_size: tuple):
        for i in range(0, len(events)):
            event = events[i]

            no_event_shift = event['no_event_time_shift']
            start = event['e_start']['timestamp']

            values1 = Storage.select_interval(con, start - lin_window_size[0],
                                              start + lin_window_size[1], derivation_attr_name,
                                              table_name)
            values2 = Storage.select_interval(con, start + no_event_shift - lin_window_size[0],
                                              start + no_event_shift + lin_window_size[1],
                                              derivation_attr_name, table_name)

            if not values2 or not values1:
                event['valid_event'] = False
                continue

            open_value = lin_reg(values1, lin_window_size[0] - 1)
            no_event_open_value = lin_reg(values2, lin_window_size[0] - 1)

            if no_event_open_value is None:
                t = DateTimeUtil.utc_timestamp_to_str(start + no_event_shift,
                                                      '%Y-%m-%d %H:%M:%S')
                logging.warning('no_event value is None: %s' % t)

            # derivacia pred otvorenim okna
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulosti, ktora je posunuta o zadany interval dozadu
            for interval in intervals_before:
                value_time = start - interval
                v = Storage.select_interval(con, value_time - lin_window_size[0],
                                            value_time + lin_window_size[1],
                                            derivation_attr_name, table_name)

                if not v:
                    event['valid_event'] = False
                    break

                value = lin_reg(v, lin_window_size[0] - 1)

                derivation = None
                if value is not None and value is not None:
                    derivation = round((open_value - value) / interval, precision)

                event['derivation']['before'].append(derivation)

            # derivacia po otvoreni okna
            # generovanie derviacii medzi hodnotou otvorenia okna a hodnotou niekde,
            # v buducnosti, ktora je posunuta o zadany interval dopredu
            for interval in intervals_after:
                value_time = start + interval
                v = Storage.select_interval(con, value_time - lin_window_size[0],
                                            value_time + lin_window_size[1],
                                            derivation_attr_name, table_name)

                if not v:
                    event['valid_event'] = False
                    break

                value = lin_reg(v, lin_window_size[0] - 1)

                derivation = None
                if value is not None and value is not None:
                    derivation = round((value - open_value) / interval, precision)

                event['derivation']['after'].append(derivation)

            # derivacia pred no_event
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulostia, ktora je posunuta o zadany interval dozadu
            # tento cas je posunuty este aj o posun danej udalosti
            for interval in intervals_before:
                value_time = start + no_event_shift - interval
                v = Storage.select_interval(con, value_time - lin_window_size[0],
                                            value_time + lin_window_size[1],
                                            derivation_attr_name, table_name)

                if not v:
                    event['valid_event'] = False
                    break

                value = lin_reg(v, lin_window_size[0] - 1)

                derivation = None
                if value is not None and value is not None and no_event_open_value is not None:
                    derivation = round((no_event_open_value - value) / interval, precision)
                else:
                    event['valid_event'] = False

                event['derivation']['no_event_before'].append(derivation)

            # derivacia pred po no_event
            # generovanie derivacii medzi hodnou otvorenia okna a hodnotou niekde
            # v minulostia, ktora je posunuta o zadany interval dozadu
            # tento cas je posunuty este aj o posun danej udalosti
            for interval in intervals_after:
                value_time = start + no_event_shift + interval
                v = Storage.select_interval(con, value_time - lin_window_size[0],
                                            value_time + lin_window_size[1],
                                            derivation_attr_name, table_name)

                if not v:
                    event['valid_event'] = False
                    break

                value = lin_reg(v, lin_window_size[0] - 1)

                derivation = None
                if value is not None and value is not None and no_event_open_value is not None:
                    derivation = round((value - no_event_open_value) / interval, precision)
                else:
                    event['valid_event'] = False

                event['derivation']['no_event_after'].append(derivation)

            event['derivation']['intervals_before'] = intervals_before
            event['derivation']['intervals_after'] = intervals_after
            event['derivation']['intervals_no_event_before'] = intervals_before
            event['derivation']['intervals_no_event_after'] = intervals_after

    def prepare_one_row(derivations: dict, key_name: str, attribute_name: str, item):
        for i in range(0, len(derivations['intervals_' + attribute_name])):
            key = key_name + '_' + str(derivations['intervals_' + attribute_name][i])
            item.append((key, derivations[attribute_name][i]))
