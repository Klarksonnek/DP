import json
import logging
import sys
import time
from os.path import dirname, abspath, join

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DBUtil import DBUtil
from dm.PreProcessing import PreProcessing
from dm.DateTimeUtil import DateTimeUtil
from dm.BeeeOnClient import BeeeOnClient
from dm.ConnectionUtil import ConnectionUtil


def devices(filename='devices.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def create_update_table(con, clients, start, end, devices, write_each, table_name):
    step_size = 600
    time_shift = 1200
    min_commit_size = 5000

    # odstranenie posledneho intervalu, ktory mohol obsahovat chybajuce hodnoty
    # z dovodu, ze tento interval este neexistoval
    DBUtil.delete_from_time(con, table_name, step_size)

    last_inserted_row = DBUtil.last_inserted_values(con, table_name)

    last_open_close_state = 0
    actual_commit_size = 0

    logging.info('table: %s' % table_name)

    for interval_from in range(start, end, step_size):
        interval_to = interval_from + step_size

        # ak sa v databaze nachadzaju nejake data a timestamp posledne vlozeneho casu,
        # je vacsi ako aktualne spracovavany koniec intervalu, tak sa spracovanie
        # tohto intervalu preskoci, inak sa zacne od tohto timestampu a tabulka sa doplna
        # o nove udaje
        if last_inserted_row is not None:
            if interval_to < last_inserted_row[0]:
                # skip inserted interval
                continue

        logging.debug('processed interval %s' % DateTimeUtil.create_interval_str(interval_from,
                                                                                 interval_to))

        PreProcessing.prepare(clients, con, table_name, devices, interval_from, interval_to,
                              last_open_close_state, time_shift, write_each=write_each)

        actual_commit_size += step_size // write_each
        if actual_commit_size > min_commit_size:
            logging.debug('commit %s rows' % actual_commit_size)
            con.commit()
            actual_commit_size = 0

        last_open_close_state = DBUtil.last_inserted_open_close_state(con, table_name)

    logging.debug('commit %s rows' % actual_commit_size)
    con.commit()

    logging.info('table %s created and updated' % table_name)


def peto_intrak_db(con, cls, start, end, devs):
    # v tomto case doslo k zmene DeviceID Protronix CO2 senzora
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/20 03:00:00').timestamp())

    # full db
    table_pt = 'measured_peto'
    DBUtil.create_table(con, table_pt)
    create_update_table(con, cls, start, middle, devs['peto'], 1, table_pt)
    create_update_table(con, cls, middle, end, devs['peto2'], 1, table_pt)

    # faster db
    table_pt = 'measured_peto_reduced'
    DBUtil.create_table(con, table_pt)
    create_update_table(con, cls, start, middle, devs['peto'], 15, table_pt)
    create_update_table(con, cls, middle, end, devs['peto2'], 15, table_pt)


def klarka_izba_db(con, cls, start, end, devs):
    table_kl = 'measured_klarka'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devs['klarka'], 1, table_kl)

    table_kl = 'measured_klarka_reduced'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devs['klarka'], 15, table_kl)

    # druha DB obsahuje od urciteho datumu vonkajsi IQ Home senzor
    middle = int(DateTimeUtil.local_time_str_to_utc('2019/02/19 12:00:00').timestamp())
    table_kl2 = 'measured_klarka_iqhome'
    DBUtil.create_table(con, table_kl2)
    create_update_table(con, cls, start, middle, devs['klarka'], 1, table_kl2)
    create_update_table(con, cls, middle, end, devs['klarka2'], 1, table_kl2)

    table_kl2 = 'measured_klarka_iqhome_reduced'
    DBUtil.create_table(con, table_kl2)
    create_update_table(con, cls, start, middle, devs['klarka'], 15, table_kl2)
    create_update_table(con, cls, middle, end, devs['klarka2'], 15, table_kl2)


def klarka_sprcha_db(con, cls, start, end, devs):
    # full db
    table_kl = 'measured_klarka_shower'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devs['klarka_shower1'], 1, table_kl)

    # faster db
    table_kl = 'measured_klarka_shower_reduced'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devs['klarka_shower2'], 15, table_kl)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
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
