from abc import ABC, abstractmethod
from collections import OrderedDict

from os.path import dirname, abspath, join
import os
from functools import reduce
import sys
import logging
import math
import csv

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.CSVUtil import CSVUtil
from dm.Storage import Storage
from dm.ValueUtil import ValueUtil
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fractions import Fraction
from sympy import *
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull

DATA_CACHE = None


class AttributeUtil:
    @staticmethod
    def training_data_without_opposite(con, table_name, events, func,
                                       row_selector, interval_selector):

        attrs = []
        for k in range(0, len(events)):
            event = events[k]
            start = event['e_start']['timestamp']
            end = event['e_end']['timestamp']

            try:
                data1 = func(con, table_name, start, row_selector, interval_selector, end)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                attrs.append(OrderedDict(data1))
            except Exception as e:
                # logging.error(str(e))
                continue

        return attrs

    @staticmethod
    def cached_training_data(con, table_name, events, func, row_selector, interval_selector,
                             event_type, file_path, print_each=10):

        attrs = []
        ev = []

        if not os.path.exists(file_path):
            attrs, ev = AttributeUtil.training_data(con, table_name, events, func, row_selector,
                                                    interval_selector, event_type, print_each)
            CSVUtil.create_csv_file(attrs, file_path)
        else:
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f, delimiter=',')
                for row in csv_reader:
                    attrs.append(row)

        return attrs, ev


    @staticmethod
    def training_data(con, table_name, events, func, row_selector, interval_selector,
                      event_type, print_each=10):
        """Generovanie trenovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param events: zoznam eventov
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        training_events = []
        attrs = []
        for k in range(0, len(events)):
            event = events[k]
            start = event['e_start']['timestamp']
            end = event['e_end']['timestamp']
            no_event_start = start + event['no_event_time_shift']
            no_event_end = end - event['no_event_time_shift']

            if k % print_each == 0:
                logging.debug('{0}/{1} events'.format(k, len(events)))

            if event_type == 'open':
                event_time = start
                no_event_time = no_event_start
            elif event_type == 'close':
                event_time = end
                no_event_time = no_event_end
            else:
                raise ValueError('event type must be: open or close')

            try:
                data1 = func(con, table_name, event_time, row_selector, interval_selector)
                data2 = func(con, table_name, no_event_time, row_selector, interval_selector)

                time = DateTimeUtil.utc_timestamp_to_str(event_time, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', event_type))
                attrs.append(OrderedDict(data1))

                no_time = DateTimeUtil.utc_timestamp_to_str(no_event_time, '%Y/%m/%d %H:%M:%S')
                data2.insert(0, ('datetime', no_time))
                data2.insert(1, ('event', 'nothing'))
                attrs.append(OrderedDict(data2))
                training_events.append(event)
            except Exception as e:
                # logging.error(str(e))
                continue

        return attrs, training_events

    @staticmethod
    def additional_training_set(con, table_name, no_event_records, func, row_selector, interval_selector,
                                print_each=10):
        """Dodatocne generovanie trenovacich dat, zo zadanych casov.

        :param con:
        :param table_name: nazov tabulky
        :param no_event_records: zoznam dvojic, z ktorych sa maju vygenerovat atributy
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        attrs = []
        for k in range(0, len(no_event_records)):
            row = no_event_records[k]

            if k % print_each == 0:
                logging.debug('{0}/{1} events'.format(k, len(no_event_records)))

            if row[0] == '':
                logging.warning('empty row in additional sets')
                continue

            start = int(DateTimeUtil.local_time_str_to_utc(row[0]).timestamp())

            try:
                data1 = func(con, table_name, start, row_selector, interval_selector)

                time = DateTimeUtil.utc_timestamp_to_str(start, '%Y/%m/%d %H:%M:%S')
                data1.insert(0, ('datetime', time))
                data1.insert(1, ('event', row[1]))
                attrs.append(OrderedDict(data1))
            except Exception as e:
                logging.error(str(e))
                continue

        return attrs

    @staticmethod
    def testing_data_with_write(con, table_name, start, end, write_each, func, row_selector,
                                interval_selector, event_type, output_filename,
                                row_count=2048, log_every_hour=1):
        """Generovanie testovacich dat s moznostou priebezneho zapisu do suboru.

        Ak bude row_selector nastaveny na None, vytvori sa pre kazdy zapis vlastny selector,
        ktory sa uvolni po zapise do intervalu.

        :param con:
        :param table_name: nazov tabulky
        :param start: interval, od ktoreho sa budu generovat testovacie data
        :param end: interval, do ktoreho sa budu generovat testovacie data
        :param write_each:
        :param func:
        :param row_selector:
        :param interval_selector:
        :param event_type: typ eventu open alebo close
        :param output_filename: subor, do ktoreho sa maju ukladat testovacie data
        :param row_count: pocet riadkov, ktore sa ma naraz zapisat do suboru
        :return:
        """

        step = row_count * write_each
        records = 0

        if os.path.isfile(output_filename):
            os.remove(output_filename)

        last_timestamp = start
        for timestamp in range(start + step, end + step, step):
            if timestamp > end:
                timestamp = timestamp - (timestamp - end)

            if row_selector is None:
                selector = CachedDiffRowWithIntervalSelector(con, table_name, last_timestamp, timestamp)
            else:
                selector = row_selector

            tr = AttributeUtil.testing_data(con, table_name, last_timestamp, timestamp, write_each, func,
                                            selector, interval_selector, event_type, log_every_hour)
            CSVUtil.create_csv_file(tr, output_filename, enable_append=True)
            last_timestamp = timestamp
            records += len(tr)

            if row_selector is None:
                selector.clear()

        return records

    @staticmethod
    def testing_data(con, table_name, start, end, write_each, func, row_selector, interval_selector,
                     event_type, log_every_hour=3):
        """Generovanie testovacich dat.

        :param con:
        :param table_name: nazov tabulky
        :param start: interval, od ktoreho sa budu generovat testovacie data
        :param end: interval, do ktoreho sa budu generovat testovacie data
        :param write_each:
        :param func:
        :param row_selector:
        :param interval_selector:
        :return:
        """

        attrs = []
        bad_open_type_events = []
        global DATA_CACHE

        for t in range(start, end):
            if t % (log_every_hour * 3600) == 0:
                logging.debug(DateTimeUtil.utc_timestamp_to_str(t))

            act_row = None
            if act_row is None:
                previous_row = Storage.one_row(con, table_name, 'open_close', t - 1)
            else:
                previous_row = act_row
            act_row = Storage.one_row(con, table_name, 'open_close', t)

            if event_type not in ['open', 'close']:
                raise ValueError('event type must be: open or close')

            if previous_row is None or act_row is None:
                continue

            open_state = 'nothing'
            if event_type == 'open' and previous_row[0] == 0 and act_row[0] == 1:
                open_state = event_type
            elif event_type == 'close' and previous_row[0] == 1 and act_row[0] == 0:
                open_state = event_type

            if open_state == 'nothing':
                if t % write_each != 0:
                    continue

            try:
                DATA_CACHE = func(con, table_name, t, row_selector, interval_selector)
            except Exception as e:
                # logging.error(str(e))

                if open_state in ['open', 'close']:
                    bad_open_type_events.append(t)
                continue

            time = DateTimeUtil.utc_timestamp_to_str(t, '%Y/%m/%d %H:%M:%S')
            DATA_CACHE.insert(0, ('datetime', time))
            DATA_CACHE.insert(1, ('event', open_state))
            DATA_CACHE.append(('valid', 'yes'))
            attrs.append(OrderedDict(DATA_CACHE))

        if DATA_CACHE is None:
            logging.warning('any {0} events can be skipped'.format(event_type))
        else:
            tmp = {}
            for item in DATA_CACHE:
                key = item[0]
                tmp[key] = None

            tmp['event'] = event_type
            tmp['valid'] = 'no'
            for timestamp in bad_open_type_events:
                tmp['datetime'] = DateTimeUtil.utc_timestamp_to_str(timestamp, '%Y/%m/%d %H:%M:%S')
                attrs.append(OrderedDict(tmp))

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


