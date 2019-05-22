"""Gets current value CO2 and measured value CO2 in a given time point.
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr
from sympy import *

__author__ = ''
__email__ = ''


class CO2VentilationLength(AbstractPrepareAttr):
    def execute(self, timestamp_start, timestamp_end, compute_timestamp, intervals,
                method, co2_out, column, precision, prefix):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        return [('actual_value', y[compute_timestamp]), ('co2_start', y[0])], []
