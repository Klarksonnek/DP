import json
import logging
import sys
import time
import os
from os.path import dirname, abspath, join

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DBUtil import DBUtil
from dm.PreProcessing import PreProcessing
from dm.DateTimeUtil import DateTimeUtil
from dm.BeeeOnClient import BeeeOnClient
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage


def delete_rows(con, timestamp_from, timestamp_to, table_name):
    table = table_name
    f = timestamp_from
    t = timestamp_to
    cur = con.cursor()

    cur.execute('UPDATE {0} SET pressure_in_hpa = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_in_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_in2_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET temperature_out_celsius = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_in2_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_percentage = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_absolute_g_m3 = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET rh_out_specific_g_kg = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))
    cur.execute('UPDATE {0} SET co2_in_ppm = Null WHERE measured_time >= {1} AND measured_time <= {2}'.format(table, f, t))

    con.commit()


def update_invalid_values(con):
    cur = con.cursor()

    # Peto
    for table in ['measured_peto', 'measured_peto_reduced', 'measured_filtered_peto', 'measured_filtered_peto_reduced']:
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time = 1538920482')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1539410852 AND measured_time <= 1539410865')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1542011517 AND measured_time <= 1542011529')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551896814 AND measured_time <= 1551902894')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551890462 AND measured_time <= 1551890556')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1540144019 AND measured_time <= 1540144924')
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time >= 1545208319 AND measured_time <= 1545208364')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1547292105 AND measured_time <= 1547292149')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time >= 1551339840 AND measured_time <= 1551339852')
        cur.execute('UPDATE ' + table + ' SET open_close = 1 WHERE measured_time >= 1554613585 AND measured_time <= 1554613592')

        delete_rows(con, 1551847133, 1551889587, table)
        delete_rows(con, 1551903872, 1551908262, table)
        delete_rows(con, 1540374284, 1540378270, table)
        delete_rows(con, 1538995201, 1539012743, table)
        delete_rows(con, 1540365694, 1540366698, table)
        delete_rows(con, 1541870939, 1541883662, table)
        delete_rows(con, 1543082767, 1543128959, table)
        delete_rows(con, 1540366406, 1540392145, table)
        delete_rows(con, 1541342801, 1541342997, table)
        delete_rows(con, 1541248034, 1541256678, table)
        delete_rows(con, 1541336415, 1541343035, table)
        delete_rows(con, 1541265886, 1541268330, table)
        delete_rows(con, 1547017612, 1547017804, table)
        delete_rows(con, 1547764885, 1547797834, table)
        delete_rows(con, 1549952386, 1549954380, table)

        delete_rows(con, 1538951188, 1538951527, table)
        delete_rows(con, 1542105369, 1542106204, table)
        delete_rows(con, 1543180780, 1543182998, table)
        delete_rows(con, 1544377532, 1544378399, table)
        delete_rows(con, 1544733452, 1544736700, table)
        delete_rows(con, 1546466972, 1546529446, table)
        delete_rows(con, 1546792707, 1546812008, table)
        delete_rows(con, 1548016983, 1548076447, table)
        delete_rows(con, 1548117828, 1548135492, table)
        delete_rows(con, 1548211577, 1548228314, table)
        delete_rows(con, 1548238685, 1548239010, table)
        delete_rows(con, 1548279855, 1548280843, table)
        delete_rows(con, 1548826585, 1548828602, table)
        delete_rows(con, 1547291955, 1547292307, table)
        delete_rows(con, 1554060946, 1554063977, table)
        delete_rows(con, 1539170291, 1539187647, table)
        delete_rows(con, 1539332345, 1539382163, table)
        delete_rows(con, 1542496507, 1542497157, table)
    con.commit()

    # Klarka
    for table in ['measured_klarka', 'measured_klarka_reduced']:
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time = 1547490233')
        cur.execute('UPDATE ' + table + ' SET open_close = 0 WHERE measured_time = 1547642276')
    con.commit()


