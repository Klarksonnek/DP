"""Calculates first differences using quantity values (not only successive values).
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


class FirstDifferenceAttrA(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize, enable_count, prefix, selected_before, selected_after):
        before = []
        after = []

        middle = self.row_selector.row(column, timestamp)

        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((middle - value) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                derivation = round(middle - value, precision)
                name = self.attr_name(column, prefix, 'before', interval)

            before.append((name, self.transform(derivation, interval)))

        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((value - middle) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                derivation = round(value - middle, precision)
                name = self.attr_name(column, prefix, 'after', interval)

            after.append((name, self.transform(derivation, interval)))

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after
