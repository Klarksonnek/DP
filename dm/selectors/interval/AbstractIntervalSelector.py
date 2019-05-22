"""Abstract class for interval selector.

Selector can select given intervals of values from a given table.
"""
from abc import ABC, abstractmethod

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class AbstractIntervalSelector(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        super(AbstractIntervalSelector, self).__init__()

    @abstractmethod
    def interval(self, column_name, start, end):
        pass
