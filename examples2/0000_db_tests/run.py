import logging
import sys
from os.path import dirname, abspath, join

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.ConnectionUtil import ConnectionUtil


def test_db_connection():
    con = ConnectionUtil.create_con()

    cur = con.cursor()
    cur.execute('SELECT VERSION()')
    res = cur.fetchone()

    logging.info(res)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    test_db_connection()
