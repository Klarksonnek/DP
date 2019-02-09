from abc import ABC, abstractmethod
from collections import OrderedDict

from os.path import dirname, abspath, join
from functools import reduce
import sys
import logging

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Storage import Storage
from scipy import stats


class AttributeUtil:
    @staticmethod
    def prepare_event(con, table_name, columns, timestamp, intervals_before, intervals_after,
                      value_delays, selector, precision, counts, delays, step_yts,
                      window_sizes):
        attrs = []

        for column in columns:
            op = FirstDifferenceAttrA(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=True)
            attrs += a + b

            op = FirstDifferenceAttrA(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=False)
            attrs += a + b

            op = FirstDifferenceAttrB(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=True)
            attrs += a + b

            op = FirstDifferenceAttrB(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=False)
            attrs += a + b

            op = SecondDifferenceAttr(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=True)
            attrs += a + b

            op = SecondDifferenceAttr(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after, normalize=False)
            attrs += a + b

            op = GrowthRate(con, table_name, selector)
            for value_delay in value_delays:
                a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                                  intervals_before=intervals_before,
                                  intervals_after=intervals_after, value_delay=value_delay)
                attrs += a + b

            op = AvgGrowthRate(con, table_name, selector)
            for count in counts:
                for delay in delays:
                    for step_yt in step_yts:
                        for value_delay in value_delays:
                            a, b = op.execute(timestamp=timestamp, column=column,
                                              precision=precision, count=count, delay=delay,
                                              step_yt=step_yt, delay_yt_1=value_delay)
                            attrs += a + b

            for window_size in window_sizes:
                op = DifferenceBetweenRealLinear(con, table_name, selector)
                a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                                  intervals_before=intervals_before,
                                  intervals_after=intervals_after, window_size=window_size)
                attrs += a + b

        return attrs

    @staticmethod
    def training_data(con, table_name, events, func, selector):
        """Generovanie trenovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param events: zoznam eventov
        :param func:
        :return:
        """

        attrs = []
        for k in range(0, len(events)):
            event = events[k]
            start = event['e_start']['timestamp']
            no_event_start = start + event['no_event_time_shift']

            try:
                data1 = func(con, table_name, start, selector)
                data2 = func(con, table_name, no_event_start, selector)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', 'open'))
                attrs.append(OrderedDict(data1))

                no_time = DateTimeUtil.utc_timestamp_to_str(no_event_start, '%Y/%m/%d %H:%M:%S')
                data2.insert(0, ('datetime', no_time))
                data2.insert(1, ('event', 'nothing'))
                attrs.append(OrderedDict(data2))
            except Exception as e:
                # logging.error(str(e))
                continue

        return attrs

    @staticmethod
    def additional_training_set(con, table_name, no_event_records, func, selector):
        """Dodatocne generovanie trenovacich dat, zo zadanych casov.

        :param con:
        :param table_name: nazov tabulky
        :param no_event_records: zoznam dvojic, z ktorych sa maju vygenerovat atributy
        :param func:
        :return:
        """

        attrs = []
        for row in no_event_records:
            start = int(DateTimeUtil.local_time_str_to_utc(row[0]).timestamp())

            try:
                data1 = func(con, table_name, start, selector)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', row[1]))
                attrs.append(OrderedDict(data1))
            except Exception as e:
                logging.error(str(e))
                continue

        return attrs


    @staticmethod
    def testing_data(con, table_name, start, end, write_each, func, selector):
        """Generovanie testovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param start: interval, od ktoreho sa budu generovat testovacie data
        :param end: interval, do ktoreho sa budu generovat testovacie data
        :param write_each:
        :param func:
        :return:
        """

        attrs = []
        count = 0

        for t in range(start, end):
            previous_row = Storage.one_row(con, table_name, 'open_close', t - 1)
            act_row = Storage.one_row(con, table_name, 'open_close', t)

            open_state = 'nothing'
            if previous_row[0] == 0 and act_row[0] == 1:
                open_state = 'open'

            try:
                data = func(con, table_name, t, selector)
            except Exception as e:
                # logging.error(str(e))
                continue

            if open_state == 'nothing':
                if count < (write_each - 1):
                    count += 1
                    continue
                else:
                    count = 0
            elif open_state == 'open':
                count += 1

            time = DateTimeUtil.utc_timestamp_to_str(t, '%Y/%m/%d %H:%M:%S')
            data.insert(0, ('datetime', time))
            data.insert(1, ('event', open_state))
            attrs.append(OrderedDict(data))

        return attrs

    @staticmethod
    def balance_set(training_set, additional_training_set):
        out = []

        index = 0
        for row in training_set:
            if row['event'] == 'nothing' and index < len(additional_training_set):
                out.append(additional_training_set[index])
                index += 1
                continue

            out.append(row)


        return out


