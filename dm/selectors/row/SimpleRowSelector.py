"""Simple class for one value selector from database.

Selector can select value based on given time from a table in database without cache.
"""
from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage
from dm.selectors.row import AbstractRowSelector

__author__ = ''
__email__ = ''


class SimpleRowSelector(AbstractRowSelector):
    def row(self, column_name, time):
        res = Storage.one_row(self.con, self.table_name, column_name, time)

        if res is None or res[0] is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return float(res[0])

    def clear(self):
        pass
