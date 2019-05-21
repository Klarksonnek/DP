"""

"""
from abc import ABC, abstractmethod

__author__ = ''
__email__ = ''


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
