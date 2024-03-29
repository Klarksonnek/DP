"""Calculates difference between quantity values after linearization (selects linearized values
   at the moment of window opening and closing).
"""
from dm.attrs.InLinear import InLinear

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


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
