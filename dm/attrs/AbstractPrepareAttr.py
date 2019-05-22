""" Calculates number of positive differences in given time points, geometric mean,
    arithmetic mean, variance and standard deviation of differences.
"""
from abc import ABC, abstractmethod
from functools import reduce
import math

__author__ = ''
__email__ = ''


# https://www.smartfile.com/blog/abstract-classes-in-python/
# https://code.tutsplus.com/articles/understanding-args-and-kwargs-in-python--cms-29494
# http://homel.vsb.cz/~dor028/Casove_rady.pdf
class AbstractPrepareAttr(ABC):
    def __init__(self, con, table_name, row_selector, interval_selector, tr=None):
        self.con = con
        self.table_name = table_name
        self.name = self.__class__.__name__
        self.row_selector = row_selector
        self.transform = tr
        self.interval_selector = interval_selector

        if self.transform is None:
            self.transform = self.__simple_transform

        super(AbstractPrepareAttr, self).__init__()

    @staticmethod
    def __simple_transform(value, timestamp):
        return value

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def attr_name(self, column_name, prefix, interval_type, interval):
        return '{0}_{1}{2}_{3}_{4}'.format(self.name, column_name, prefix, interval_type,
                                           interval)

    def _compute_increase(self, column, intervals_before, intervals_after,  before, after,
                          selected_before, selected_after, prefix):
        before_out = []
        after_out = []

        for intervals in selected_before:
            before_increase = 0

            for interval in intervals:
                index = intervals_before.index(interval)
                value = before[index][1]

                if value > 0:
                    before_increase += 1

            suffix = '_'.join(str(x) for x in intervals)
            name = self.attr_name(column, prefix, 'before_increase', suffix)
            before_out.append((name, before_increase))

        for intervals in selected_after:
            after_increase = 0

            for interval in intervals:
                index = intervals_after.index(interval)
                value = after[index][1]

                if value > 0:
                    after_increase += 1

            suffix = '_'.join(str(x) for x in intervals)
            name = self.attr_name(column, prefix, 'after_increase', suffix)
            after_out.append((name, after_increase))

        return before_out, after_out

    def _extract_values(self, values):
        out = []
        for row in values:
            out.append(row[1])

        return out

    def geometric_mean(self, column, precision, values_before, values_after, prefix):
        def compute(input_values, interval_name):
            values = self._extract_values(input_values)
            vals = values[1:]
            try:
                vals.remove(0.0)
                vals.remove(0)
            except:
                pass

            count = len(input_values)

            # sqrt can be negative
            is_negative = False
            tmp = reduce((lambda x, y: x * y), vals)
            if tmp < 0:
                is_negative = True
                tmp *= -1
            v1 = round(tmp ** (1/(count - 1)), precision)
            if is_negative:
                v1 *= -1

            attr_prefix = '_geometricMean' + prefix
            name = self.attr_name(column, attr_prefix, interval_name, '')
            return name, v1

        before = [compute(values_before, 'before')]
        after = [compute(values_after, 'after')]

        return before, after

    def arithmetic_mean(self, column, precision, values_before, values_after, prefix):
        def compute(input_values, interval_name):
            count = len(input_values)
            values_sum = sum(self._extract_values(input_values))
            avg = round(values_sum / count, precision)

            attr_prefix = '_arithmeticMean' + prefix
            name = self.attr_name(column, attr_prefix, interval_name, '')
            return name, avg

        before = [compute(values_before, 'before')]
        after = [compute(values_after, 'after')]

        return before, after

    def variance(self, column, precision, values_before, values_after, prefix):
        def compute(input_values, interval_name):
            count = len(input_values)
            values = self._extract_values(input_values)
            values_sum = sum(values)
            avg = values_sum / count

            res = 0
            for row in values:
                res += (row - avg) ** 2
            res = round(res/count, precision)

            attr_prefix = '_variance' + prefix
            name = self.attr_name(column, attr_prefix, interval_name, '')
            return name, res

        before = [compute(values_before, 'before')]
        after = [compute(values_after, 'after')]

        return before, after

    def standard_deviation(self, column, precision, values_before, values_after, prefix):
        def compute(value, interval_name):
            attr_prefix = '_standardDeviation' + prefix
            name = self.attr_name(column, attr_prefix, interval_name, '')
            return name, round(value, precision)

        b, a = self.variance(column, precision, values_before, values_after, prefix)

        before = [compute(math.sqrt(b[0][1]), 'before')]
        after = [compute(math.sqrt(a[0][1]), 'after')]

        return before, after
