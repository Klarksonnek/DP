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
                interval = DateTimeUtil.create_interval_str(interval_from,
                                                            interval_from + step_size)

                logging.debug('processed interval %s has been already inserted' % interval)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    con = ConnectionUtil.create_con()
    cur = con.cursor()

    cls = {
        "ant-work": BeeeOnClient("ant-work.fit.vutbr.cz", 8010),
        "rehivetech": BeeeOnClient("beeeon.rehivetech.com", 8010),
    }

    cls['ant-work'].api_key = ConnectionUtil.api_key('ant-work')
    cls['rehivetech'].api_key = ConnectionUtil.api_key('rehivetech')

    # from 2018/09/20 00:01:00
    start = int(DateTimeUtil.local_time_str_to_utc('2018/09/20 00:01:00').timestamp())
    end = int(time.time())

    # full db
    table_pt = 'measured_peto'
    DBUtil.create_table(con, table_pt)
    # DBUtil.check_timestamp_order(con, table_pt)
    create_update_table(con, cls, start, end, devices()['peto'], 1, table_pt)

    table_kl = 'measured_klarka'
    DBUtil.create_table(con, table_kl)
    # DBUtil.check_timestamp_order(con, table_kl)
    create_update_table(con, cls, start, end, devices()['klarka'], 1, table_kl)

    # faster db
    table_pt = 'measured_peto_reduced'
    DBUtil.create_table(con, table_pt)
    create_update_table(con, cls, start, end, devices()['peto'], 15, table_pt)

    table_kl = 'measured_klarka_reduced'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devices()['klarka'], 15, table_kl)

    #
    # shower
    #
    start = int(DateTimeUtil.local_time_str_to_utc('2018/07/18 00:06:00').timestamp())
    end = int(time.time())

    # full db
    table_kl = 'measured_klarka_shower'
    DBUtil.create_table(con, table_kl)
    # DBUtil.check_timestamp_order(con, table_pt)
    create_update_table(con, cls, start, end, devices()['klarka_shower2'], 1, table_kl)

    # faster db
    table_kl = 'measured_klarka_shower_reduced'
    DBUtil.create_table(con, table_kl)
    create_update_table(con, cls, start, end, devices()['klarka_shower2'], 15, table_kl)
