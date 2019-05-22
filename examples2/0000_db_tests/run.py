""" Tests connection to database.
"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.ConnectionUtil import ConnectionUtil
import logging

__author__ = ''
__email__ = ''


def test_db_connection():
    con = ConnectionUtil.create_con()

    cur = con.cursor()
    cur.execute('SELECT VERSION()')
    res = cur.fetchone()

    logging.info(res)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    test_db_connection()
