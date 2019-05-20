from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

class InOutDiff(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                prefix):

        before = []
        after = []

        for interval in intervals_before:
            res = round(self.row_selector.row(column, timestamp - interval), precision)
            name = self.attr_name(column, prefix, 'before', interval)
            before.append((name, res))

        for interval in intervals_after:
            res = round(self.row_selector.row(column, timestamp + interval), precision)
            name = self.attr_name(column, prefix, 'after', interval)
            before.append((name, res))

        return before, after