class AbstractRowSelector(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        super(AbstractRowSelector, self).__init__()

    @abstractmethod
    def row(self, column_name, time):
        pass


class SimpleRowSelector(AbstractRowSelector):
    def row(self, column_name, time):
        res = Storage.one_row(self.con, self.table_name, column_name, time)

        if res is None or res[0] is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return float(res[0])


class SimpleCachedRowSelector(AbstractRowSelector):
    def __init__(self, con, table_name):
        self.cache = {}
        super(SimpleCachedRowSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}

        value = None
        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            res = Storage.one_row(self.con, self.table_name, column_name, time)

            if res is not None and res[0] is not None:
                self.cache[column_name][time] = float(res[0])
                value = float(res[0])

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return value


class LinearSimpleCachedRowSelector(AbstractRowSelector):
    def __init__(self, con, table_name, half_window_size):
        self.cache = {}
        self.half_window_size = half_window_size
        super(LinearSimpleCachedRowSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}

        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            start = time - self.half_window_size
            end = time + self.half_window_size
            res = Storage.select_interval(self.con, start, end, column_name, self.table_name,
                                          without_none_value=False)

            error = False
            if res is None or None in res:
                error = True

            if error:
                self.cache[column_name][time] = None
                t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
                raise ValueError('empty value at %s' % t)

            x = []
            y = []
            for i in range(0, len(res)):
                x.append(i)
                y.append(res[i])

            slope, intercept, _, _, _ = stats.linregress(x, y)

            value = intercept + slope * self.half_window_size
            self.cache[column_name][time] = value

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return value


class CachedRowWithIntervalSelector(SimpleCachedRowSelector):
    def __init__(self, con, table_name, start, end):
        self.start = start
        self.end = end
        self.cache = {}
        super(CachedRowWithIntervalSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}
            res = Storage.select_interval(self.con, self.start, self.end, column_name,
                                          self.table_name, without_none_value=False)

            actual_timestamp = self.start
            for row in res:
                if row is None:
                    self.cache[column_name][actual_timestamp] = None
                else:
                    self.cache[column_name][actual_timestamp] = float(row)
                actual_timestamp += 1

        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            value = super(CachedRowWithIntervalSelector, self).row(column_name, time)

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)
        return value