def devices(filename='devices.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def create_update_table(con, clients, start, end, devices, tables):
    step_size = 600
    time_shift = 1200
    min_commit_size = 10000
    precision = 2

    total_min = None
    last_inserted_table = tables[0][0]
    str_tables = ''

    # odstranenie posledneho intervalu, ktory mohol obsahovat chybajuce hodnoty
    # z dovodu, ze tento interval este neexistoval
    delete_step = 1 * step_size

    for table in tables:
        DBUtil.create_table(con, table[0])

        DBUtil.delete_from_time(con, table[0], delete_step)
        str_tables += table[0] + ', '

        last_inserted_row = DBUtil.last_inserted_values(con, table[0])
        if last_inserted_row is None:
            continue

        if total_min is None or total_min > last_inserted_row[0]:
            total_min = last_inserted_row[0]
            last_inserted_table = table[0]

    last_open_close_state = 0
    actual_commit_size = 0

    logging.info('table: %s' % str_tables)

    for interval_from in range(start - delete_step, end, step_size):
        interval_to = interval_from + step_size

        # ak sa v databaze nachadzaju nejake data a timestamp posledne vlozeneho casu,
        # je vacsi ako aktualne spracovavany koniec intervalu, tak sa spracovanie
        # tohto intervalu preskoci, inak sa zacne od tohto timestampu a tabulka sa doplna
        # o nove udaje
        if total_min is not None:
            if interval_to < total_min:
                # skip inserted interval
                continue

        logging.debug('processed interval %s' % DateTimeUtil.create_interval_str(interval_from,
                                                                                 interval_to))

        maps, values = PreProcessing.prepare(clients, devices, interval_from, interval_to,
                                             last_open_close_state, time_shift)

        for table in tables:
            if 'filtered' in table[0]:
                values = PreProcessing.ppm_filter(values)

            PreProcessing.insert_values(con, table[0], values, maps, table[1], precision)
            actual_commit_size += step_size // table[1]

        if actual_commit_size > min_commit_size:
            logging.debug('commit %s rows' % actual_commit_size)
            con.commit()
            actual_commit_size = 0

        last_open_close_state = DBUtil.last_inserted_open_close_state(con, last_inserted_table)

    logging.debug('commit %s rows' % actual_commit_size)
    con.commit()

    logging.info('table %s created and updated' % str_tables)


def peto_intrak_db(con, cls, start, end, devs):
    # v tomto case doslo k zmene DeviceID Protronix CO2 senzora
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/20 03:00:00').timestamp())

    tables = [
        ('measured_peto', 1),
        ('measured_peto_reduced', 15),
        ('measured_filtered_peto', 1),
        ('measured_filtered_peto_reduced', 15),
    ]

    create_update_table(con, cls, start, middle, devs['peto'], tables)
    create_update_table(con, cls, middle, end, devs['peto2'], tables)


def klarka_izba_db(con, cls, start, end, devs):
    tables = [
        ('measured_klarka', 1),
        ('measured_klarka_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['klarka'], tables)

    # druha DB obsahuje od urciteho datumu vonkajsi IQ Home senzor
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/19 12:00:00').timestamp())
    tables = [
        ('measured_klarka_iqhome', 1),
        ('measured_klarka_iqhome_reduced', 15),
    ]
    create_update_table(con, cls, start, middle, devs['klarka'], tables)
    create_update_table(con, cls, middle, end, devs['klarka2'], tables)


def klarka_sprcha_db(con, cls, start, end, devs):
    tables = [
        ('measured_klarka_shower', 1),
        ('measured_klarka_shower_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['klarka_shower2'], tables)

    update_shower(con, 'examples/events_klarka_shower.json', ['measured_klarka_shower', 'measured_klarka_shower_reduced'])


def update_shower(con, filename, table_names):
    pwd = os.path.dirname(__file__)
    os.path.abspath(os.path.join(pwd, './..', '')) + '/'

    events = Storage(filename, 0, '').read_meta()

    cur = con.cursor()
    for table in table_names:
        cur.execute('UPDATE {0} SET open_close = 0'.format(table))
    con.commit()

    for event in events:
        start = event['e_start']['timestamp']
        end = event['e_end']['timestamp']

        for timestamp in range(start, end):
            for table in table_names:
                DBUtil.update_attribute(con, table, 'open_close', 1, timestamp)
        con.commit()


def david(con, cls, start, end, devs):
    tables = [
        ('measured_david', 1),
        ('measured_david_reduced', 15),
    ]
    create_update_table(con, cls, start, end, devs['david'], tables)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    devs = devices()

    con = ConnectionUtil.create_con()
    cur = con.cursor()

    cls = {
        "ant-work": BeeeOnClient("ant-work.fit.vutbr.cz", 8010),
        "rehivetech": BeeeOnClient("beeeon.rehivetech.com", 8010),
    }

    cls['ant-work'].api_key = ConnectionUtil.api_key('ant-work')
    cls['rehivetech'].api_key = ConnectionUtil.api_key('rehivetech')

    # from 2018/09/20 00:01:00
    start = int(DateTimeUtil.local_time_str_to_utc('2018/09/20 01:00:00').timestamp())
    end = int(time.time())

    peto_intrak_db(con, cls, start, end, devs)
    klarka_izba_db(con, cls, start, end, devs)

    start = int(DateTimeUtil.local_time_str_to_utc('2018/07/18 06:00:00').timestamp())
    klarka_sprcha_db(con, cls, start, end, devs)

    start = int(DateTimeUtil.local_time_str_to_utc('2019/04/03 15:00:00').timestamp())
    david(con, cls, start, end, devs)

    update_invalid_values(con)
