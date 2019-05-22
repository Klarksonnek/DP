"""Calculates growth rates.

The growth rate is calculated as y_t/y_t_-1, where y_t is selected
based on forward/backward shift and y_t_-1 is calculated as y_t - value_delay.
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

__author__ = ''
__email__ = ''


class GrowthRate(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                value_delay, prefix):
        before = []
        after = []

        for interval in intervals_before:
            value_time = timestamp - interval
            y_t = self.row_selector.row(column, value_time)
            y_t_1 = self.row_selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_before', interval)
            before.append((name, self.transform(ratio, interval)))

        for interval in intervals_after:
            value_time = timestamp + interval
            y_t = self.row_selector.row(column, value_time)
            y_t_1 = self.row_selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_after', interval)
            after.append((name, self.transform(ratio, interval)))

        return before, after
