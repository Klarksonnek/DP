from abc import ABC, abstractmethod


class AbstractIntervalSelector(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        super(AbstractIntervalSelector, self).__init__()

    @abstractmethod
    def interval(self, column_name, start, end):
        pass
