from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from scipy import stats
from sympy import *

DATA_CACHE = None

from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr


class InLinear(AbstractPrepareAttr):
    def execute(self, timestamp_before, timestamp_after, column, precision,
                start_before, end_before, start_after, end_after, prefix):
        def compute(start, end, timestamp, interval_name):
            res = self.interval_selector.interval(column, start, end)
            x = []
            y = []
            for i in range(0, len(res)):
                x.append(i + start)
                y.append(res[i])

            slope, intercept, _, _, _ = stats.linregress(x, y)
            res = round(intercept + slope * timestamp, precision)

            if interval_name == 'before':
                interval = end_before - start_before
            else:
                interval = end_after - start_after
            name = self.attr_name(column, prefix, interval_name, str(interval))

            return name, res

        before = [compute(start_before, end_before, timestamp_before, 'before')]
        after = [compute(start_after, end_after, timestamp_after, 'after')]

        return before, after
