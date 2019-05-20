from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr
class FirstDifferenceAttrA(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize, enable_count, prefix, selected_before, selected_after):
        """Vypocet diferencii.

        Vypocet diferencii sa vykona ako rozdiel medzi hodnotou v case timestamp a hodnotou,
        ktore je posunuta o urcity hodnotu z intervalu dopredu/dozadu.

        :param timestamp: stred okienka, ktory sa pouzije ako bod od ktoreho sa posuva
        :param column: stlpec, pre ktory sa maju spocitat atributy
        :param precision: presnost vysledku
        :param intervals_before: intervaly pred udalostou
        :param intervals_after: interaly po udalosti
        :param normalize: povolenie alebo zakazanie normalizacie diferencie
        :param enable_count:
        :param prefix:
        :param selected_before:
        :param selected_after:
        :return:
        """

        before = []
        after = []

        middle = self.row_selector.row(column, timestamp)

        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((middle - value) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                derivation = round(middle - value, precision)
                name = self.attr_name(column, prefix, 'before', interval)

            before.append((name, self.transform(derivation, interval)))

        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.row_selector.row(column, value_time)

            if normalize:
                derivation = round((value - middle) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                derivation = round(value - middle, precision)
                name = self.attr_name(column, prefix, 'after', interval)

            after.append((name, self.transform(derivation, interval)))

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after

