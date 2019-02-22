from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Attributes import *

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sympy import var
from fractions import Fraction
from dm.CSVUtil import CSVUtil

no_events_records = [
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in2_specific_g_kg_diff',
        'rh_in2_absolute_g_m3_diff',
        'rh_in2_percentage_diff',
        'temperature_in2_celsius_diff']
    precision = 5

    for column in columns:
        intervals_before = [x for x in range(0, 61, 15)]
        intervals_after = [x for x in range(0, 61, 15)]

        op = InOutDifference(con, table_name, row_selector, interval_selector)
        a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                          intervals_before=intervals_before,
                          intervals_after=intervals_after,
                          prefix='')
        attrs += a + b

        op = InLinear(con, table_name, row_selector, interval_selector)
        a, b = op.execute(timestamp_before=timestamp, timestamp_after=end,
                          column='rh_in2_specific_g_kg', precision=precision,
                          start_before=timestamp - 1200, end_before=timestamp,
                          start_after=end, end_after=end + 1200,
                          prefix='')
        attrs += a + b

        op = VentilationLength(con, table_name, row_selector, interval_selector)
        a, b = op.execute(event_start=timestamp, event_end=end, intervals=[5*60, 10*60, 25*60],
                          threshold=120, prefix='')
        attrs += a + b

    return attrs


def training_testing_data(data, splitting):
    length_map = {}
    for row in data:
        attr_value = row['VentilationLength_event__']

        if attr_value in length_map:
            length_map[attr_value] += 1
        else:
            length_map[attr_value] = 1

    minimum = None
    for _, value in length_map.items():
        if minimum is None:
            minimum = value
        else:
            if minimum > value:
                minimum = value

    minimum = round(minimum * splitting)
    for key, value in length_map.items():
        length_map[key] = minimum

    training = []
    testing = []
    for row in data:
        attr_value = row['VentilationLength_event__']

        if length_map[attr_value] > 0:
            training.append(row)
            length_map[attr_value] -= 1
        else:
            testing.append(row)

    return training, testing, minimum


def ventilation_length_events(training: list, ventilation_length: int):
    out = []

    for row in training:
        #ventilation_len = "'" + str(ventilation_length) + "'"
        if row['VentilationLength_event__'] == str(ventilation_length):
            out.append(row)

    return out


def ventilation_length_count(data: list, intervals: list):
    out = {}

    for interval in intervals:
        i = 0
        for item in data:
            if int(item['VentilationLength_event__']) == interval * 60:
                i += 1

        out[interval] = i

    return out


def convert_line_to_general(coeffs):
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


def distance_point_line(a1, a2, a, b, c):
    """ Calculates distance from point to line

    :param a1: point coordinate x
    :param a2: point coordinate y
    :param a: parameter of the line equation
    :param b: parameter of the line equation
    :param c: parameter of the line equation
    """

    return float(abs(a * a1 + b * a2 + c) / (np.sqrt(a**2 + b**2)))


def humidity_clusters(training, col1, col2, col3, intervals):
    # colors
    colors = ['red', 'green', 'blue', 'magenta', 'cyan']
    # counter for colors
    i = 0
    fig = plt.figure()
    leg = []
    out = {}

    for interval in intervals:
        sh_decrease = []
        sh_diff = []
        for res in ventilation_length_events(training, interval * 60):
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

        # convert the line equation
        (a, b, c) = convert_line_to_general(coeffs)
        out[interval] = {
            'a': a,
            'b': b,
            'c': c
        }

        # evaluate polynom
        yFitted = np.polyval(coeffs, sh_decrease)

        # plot graphs
        # plot points
        plt.scatter(sh_decrease, sh_diff, marker='x', color=colors[i])

        # plot cluster centroid
        plt.scatter(C[0][0], C[0][1], marker='o', color=colors[i])

        # plot trendline of the cluster
        plt.plot(sh_decrease, yFitted, color=colors[i])

        leg.append(str(intervals[i]) + ' min')

        i += 1

    plt.legend(leg)
    plt.grid()

    return out, fig


def testing_evaluation(testing, intervals, coefficients, fig):

    # calculate the distance point-line
    success = 0
    for row in testing:
        dist = []
        x = float(row['InLinear_rh_in2_specific_g_kg_before_1200'])
        x -= float(row['InLinear_rh_in2_specific_g_kg_after_1200'])
        y = float(row['InOutDifference_rh_in2_specific_g_kg_diff_before_0'])

        for interval in intervals:
            coeff = coefficients[interval]
            dist_curr = distance_point_line(x, y, float(coeff['a']), float(coeff['b']), coeff['c'])
            dist.append(dist_curr)

        # minumum distance
        min_i = dist.index(min(dist))

        real_interval = int(row['VentilationLength_event__']) // 60

        logging.info('ideal ventilation interval: %s' % intervals[min_i])
        logging.info('real ventilation interval: %s' % real_interval)

        if intervals[min_i] == real_interval:
            success += 1

        plt.scatter(x, y, 80, marker='o', color='black')
        fname = 'out_{0}_{1}.png'.format(x, y)
        title_graph = 'P = [%g, %g], predict: %g min, real: %g min, point-line\n' % (x, y, intervals[min_i],
                                                                                     real_interval)
        plt.title(title_graph)
        fig.savefig(fname)

        plt.scatter(x, y, 80, marker='o', color='white')

    return success / len(testing)


def diff(data, col, min_value, max_value):
    out = []
    for item in data:
        if min_value <= item[col] <= max_value:
            out.append(item)

    return out


def main(events_file: str, no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_klarka'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'rh_in2_specific_g_kg')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    filtered = FilterUtil.temperature_diff(filtered, 5, 100)
    filtered = FilterUtil.temperature_out_max(filtered, 15)
    filtered = FilterUtil.humidity(filtered, 6, 1.6, 100)
    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    row_selector = SimpleDiffRowSelector(con, table_name)
    interval_selector = SimpleIntervalSelector(con, table_name)

    # datova mnozina
    logging.info('start computing of data set')
    data = AttributeUtil.training_data_without_opposite(con, table_name, filtered, func,
                                                        row_selector, interval_selector)
    logging.info('data set contains %d events' % len(data))
    logging.info('end computing of data set')

    events = ventilation_length_events(data, 1500)
    CSVUtil.create_csv_file(events, 'humidity_info_25_minut.csv')

    # aplikovanie filtrov na data
    data = diff(data, 'InOutDifference_temperature_in2_celsius_diff_before_0', 05.0, 25.0)

    counts = ventilation_length_count(data, [5, 10, 25])
    logging.debug("counts: %s" % counts)

    # rozdelenie dat na trenovaciu a testovaciu mnozinu
    training, testing, minimum = training_testing_data(data, 0.7)
    logging.info('training set contains %d records, each %d-krat' % (len(training), minimum))
    logging.info('testing set contains %d records' % len(testing))

    intervals = [5, 10, 25]
    out, fig = humidity_clusters(training,
                                 'InLinear_rh_in2_specific_g_kg_before_1200',
                                 'InLinear_rh_in2_specific_g_kg_after_1200',
                                 'InOutDifference_rh_in2_specific_g_kg_diff_before_0',
                                 intervals)

    success_rate = testing_evaluation(testing, intervals, out, fig)

    logging.info('success rate: %s' % round(success_rate, 2))

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka.json', -500)
