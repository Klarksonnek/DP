"""

"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr
import numpy as np

__author__ = ''
__email__ = ''


class Regression(AbstractPrepareAttr):
    def __init__(self, con, table_name, row_selector, interval_selector, method):
        self._method = method
        super(Regression, self).__init__(con, table_name, row_selector, interval_selector)

    def execute(self, timestamp_start, timestamp_end, column, precision, prefix, enable_error):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        x = np.asarray(x)
        y = np.asarray(y)

        param, err = self._method.compute_parameter(x, y)
        name = self.attr_name(column, prefix, 'before', 0)
        before = [(name, round(param * 3600, precision))]

        if enable_error:
            before.append(('err', round(float(err), 8)))

        return before, []

    @staticmethod
    def gen_f_lambda(co2_start, co2_out):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a * x)

    @staticmethod
    def gen_f_prietok(co2_start, co2_out, volume):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)
