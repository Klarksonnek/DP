from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage
from dm.selectors.row.AbstractRowSelector import AbstractRowSelector


class SimpleCachedRowSelector(AbstractRowSelector):
    def __init__(self, con, table_name):
        self.cache = {}
        super(SimpleCachedRowSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}

        value = None
        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            res = Storage.one_row(self.con, self.table_name, column_name, time)

            if res is not None and res[0] is not None:
                self.cache[column_name][time] = float(res[0])
                value = float(res[0])

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return value

    def clear(self):
        del self.cache