class VentilationLength(AbstractPrepareAttr):
    def execute(self, event_start, event_end, intervals, threshold, prefix):
        diff = event_end - event_start
        value = None

        for interval in intervals:
            if (interval - threshold) < diff < (interval + threshold):
                value = str(interval)
                break

        if value is None:
            raise ValueError('the value can not be assigned to any class')

        name = self.attr_name('event', prefix, '', '')
        before = [(name, "'" + value + "'")]
        #before = [(name, value)]
        after = []

        return before, after


class DiffInLinear(InLinear):
    def execute(self, timestamp_before, timestamp_after, column, precision,
                start_before, end_before, start_after, end_after, prefix):
        b, a = super(DiffInLinear, self).execute(timestamp_before, timestamp_after,
                                                 column, precision,
                                                 start_before, end_before,
                                                 start_after, end_after, prefix)

        name = self.attr_name(column, prefix, 'before', '')
        before = [(name, round(b[0][1] - a[0][1], 2))]

        return before, []


class AbstractRegression(ABC):
    def __init__(self, co2_out):
        self._co2_out = co2_out
        super(AbstractRegression, self).__init__()

    @abstractmethod
    def compute_parameter(self, x, y):
        pass

    @abstractmethod
    def compute_curve(self, x, y):
        pass


