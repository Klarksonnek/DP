"""Assigns given ventilation length to a class.
"""
from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class VentilationLength(AbstractPrepareAttr):
    def execute(self, event_start, event_end, intervals, threshold, prefix):
        diff = event_end - event_start
        value = None

        for interval in intervals:
            if (interval - threshold) < diff < (interval + threshold):
                value = str(interval)
                break

        if value is None:
            raise ValueError('the value can not be assigned to any class')

        name = self.attr_name('event', prefix, '', '')
        before = [(name, "'" + value + "'")]
        # before = [(name, value)]
        after = []

        return before, after
