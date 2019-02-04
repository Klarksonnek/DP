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


class FirstDifferenceAttrA(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize):
        """Vypocet diferencii.

        Vypocet diferencii sa vykona ako rozdiel medzi hodnotou v case timestamp a hodnotou,
        ktore je posunuta o urcity hodnotu z intervalu dopredu/dozadu.

        :param timestamp: stred okienka, ktory sa pouzije ako bod od ktoreho sa posuva
        :param column: stlpec, pre ktory sa maju spocitat atributy
        :param precision: presnost vysledku
        :param intervals_before: intervaly pred udalostou
        :param intervals_after: interaly po udalosti
        :param normalize: povolenie alebo zakazanie normalizacie diferencie
        :return:
        """

        before = []
        after = []

        middle = self.select_one_row(column, timestamp)

        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.select_one_row(column, value_time)

            if normalize:
                derivation = round((middle - value) / interval, precision)
                name = self.attr_name(column, 'norm_before', interval)
            else:
                derivation = round(middle - value, precision)
                name = self.attr_name(column, 'before', interval)

            before.append((name, derivation))

        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.select_one_row(column, value_time)

            if normalize:
                derivation = round((value - middle) / interval, precision)
                name = self.attr_name(column, 'norm_after', interval)
            else:
                derivation = round(value - middle, precision)
                name = self.attr_name(column, 'after', interval)

            after.append((name, derivation))

        return before, after


class FirstDifferenceAttrB(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize):
        """Vypocet diferencii druhy sposob.

        Vypocet diferencii sa vykona ako rozdiel medzi susednymi hodnotami, ktore su vsak
        posunute o urcitu hodnotu z intervalu dopredu/dozadu.

        :param timestamp: stred okienka, ktory sa pouzije ako bod od ktoreho sa posuva
        :param column: stlpec, pre ktory sa maju spocitat atributy
        :param precision: presnost vysledku
        :param intervals_before: intervaly pred udalostou
        :param intervals_after: interaly po udalosti
        :param normalize: povolenie alebo zakazanie normalizacie diferencie
        :return:
        """

        before = []
        after = []

        middle = self.select_one_row(column, timestamp)

        last_value = middle
        last_shift = 0
        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.select_one_row(column, value_time)

            if normalize:
                derivation = round((last_value - value) / (interval - last_shift), precision)
                name = self.attr_name(column, 'norm_before', interval)
            else:
                derivation = round(last_value - value, precision)
                name = self.attr_name(column, 'before', interval)

            before.append((name, derivation))
            last_value = value
            last_shift = interval

        last_value = middle
        last_shift = 0
        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.select_one_row(column, value_time)

            if normalize:
                derivation = round((value - last_value) / (interval - last_shift), precision)
                name = self.attr_name(column, 'norm_after', interval)
            else:
                derivation = round(value - last_value, precision)
                name = self.attr_name(column, 'after', interval)

            after.append((name, derivation))
            last_value = value
            last_shift = interval

        return before, after


class SecondDifferenceAttr(FirstDifferenceAttrB):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize):
        before, after = super(SecondDifferenceAttr, self).execute(timestamp, column, precision,
                                                                  intervals_before,
                                                                  intervals_after, normalize)
        """Vypocet druhych derivacii.

        Vypocet druhych derivacii sa vykona pomocou vypoctu prvych derivacii a naslednym
        rozdielom medzi susednymi hodnotami.

        :param timestamp: stred okienka, ktory sa pouzije ako bod od ktoreho sa posuva
        :param column: stlpec, pre ktory sa maju spocitat atributy
        :param precision: presnost vysledku
        :param intervals_before: intervaly pred udalostou
        :param intervals_after: interaly po udalosti
        :param normalize: povolenie alebo zakazanie normalizacie diferencie
        :return:
        """

        before_second = []
        after_second = []

        last_value = before[0][1]
        for k in range(1, len(before)):
            value = before[k][1]

            if normalize:
                name = self.attr_name(column, 'norm_before', k)
            else:
                name = self.attr_name(column, 'before', k)

            derivation = round(last_value - value, precision)
            before_second.append((name, derivation))
            last_value = value

        last_value = after[0][1]
        for k in range(1, len(after)):
            value = after[k][1]

            if normalize:
                name = self.attr_name(column, 'norm_after', k)
            else:
                name = self.attr_name(column, 'after', k)

            derivation = round(value - last_value, precision)
            after_second.append((name, derivation))
            last_value = value

        return before_second, after_second