class SimpleExpRegression(AbstractRegression):
    def __init__(self, co2_out, volume):
        self._volume = volume
        super(SimpleExpRegression, self).__init__(co2_out)

    @staticmethod
    def gen_f(co2_start, co2_out):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a * x)

    @staticmethod
    def gen_f_volume(co2_start, co2_out, volume):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)

    def compute_parameter(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)

        if self._volume is None:
            f = SimpleExpRegression.gen_f(y[0], self._co2_out)
        else:
            f = SimpleExpRegression.gen_f_volume(y[0], self._co2_out, self._volume)

        popt, pcov = curve_fit(f, x, y)
        return popt[0], np.sqrt(np.diag(pcov))

    def compute_curve(self, x, y):
        # index 0 - parameter, index 1 - error
        param = self.compute_parameter(x, y)[0]

        if self._volume is None:
            f = SimpleExpRegression.gen_f(y[0], self._co2_out)
        else:
            f = SimpleExpRegression.gen_f_volume(y[0], self._co2_out, self._volume)

        out = []
        for i in range(0, len(x)):
            out.append(f(i, param))

        return out


class ExpRegressionWithDelay(SimpleExpRegression):
    def __init__(self, co2_out, volume, window_size, threshold):
        self._window_size = window_size
        self._threshold = threshold
        super(ExpRegressionWithDelay, self).__init__(co2_out, volume)

    def compute_parameter(self, x, y):
        delay = ValueUtil.detect_sensor_delay(x, self._window_size, self._threshold)
        return super(ExpRegressionWithDelay, self).compute_parameter(x[delay:], y[delay:])

    def compute_curve(self, x, y):
        delay = ValueUtil.detect_sensor_delay(y, self._window_size, self._threshold)

        new_x = []
        for i in range(0, len(x) - delay):
            new_x.append(i)

        values = super(ExpRegressionWithDelay, self).compute_curve(new_x, y[delay:])

        if delay == 0:
            return values

        out = []
        for k in range(0, delay):
            out.append(y[k])

        return out + values


class Regression(AbstractPrepareAttr):
    def __init__(self, con, table_name, row_selector, interval_selector, method):
        self._method = method
        super(Regression, self).__init__(con, table_name, row_selector, interval_selector)

    def execute(self, timestamp_start, timestamp_end, column, precision, prefix, enable_error):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        x = np.asarray(x)
        y = np.asarray(y)

        param, err = self._method.compute_parameter(x, y)
        name = self.attr_name(column, prefix, 'before', 0)
        before = [(name, round(param * 3600, precision))]

        if enable_error:
            before.append(('err', round(float(err), 8)))

        return before, []

    @staticmethod
    def gen_f_lambda(co2_start, co2_out):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a * x)

    @staticmethod
    def gen_f_prietok(co2_start, co2_out, volume):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)


