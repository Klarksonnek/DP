from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.Storage import Storage

DATA_CACHE = None

from dm.selectors.interval.AbstractIntervalSelector import AbstractIntervalSelector
class SimpleIntervalSelector(AbstractIntervalSelector):
    def interval(self, column_name, start, end):
        return Storage.select_interval(self.con, start, end, column_name, self.table_name)

