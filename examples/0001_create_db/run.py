from os.path import dirname, abspath, join
import sys
import json

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
from env_dp.DBUtil import DBUtil
from env_dp.PreProcessing import PreProcessing
from env_dp.DateTimeUtil import DateTimeUtil
import logging

import mysql.connector


def devices(filename='devices.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def create_table_fast_view(client, con, start, end, owner, devices, table_name, write_each):
    last_open_close_state = 0
    step_size = 600
    time_shift = 1200
    min_commit_size = 100000
    actual_commit_size = 0

    for t in range(start, end, step_size):
        logging.debug('processing interval: %s - %s' % (DateTimeUtil.utc_timestamp_to_str(t),
                                                        DateTimeUtil.utc_timestamp_to_str(
                                                        t + step_size, '%H:%M:%S')))

        PreProcessing.prepare(client, con, table_name, devices, t, t + step_size,
                              last_open_close_state, owner, time_shift, write_each=write_each)

        actual_commit_size += step_size // write_each
        if actual_commit_size > min_commit_size:
            logging.debug('commit %s rows' % actual_commit_size)
            con.commit()
            actual_commit_size = 0

        last_open_close_state = DBUtil.last_inserted_open_close_state(con, table_name, owner)

    logging.debug('commit %s rows' % actual_commit_size)
    con.commit()


if __name__ == '__main__':
    exit(0)
    logging.basicConfig(level=logging.DEBUG)

    config = dp.db_config(CODE_DIR + '/config.ini')
    con = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        passwd=config['passwd'],
        database=config['database']
    )

    cur = con.cursor()

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=False)
    client.api_key = dp.api_key(CODE_DIR + '/config.ini')

    # from 2018/09/20 00:01:00
    start = int(dp.local_time_str_to_utc('2018/09/20 00:01:00').timestamp())
    end = int(dp.local_time_str_to_utc('2018/11/24 22:59:59').timestamp())

    table1 = 'fast_view'
    table2 = 'view_all'
    DBUtil.create_table(con, table1)
    DBUtil.create_table(con, table2)

    generate_time = 60 * 60 * 24  # one day
    last_generated_time = None
    for time in range(start, end, generate_time):
        if last_generated_time is None:
            last_generated_time = time
            continue

        logging.debug('processing interval: %s - %s' %
                      (DateTimeUtil.utc_timestamp_to_str(last_generated_time),
                       DateTimeUtil.utc_timestamp_to_str(time)))

        # create or update fast_view table for Klarka
        end1 = DBUtil.last_inserted_values(con, table1, 'Klarka')
        # ak je end1 None, ziaden zaznam este nebol pridany do danej tabulky s danym ownerom
        if end1 is None or end1[0] < time:
            if end1 is None:
                s = last_generated_time
            else:
                s = end1[0]

            logging.debug('finding of last inserted interval for table %s - Klarka', table1)
            create_table_fast_view(client, con, s, time, 'Klarka', devices()['klarka'], table1, 10)

        # create or update fast_view table for Peto
        end1 = DBUtil.last_inserted_values(con, table1, 'Peto')
        if end1 is None or end1[0] < time:
            if end1 is None:
                s = last_generated_time
            else:
                s = end1[0]

            logging.debug('finding of last inserted interval for table %s - Peto',
                          table1)
            create_table_fast_view(client, con, s, time, 'Peto', devices()['peto'], table1, 10)

        # create or update view_all table for Klarka
        end1 = DBUtil.last_inserted_values(con, table2, 'Klarka')
        if end1 is None or end1[0] < time:
            if end1 is None:
                s = last_generated_time
            else:
                s = end1[0]

            logging.debug('finding of last inserted interval for table %s - Klarka', table2)
            create_table_fast_view(client, con, s, time, 'Klarka', devices()['klarka'], table2, 1)

        # create or update view_all table for Peto
        end1 = DBUtil.last_inserted_values(con, table2, 'Peto')
        if end1 is None or end1[0] < time:
            if end1 is None:
                s = last_generated_time
            else:
                s = end1[0]

            logging.debug('finding of last inserted interval for table %s - Peto', table2)
            create_table_fast_view(client, con, s, time, 'Peto', devices()['peto'], table2, 1)

        last_generated_time = time
