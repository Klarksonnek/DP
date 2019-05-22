"""Abstract class for one value selector.

Selector can select value based on given time from a table.
"""
from abc import ABC, abstractmethod

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


class AbstractRowSelector(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        super(AbstractRowSelector, self).__init__()

    @abstractmethod
    def row(self, column_name, time):
        pass

    @abstractmethod
    def clear(self):
        pass
