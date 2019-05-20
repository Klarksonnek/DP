from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage

DATA_CACHE = None

from dm.selectors.row.SimpleCachedRowSelector import SimpleCachedRowSelector


class CachedRowWithIntervalSelector(SimpleCachedRowSelector):
    def __init__(self, con, table_name, start, end):
        self.start = start
        self.end = end
        self.cache = {}
        super(CachedRowWithIntervalSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}
            res = Storage.select_interval(self.con, self.start, self.end, column_name,
                                          self.table_name, without_none_value=False)

            actual_timestamp = self.start
            for row in res:
                if row is None:
                    self.cache[column_name][actual_timestamp] = None
                else:
                    self.cache[column_name][actual_timestamp] = float(row)
                actual_timestamp += 1

        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            value = super(CachedRowWithIntervalSelector, self).row(column_name, time)

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)
        return value
