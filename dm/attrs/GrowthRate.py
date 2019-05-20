from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.attrs.AbstractPrepareAttr import AbstractPrepareAttr

class GrowthRate(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                value_delay, prefix):
        """Vypocet tempa rastu.

        Vypocet tempa rastu sa vypocita ako pomer y_t/y_t_-1. Hodnota y_t sa vyberie na
        zaklade posunu dopredu/dozadu a hodnota y_t_-1 sa vyberie ako posun o value_delay
        do historie od hodnoty y_t.

        :param timestamp: stred okienka, ktory sa pouzije ako bod od ktoreho sa posuva
        :param column: stlpec, pre ktory sa maju spocitat atributy
        :param precision: presnost vysledku
        :param intervals_before: intervaly pred udalostou
        :param intervals_after: interaly po udalosti
        :param value_delay: posun do historie, z ktorej sa vyberie hodnota pre vypocet
        :param prefix
        :return:
        """

        before = []
        after = []

        for interval in intervals_before:
            value_time = timestamp - interval
            y_t = self.row_selector.row(column, value_time)
            y_t_1 = self.row_selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_before', interval)
            before.append((name, self.transform(ratio, interval)))

        for interval in intervals_after:
            value_time = timestamp + interval
            y_t = self.row_selector.row(column, value_time)
            y_t_1 = self.row_selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_after', interval)
            after.append((name, self.transform(ratio, interval)))

        return before, after