class CO2VentilationLength(AbstractPrepareAttr):
    def execute(self, timestamp_start, timestamp_end, compute_timestamp, intervals,
                method, co2_out, column, precision, prefix):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        return [('actual_value', y[compute_timestamp]), ('co2_start', y[0])], []


class AbstractLineCoefficients(ABC):
    def __init__(self):
        super(AbstractLineCoefficients, self).__init__()

    @abstractmethod
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        pass

    def convert_line(self, coeffs):
        if coeffs[1] == 0:
            return self._convert_line_to_general_without_c(coeffs)

        return self._convert_line_to_general(coeffs)

    def _convert_line_to_general(self, coeffs):
        """ Converts line equation y = kx + q to the form ax + by + c = 0 (general form)
        """

        # represents coeffs as fractions
        tmp = Fraction(str(coeffs[0])).limit_denominator(1000)
        n1 = tmp.numerator
        d1 = tmp.denominator

        tmp2 = Fraction(str(coeffs[1])).limit_denominator(1000)
        n2 = tmp2.numerator
        d2 = tmp2.denominator

        # find LCM
        L = np.lcm(d1, d2)

        # symbolic variables
        x = var('x')

        y1 = (n1 * x) / d1
        y2 = n2 / d2

        y_mult1 = y1 * L

        a = y_mult1.subs('x', 1) * (-1)

        y_mult2 = (y2 * L)
        c = y_mult2 * (-1)

        b = L

        return a, b, c

    def _convert_line_to_general_without_c(self, coeffs):
        """ Converts line equation y = kx to the form ax + by = 0 (general form)
        """

        # represents coeffs as fractions
        tmp = Fraction(str(coeffs[0])).limit_denominator(1000)
        n1 = tmp.numerator
        d1 = tmp.denominator

        # symbolic variables
        x = var('x')

        y1 = (n1 * x) / d1

        y_mult1 = y1 * d1

        a = y_mult1.subs('x', 1) * (-1)

        b = d1

        return a, b, 0


class MathLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            b = -(float(row[col1]) - float(row[col2]))
            a = float(row[col3])
            direction.append(-a / b)

        return sum(direction) / float(len(direction))


class PolyfitLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            sh_decrease_tmp = [0, float(row[col1]) - float(row[col2])]
            sh_diff_tmp = [0, float(row[col3])]
            coeffs_point = np.polyfit(sh_decrease_tmp, sh_diff_tmp, 1)
            direction.append(coeffs_point[0])

        return sum(direction) / float(len(direction))


class CenterLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        a = point_y
        b = -point_x

        return -a / b


