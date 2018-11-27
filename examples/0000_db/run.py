#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.db_core as dp


def test_db_connection():
    con = dp.create_con()

    cur = con.cursor()
    cur.execute('SELECT VERSION()')
    res = cur.fetchone()

    print(res)


if __name__ == '__main__':
    test_db_connection()
