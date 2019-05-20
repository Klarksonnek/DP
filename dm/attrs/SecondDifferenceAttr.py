from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from sympy import *

DATA_CACHE = None

from dm.attrs.FirstDifferenceAttrB import FirstDifferenceAttrB
class SecondDifferenceAttr(FirstDifferenceAttrB):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize, enable_count, prefix, selected_before, selected_after):
        before, after = super(SecondDifferenceAttr, self).execute(timestamp, column, precision,
                                                                  intervals_before,
                                                                  intervals_after, normalize,
                                                                  False, prefix,
                                                                  selected_before,
                                                                  selected_after)
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

            interval = '{0}and{1}'.format(intervals_before[k - 1], intervals_before[k])
            if normalize:
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                name = self.attr_name(column, prefix, 'before', interval)

            derivation = round(last_value - value, precision)
            before_second.append((name, derivation))
            last_value = value

        last_value = after[0][1]
        for k in range(1, len(after)):
            value = after[k][1]

            interval = '{0}and{1}'.format(intervals_after[k - 1], intervals_after[k])
            if normalize:
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                name = self.attr_name(column, prefix, 'after', interval)

            derivation = round(value - last_value, precision)
            after_second.append((name, derivation))
            last_value = value

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after