class DistanceToLine:
    def __init__(self, training):
        self.training = training
        self.model = None

    @staticmethod
    def ventilation_length_events(training: list, ventilation_length: int):
        out = []

        for row in training:
            if row['VentilationLength_event__'] == "'" + str(ventilation_length) + "'":
                out.append(row)

        return out

    def humidity_clusters(self, training, col1, col2, col3, intervals, strategy, strategyFlag, one_line,
                          cluster_boundaries, cluster_boundaries_all):
        """

        :param training:
        :param col1:
        :param col2:
        :param col3:
        :param intervals:
        :param strategy:
        :return:
        """

        # colors
        if cluster_boundaries_all:
            colors_trendline = [(0.854, 0.035, 0.027), (0.101, 0.454, 0.125), (0, 0.545, 0.545), (0.545, 0, 0.545), (0, 0, 1)]
            colors_line = [(1, 0.5, 0.5), (0.5, 1, 0.5), (0, 1, 1), (1, 0, 1), (0.5, 0.5, 1)]
        else:
            colors_trendline = [(0.854, 0.035, 0.027), (0.101, 0.454, 0.125), (0, 0, 1)]
            colors_line = [(1, 0.5, 0.5), (0.5, 1, 0.5), (0.5, 0.5, 1)]
        # counter for colors
        i = 0
        fig = plt.figure()
        out_point_line = {}
        out_point_point = {}

        for interval in intervals:
            sh_decrease = []
            sh_diff = []
            for res in self.ventilation_length_events(training, interval * 60):
                sh_decrease.append(float(res[col1]) - float(res[col2]))
                sh_diff.append(float(res[col3]))

            logging.debug('sh_decrease: %s, sh_diff: %s' % (str(sh_decrease), str(sh_diff)))

            # k-means clustering
            X = np.array(list(zip(sh_decrease, sh_diff)))
            # number of clusters (we assume one cluster: K=1)
            kmeans = KMeans(n_clusters=1)
            # fitting the input data
            kmeans = kmeans.fit(X)
            # centroid values
            C = kmeans.cluster_centers_

            # get coefficients of the line (1st order polynom = line)
            coeffs = np.polyfit(sh_decrease, sh_diff, 1)

            if one_line and strategyFlag == 'polyfit_':
                for j in range(0, len(DistanceToLine.ventilation_length_events(training, interval * 60))):
                    b = -sh_decrease[j]
                    a = sh_diff[j]
                    direction = -a / b
                    y = direction * sh_decrease[j]
                    plt.plot([0, sh_decrease[j]], [0, y], color=colors_line[i], linewidth=0.75)
                    plt.xlim(0.0, 3.0)
                    plt.ylim(0.0, 7.0)
                    j += 1

            direction = strategy.calculate(training, interval * 60, col1, col2, col3, C[0][0], C[0][1])
            y = direction * max(sh_decrease)

            if strategyFlag == "polyfit_" or strategyFlag == "center_":
                # convert the line equation
                (a, b, c) = strategy.convert_line([direction, 0])
            if strategyFlag == "trendline_":
                (a, b, c) = strategy.convert_line(coeffs)

            out_point_line[interval] = {
                'a': a,
                'b': b,
                'c': c
            }

            out_point_point[interval] = {
                'cx': C[0][0],
                'cy': C[0][1],
            }

            # evaluate polynom
            yFitted = np.polyval(coeffs, sh_decrease)

            # plot graphs
            # plot points
            plt.scatter(sh_decrease, sh_diff, marker='x', color=colors_trendline[i], zorder=3)

            if not cluster_boundaries and not cluster_boundaries_all:
                # plot cluster centroid
                plt.scatter(C[0][0], C[0][1], marker='o', color=colors_trendline[i], zorder=3)

                if strategyFlag == 'polyfit_':
                    plt.plot([0, max(sh_decrease)], [0, y], color=colors_trendline[i], label=str(interval) + ' min')
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 7.0)
                    plt.grid(zorder=0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        return out_point_line, out_point_point, fig

                if strategyFlag == 'center_':
                    plt.plot([0, max(sh_decrease)], [0, y], color=colors_trendline[i], label=str(interval) + ' min')
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 6.0)
                    plt.grid(zorder=0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        return out_point_line, out_point_point, fig

                if strategyFlag == 'trendline_':
                    # plot trendline of the cluster
                    plt.plot(sh_decrease, yFitted, color=colors_trendline[i], label=str(interval) + ' min')
                    plt.grid(zorder=0)
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 6.0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        plt.ylim(0.0, 5.0)
                        return out_point_line, out_point_point, fig

            if cluster_boundaries or cluster_boundaries_all:
                plt.plot(C[0][0], C[0][1], marker="o", color=colors_trendline[i], markersize=10, markeredgecolor='k',
                     markeredgewidth=2)

                # plot filled boundaries
                xy = np.array([sh_decrease, sh_diff])
                xy = np.transpose(xy)

                # get boundaries
                hull = ConvexHull(xy)

                for simplex in hull.simplices:
                    plt.plot(xy[simplex, 0], xy[simplex, 1], '-k', linewidth=1.0)

                plt.fill(xy[hull.vertices, 0], xy[hull.vertices, 1], color=colors_line[i], label=str(interval) + ' min')
            i += 1

        if not one_line:
            plt.legend()
        plt.grid(zorder=0)

        return out_point_line, out_point_point, fig

    def distance_point_line(self, a1, a2, a, b, c):
        """ Calculates distance from point to line

        :param a1: point coordinate x
        :param a2: point coordinate y
        :param a: parameter of the line equation
        :param b: parameter of the line equation
        :param c: parameter of the line equation
        """

        return float(abs(a * a1 + b * a2 + c) / (np.sqrt(a ** 2 + b ** 2)))

    def distance_point_point_Euclidean(self, a1, a2, b1, b2):
        """ Calculates distance from point to point (Euclidean)

        :param a1: point 1 coordinate x
        :param a2: point 1 coordinate y
        :param b1: point 2 coordinate x
        :param b2: point 2 coordinate y
        """

        return float(np.sqrt((b1 - a1) ** 2 + (b2 - a2) ** 2))

    def exec(self, intervals, data_testing, col1, col2, col3, strategy, strategyFlag, one_line, test_points,
             cluster_boundaries, cluster_boundaries_all, precision=2):
        if self.model is None:
            line, point, fig = self.humidity_clusters(self.training, col1, col2, col3, intervals,
                                                      strategy, strategyFlag, one_line, cluster_boundaries,
                                                      cluster_boundaries_all)

            self.model = {
                'line' + strategyFlag: line,
                'point' + strategyFlag: point,
                'fig' + strategyFlag: fig,
            }

            if not cluster_boundaries:
                if strategyFlag == 'trendline_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('trendline.eps')

                if strategyFlag == 'polyfit_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('avg_trendline.eps')

                if strategyFlag == 'center_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('trendline_passing_cluster_centroid.eps')

            if one_line:
                return

            if cluster_boundaries:
                plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                plt.xlim(0.0, 5.0)
                plt.ylim(1.0, 6.0)
                self.model['fig' + strategyFlag].savefig('model.pdf')
                return

            if cluster_boundaries_all:
                plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                plt.xlim(0.0, 5.0)
                plt.ylim(1.0, 6.0)
                self.model['fig' + strategyFlag].savefig('model_all.pdf')
                return

        out = []
        for row in data_testing:
            dist_point_line = []
            dist_point_point = []
            x = float(row[col1]) - float(row[col2])
            y = float(row[col3])

            for interval in intervals:
                coeff = self.model['line' + strategyFlag][interval]

                # calculate the distance point-line
                dist = self.distance_point_line(x, y,
                                                float(coeff['a']),
                                                float(coeff['b']),
                                                coeff['c'])
                row['min_pl_' + strategyFlag + str(interval)] = round(dist, precision)
                dist_point_line.append(dist)
                coord = self.model['point' + strategyFlag][interval]

                # calculate the distance point-point
                dist = self.distance_point_point_Euclidean(x, y, coord['cx'], coord['cy'])
                row['min_pp_' + str(interval)] = round(dist, precision)
                dist_point_point.append(dist)

            out.append(row)

            if test_points:
                plt.scatter(x, y, 80, marker='o', color='black')
                fname = 'out_{0}_{1}.png'.format(x, y)
                title_graph = 'P = [%g, %g]' % (x, y)
                plt.title(title_graph)
                plt.xlabel('Decrease of $SH_{in}$ sensor 2 [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ sensor 2 [g/kg]')
                self.model['fig' +  strategyFlag].savefig(fname)
                plt.scatter(x, y, 80, marker='o', color='white')

        return out

    @staticmethod
    def select_attributes(data, attributes):
        out = []
        for row in data:
            new_row = []
            for key, value in row.items():
                if key in attributes:
                    new_row.append((key, value))
            out.append(OrderedDict(new_row))

        return out



