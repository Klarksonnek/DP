from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.attrs.InLinear import InLinear

class DiffInLinear(InLinear):
    def execute(self, timestamp_before, timestamp_after, column, precision,
                start_before, end_before, start_after, end_after, prefix):
        b, a = super(DiffInLinear, self).execute(timestamp_before, timestamp_after,
                                                 column, precision,
                                                 start_before, end_before,
                                                 start_after, end_after, prefix)

        name = self.attr_name(column, prefix, 'before', '')
        before = [(name, round(b[0][1] - a[0][1], 2))]

        return before, []
