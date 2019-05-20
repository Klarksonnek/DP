from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage

DATA_CACHE = None

from dm.selectors.row.AbstractRowSelector import AbstractRowSelector

class SimpleRowSelector(AbstractRowSelector):
    def row(self, column_name, time):
        res = Storage.one_row(self.con, self.table_name, column_name, time)

        if res is None or res[0] is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return float(res[0])

    def clear(self):
        pass