# https://www.smartfile.com/blog/abstract-classes-in-python/
# https://code.tutsplus.com/articles/understanding-args-and-kwargs-in-python--cms-29494
# http://homel.vsb.cz/~dor028/Casove_rady.pdf
class AbstractPrepareAttr(ABC):
    def __init__(self, con, table_name, selector):
        self.con = con
        self.table_name = table_name
        self.name = self.__class__.__name__
        self.selector = selector
        super(AbstractPrepareAttr, self).__init__()

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def attr_name(self, column_name, interval_type, interval):
        return '{0}_{1}_{2}_{3}'.format(self.name, column_name, interval_type, interval)

    def _compute_increase(self, column, intervals_before, intervals_after,  before, after,
                          selected_before, selected_after, prefix):
        before_out = []
        after_out = []

        for intervals in selected_before:
            before_increase = 0

            for interval in intervals:
                index = intervals_before.index(interval)
                value = before[index][1]

                if value > 0:
                    before_increase += 1

            suffix = '_'.join(str(x) for x in intervals)
            name = self.attr_name(column, prefix, 'before_increase', suffix)
            before_out.append((name, before_increase))

        for intervals in selected_after:
            after_increase = 0

            for interval in intervals:
                index = intervals_after.index(interval)
                value = after[index][1]

                if value > 0:
                    after_increase += 1

            suffix = '_'.join(str(x) for x in intervals)
            name = self.attr_name(column, prefix, 'after_increase', suffix)
            after_out.append((name, after_increase))

        return before_out, after_out


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
        :return:
        """

        before = []
        after = []

        middle = self.selector.row(column, timestamp)

        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.selector.row(column, value_time)

            if normalize:
                derivation = round((middle - value) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                derivation = round(middle - value, precision)
                name = self.attr_name(column, prefix, 'before', interval)

            before.append((name, derivation))

        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.selector.row(column, value_time)

            if normalize:
                derivation = round((value - middle) / interval, precision)
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                derivation = round(value - middle, precision)
                name = self.attr_name(column, prefix, 'after', interval)

            after.append((name, derivation))

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after


class FirstDifferenceAttrB(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                normalize, enable_count, prefix, selected_before, selected_after):
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

        middle = self.selector.row(column, timestamp)

        last_value = middle
        last_shift = 0
        for interval in intervals_before:
            value_time = timestamp - interval
            value = self.selector.row(column, value_time)

            if normalize:
                derivation = round((last_value - value) / (interval - last_shift), precision)
                name = self.attr_name(column, prefix, 'norm_before', interval)
            else:
                derivation = round(last_value - value, precision)
                name = self.attr_name(column, prefix, 'before', interval)

            before.append((name, derivation))
            last_value = value
            last_shift = interval

        last_value = middle
        last_shift = 0
        for interval in intervals_after:
            value_time = timestamp + interval
            value = self.selector.row(column, value_time)

            if normalize:
                derivation = round((value - last_value) / (interval - last_shift), precision)
                name = self.attr_name(column, prefix, 'norm_after', interval)
            else:
                derivation = round(value - last_value, precision)
                name = self.attr_name(column, prefix, 'after', interval)

            after.append((name, derivation))
            last_value = value
            last_shift = interval

        if enable_count:
            b, a = self._compute_increase(column, intervals_before, intervals_after,
                                          before, after,
                                          selected_before, selected_after, prefix)
            return before + b, after + a

        return before, after


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
        :return:
        """

        before = []
        after = []

        for interval in intervals_before:
            value_time = timestamp - interval
            y_t = self.selector.row(column, value_time)
            y_t_1 = self.selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_before', interval)
            before.append((name, ratio))

        for interval in intervals_after:
            value_time = timestamp + interval
            y_t = self.selector.row(column, value_time)
            y_t_1 = self.selector.row(column, value_time - value_delay)  # t-1

            ratio = round(y_t / y_t_1, precision)
            name = self.attr_name(column, prefix, 'valDelay' + str(value_delay) + '_after', interval)
            after.append((name, ratio))

        return before, after


class AvgGrowthRate(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, count, delay, step_yt, delay_yt_1,
                prefix=''):
        infix = 'delay{0}_stepYt{1}_valDelay{2}'.format(delay, step_yt, delay_yt_1)
        before = []
        after = []

        before_values = []
        for k in range(0, count):
            t = (timestamp - delay) - k * step_yt

            y_t = self.selector.row(column, t)
            y_t_1 = self.selector.row(column, t - delay_yt_1)  # t-1
            before_values.append(y_t / y_t_1)

        v1 = round(reduce((lambda a, b: a * b), before_values) ** (1/(count - 1)), precision)
        name = self.attr_name(column, prefix, infix + '_before', count)
        before.append((name, v1))

        after_values = []
        for k in range(0, count):
            t = (timestamp + delay) + k * step_yt

            y_t = self.selector.row(column, t)
            y_t_1 = self.selector.row(column, t - delay_yt_1)  # t-1
            after_values.append(y_t / y_t_1)

        v1 = round(reduce((lambda a, b: a * b), after_values) ** (1/(count - 1)), precision)
        name = self.attr_name(column, prefix, infix + '_after', count)
        after.append((name, v1))

        return before, after


class DifferenceBetweenRealLinear(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                window_size, prefix=''):

        intervals_before = [0] + intervals_before
        before = []
        after = []
        infix = '_windowSize{0}'.format(window_size)

        # compute before
        x = []
        y = []
        values = {}

        start = timestamp - window_size
        end = timestamp + 1
        for time in range(start, end, 1):
            value = self.selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_before:
            if interval > window_size:
                break

            time = timestamp - interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = linear_value - orig_value
            name = self.attr_name(column, prefix, infix + '_before', interval)
            before.append((name, diff))

        # compute after
        x = []
        y = []
        values = {}

        start = timestamp
        end = timestamp + window_size + 1
        for time in range(start, end, 1):
            value = self.selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_after:
            if interval > window_size:
                break

            time = timestamp + interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = linear_value - orig_value
            name = self.attr_name(column, prefix, infix + '_after', interval)
            after.append((name, diff))

        return before, after
