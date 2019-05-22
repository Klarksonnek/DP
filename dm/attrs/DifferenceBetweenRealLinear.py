"""Calculates differences between real and linearized values of quantity in given time points.
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr
from scipy import stats

__author__ = ''
__email__ = ''


class DifferenceBetweenRealLinear(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                window_size_before, window_size_after, prefix=''):

        intervals_before = [0] + intervals_before
        before = []
        after = []
        infix = '_windowSize{0}_{1}'.format(window_size_before,window_size_after )

        # compute before
        x = []
        y = []
        values = {}

        start = timestamp - window_size_before
        end = timestamp + 1
        for time in range(start, end, 1):
            value = self.row_selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_before:
            if interval > window_size_before:
                break

            time = timestamp - interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = round(linear_value - orig_value, precision)
            name = self.attr_name(column, prefix, infix + '_before', interval)
            before.append((name, self.transform(diff, interval)))

        # compute after
        x = []
        y = []
        values = {}

        start = timestamp
        end = timestamp + window_size_after + 1
        for time in range(start, end, 1):
            value = self.row_selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_after:
            if interval > window_size_after:
                break

            time = timestamp + interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = round(linear_value - orig_value, precision)
            name = self.attr_name(column, prefix, infix + '_after', interval)
            after.append((name, self.transform(diff, interval)))

        return before, after
