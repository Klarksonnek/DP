"""Calculates differences between quantity values measured indoor and outdoor.
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class InOutDiff(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                prefix):

        before = []
        after = []

        for interval in intervals_before:
            res = round(self.row_selector.row(column, timestamp - interval), precision)
            name = self.attr_name(column, prefix, 'before', interval)
            before.append((name, res))

        for interval in intervals_after:
            res = round(self.row_selector.row(column, timestamp + interval), precision)
            name = self.attr_name(column, prefix, 'after', interval)
            before.append((name, res))

        return before, after
