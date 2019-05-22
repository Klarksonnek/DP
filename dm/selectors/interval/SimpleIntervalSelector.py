"""Simple interval selector from database.

Selector can select given intervals of values from a given table without cache.
"""
from dm.Storage import Storage
from dm.selectors.interval.AbstractIntervalSelector import AbstractIntervalSelector

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class SimpleIntervalSelector(AbstractIntervalSelector):
    def interval(self, column_name, start, end):
        return Storage.select_interval(self.con, start, end, column_name, self.table_name)

