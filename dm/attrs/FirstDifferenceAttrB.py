"""Calculates first differences using quantity values (only successive values).
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class FirstDifferenceAttrB(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize, enable_count, prefix, selected_before, selected_after):
        before = []
        after = []

        middle = self.row_selector.row(column, timestamp)

        last_value = middle
        last_shift = 0
        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((last_value - value) / (interval - last_shift), precision)
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                derivation = round(last_value - value, precision)
                name = self.attr_name(column, prefix, 'before', interval)

            before.append((name, self.transform(derivation, interval)))
            last_value = value
            last_shift = interval

        last_value = middle
        last_shift = 0
        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((value - last_value) / (interval - last_shift), precision)
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                derivation = round(value - last_value, precision)
                name = self.attr_name(column, prefix, 'after', interval)

            after.append((name, self.transform(derivation, interval)))
            last_value = value
            last_shift = interval

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after
