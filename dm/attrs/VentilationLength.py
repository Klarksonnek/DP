from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr


class VentilationLength(AbstractPrepareAttr):
    def execute(self, event_start, event_end, intervals, threshold, prefix):
        diff = event_end - event_start
        value = None

        for interval in intervals:
            if (interval - threshold) < diff < (interval + threshold):
                value = str(interval)
                break

        if value is None:
            raise ValueError('the value can not be assigned to any class')

        name = self.attr_name('event', prefix, '', '')
        before = [(name, "'" + value + "'")]
        #before = [(name, value)]
        after = []

        return before, after
