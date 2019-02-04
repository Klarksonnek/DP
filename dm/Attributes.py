from abc import ABC, abstractmethod
from collections import OrderedDict

from os.path import dirname, abspath, join
import sys
import logging

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage


# https://www.smartfile.com/blog/abstract-classes-in-python/
# https://code.tutsplus.com/articles/understanding-args-and-kwargs-in-python--cms-29494
# http://homel.vsb.cz/~dor028/Casove_rady.pdf
class AbstractPrepareAttr(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        self.name = self.__class__.__name__
        super(AbstractPrepareAttr, self).__init__()

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def select_one_row(self, column_name, time):
        res = Storage.one_row(self.con, self.table_name, column_name, time)

        if res is None or res[0] is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return float(res[0])

    def attr_name(self, column_name, interval_type, interval):
        return '{0}_{1}_{2}_{3}'.format(self.name, column_name, interval_type, interval)
