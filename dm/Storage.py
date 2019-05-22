"""

"""
from collections import OrderedDict
from dm.DateTimeUtil import DateTimeUtil
from dm.SQLUtil import SQLUtil
import json
import logging
import os

__author__ = ''
__email__ = ''


class Storage:
    def __init__(self, filename: str, no_event_time_shift: int, table_name: str):
        self.__filename = self.__root_folder() + filename
        self.__no_event_time_shift = no_event_time_shift
        self.__table_name = table_name

    def __root_folder(self):
        pwd = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(pwd, './..', '')) + '/'

    def read_meta(self):
        with open(self.__filename) as f:
            events = json.load(f)

        out = []
        for event in events['events']:
            # atributy, ktore su spolocne pre vsetky udalosti
            attributes = {
                'e_start': {
                    'readable': event['times']['event_start'],
                    'timestamp': int(DateTimeUtil.local_time_str_to_utc(
                        event['times']['event_start']).timestamp())
                },
                'e_end': {
                    'readable': event['times']['event_end'],
                    'timestamp': int(
                        DateTimeUtil.local_time_str_to_utc(
                            event['times']['event_end']).timestamp())
                },
                'measured': {
                    'pressure_in_hpa': [],
                    'temperature_in_celsius': [],
                    'temperature_in2_celsius': [],
                    'temperature_out_celsius': [],
                    'rh_in_percentage': [],
                    'rh_in_absolute_g_m3': [],
                    'rh_in_specific_g_kg': [],
                    'rh_in2_percentage': [],
                    'rh_in2_absolute_g_m3': [],
                    'rh_in2_specific_g_kg': [],
                    'rh_out_percentage': [],
                    'rh_out_absolute_g_m3': [],
                    'rh_out_specific_g_kg': [],
                    'co2_in_ppm': []
                },
                'derivation': {
                    'after': [],
                    'before': [],
                    'no_event_after': [],
                    'no_event_before': []
                },
                'no_event_time_shift': self.__no_event_time_shift,
                'no_event_values': None,
                'valid_event': True
            }

            start = attributes['e_start']['timestamp']
            end = attributes['e_end']['timestamp']
            attributes['event_duration'] = end - start

            # doplnenie atributov, ktore su specificke pre dany json
            # len sa nakopuruju jednotlive polozky json struktury
            for key, value in event.items():
                if key in ['times', 'devices']:
                    continue
                attributes[key] = value

            out.append(attributes)

        return out

    def load_data(self, con, start_shift: int, end_shift: int, column: str):
        data = self.read_meta()

        cur = con.cursor()
        for i in range(0, len(data)):
            event = data[i]

            event['start_shift'] = start_shift
            event['end_shift'] = end_shift

            start = event['e_start']['timestamp'] + start_shift
            end = event['e_end']['timestamp'] + end_shift

            # kontrola, ci velkost intervalu v db bez Null hodnot je rovnaka
            # ako rozdiel intervalov
            sql = SQLUtil.select_interval_size(self.__table_name, start, end, column)
            cur.execute(sql)

            if end - start + 1 != cur.fetchone()[0]:
                event['valid_event'] = False
                continue

            # zistanie pozadovaneho intervalu
            cur.execute(SQLUtil.select_interval(self.__table_name, start, end, '*'))

            # doplnenie udajov z db do struktury
            for row in cur.fetchall():
                if row[3] is not None:
                    event['measured']['pressure_in_hpa'].append(float(row[3]))

                if row[4] is not None:
                    event['measured']['temperature_in_celsius'].append(float(row[4]))

                if row[5] is not None:
                    event['measured']['temperature_in2_celsius'].append(float(row[5]))

                if row[6] is not None:
                    event['measured']['temperature_out_celsius'].append(float(row[6]))

                if row[7] is not None:
                    event['measured']['rh_in_percentage'].append(float(row[7]))

                if row[8] is not None:
                    event['measured']['rh_in2_percentage'].append(float(row[8]))

                if row[9] is not None:
                    event['measured']['rh_in_absolute_g_m3'].append(float(row[9]))

                if row[10] is not None:
                    event['measured']['rh_in2_absolute_g_m3'].append(float(row[10]))

                if row[11] is not None:
                    event['measured']['rh_in_specific_g_kg'].append(float(row[11]))

                if row[12] is not None:
                    event['measured']['rh_in2_specific_g_kg'].append(float(row[12]))

                if row[13] is not None:
                    event['measured']['rh_out_percentage'].append(float(row[13]))

                if row[14] is not None:
                    event['measured']['rh_out_absolute_g_m3'].append(float(row[14]))

                if row[15] is not None:
                    event['measured']['rh_out_specific_g_kg'].append(float(row[15]))

                if row[16] is not None:
                    event['measured']['co2_in_ppm'].append(float(row[16]))

            # ak je nastaveny posun no_eventu na nulu tato cast sa preskoci,
            # v opacnom priapde sa stiahne hodnota
            if event['no_event_time_shift'] != 0:
                sql = SQLUtil.select_one_value(self.__table_name,
                                               start + event['no_event_time_shift'],
                                               '*')
                cur.execute(sql)
                event['no_event_values'] = cur.fetchone()

        return data

    @staticmethod
    def one_row(con, table_name: str, columns: str, timestamp: int):
        cur = con.cursor()

        sql = SQLUtil.select_one_value(table_name, timestamp, columns)
        cur.execute(sql)

        res = cur.fetchone()
        if res is None:
            logging.warning('missing row in table `%s` for sql: %s' % (table_name, sql))
            return None

        return res

    @staticmethod
    def select_interval(con, start, end, column, table_name, without_none_value=True):
        cur = con.cursor()
        sql = SQLUtil.select_interval_size(table_name, start, end, column)
        cur.execute(sql)

        if (end - start + 1) != cur.fetchone()[0] and without_none_value:
            return []

        # kontrola, ci velkost intervalu v db bez Null hodnot je rovnaka
        # ako rozdiel intervalov
        sql = SQLUtil.select_interval(table_name, start, end, column)
        cur.execute(sql)

        out = []
        for row in cur.fetchall():
            if row[0] is None:
                out.append(None)
            else:
                out.append(float(row[0]))

        return out

    @staticmethod
    def dw_columns_ordered(con, start, end, columns, table_name):
        columns = columns.split(',')
        dw_values = {}

        for column in columns:
            dw_values[column] = Storage.select_interval(con, start, end, column, table_name)

        output = []
        for k in range(0, len(dw_values[columns[0]])):
            row = []

            for column in columns:
                row.append((column, dw_values[column][k]))
            output.append(OrderedDict(row))

        return output
