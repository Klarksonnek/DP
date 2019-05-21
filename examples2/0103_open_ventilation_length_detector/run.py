"""

"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm import CSVUtil, Storage, FilterUtil
from dm.AttributeUtil import AttributeUtil
from dm.CSVUtil import CSVUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.FilterUtil import FilterUtil
from dm.Storage import Storage
from dm.attrs.DiffInLinear import DiffInLinear
from dm.attrs.InLinear import InLinear
from dm.attrs.InOutDiff import InOutDiff
from dm.attrs.VentilationLength import VentilationLength
from dm.coefficients.CenterLineCoefficients import CenterLineCoefficients
from dm.coefficients.DistanceToLine import DistanceToLine
from dm.coefficients.PolyfitLineCoefficients import PolyfitLineCoefficients
from dm.selectors.interval.SimpleIntervalSelector import SimpleIntervalSelector
from dm.selectors.row.CachedDiffRowWithIntervalSelector import CachedDiffRowWithIntervalSelector
import copy
import logging
import random

__author__ = ''
__email__ = ''


no_events_records = [
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in2_specific_g_kg_diff',
        'rh_in2_absolute_g_m3_diff',
        'temperature_in2_celsius_diff',
    ]
    precision = 5

    for column in columns:
        op = InOutDiff(con, table_name, row_selector, interval_selector)
        a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                          intervals_before=[0],
                          intervals_after=[],
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
    # all intervals
    # a, b = op.execute(event_start=timestamp, event_end=end, intervals=[5 * 60, 10 * 60, 15 * 60, 20 * 60, 25 * 60],
                      # threshold=120, prefix='')
    attrs += a + b

    op = DiffInLinear(con, table_name, row_selector, interval_selector)
    a, b = op.execute(timestamp_before=timestamp, timestamp_after=end,
                      column='rh_in2_specific_g_kg', precision=precision,
                      start_before=timestamp - 1200, end_before=timestamp,
                      start_after=end, end_after=end + 1200,
                      prefix='')

    attrs += a

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


def training_testing_data_with_distance(training, testing, number, strategy, strategyFlag, one_line, test_points,
                                        cluster_boundaries, cluster_boundaries_all):
    if cluster_boundaries_all:
        intervals = [5, 10, 15, 20, 25]
    else:
        intervals = [5, 10, 25]

    op = DistanceToLine(training)

    training = op.exec(intervals, training,
                       'InLinear_rh_in2_specific_g_kg_before_1200',
                       'InLinear_rh_in2_specific_g_kg_after_1200',
                       'InOutDiff_rh_in2_specific_g_kg_diff_before_0', strategy,  strategyFlag, one_line, test_points,
                       cluster_boundaries, cluster_boundaries_all)

    if one_line or cluster_boundaries or cluster_boundaries_all:
        return

    testing = op.exec(intervals, testing,
                      'InLinear_rh_in2_specific_g_kg_before_1200',
                      'InLinear_rh_in2_specific_g_kg_after_1200',
                      'InOutDiff_rh_in2_specific_g_kg_diff_before_0', strategy, strategyFlag, one_line, test_points,
                       cluster_boundaries, cluster_boundaries_all)

    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    CSVUtil.create_csv_file(training, 'training' + str(number) + '.csv')
    CSVUtil.create_csv_file(testing, 'testing' + str(number) + '.csv')
    logging.info('end preparing file of training and testing set')


def training_testing_data_only_distance(training, testing, number, strategy, strategyFlag, one_line, test_points,
                                        cluster_boundaries, cluster_boundaries_all):
    if cluster_boundaries_all:
        intervals = [5, 10, 15, 20, 25]
    else:
        intervals = [5, 10, 25]

    op = DistanceToLine(training)

    training = op.exec(intervals, training,
                       'InLinear_rh_in2_specific_g_kg_before_1200',
                       'InLinear_rh_in2_specific_g_kg_after_1200',
                       'InOutDiff_rh_in2_specific_g_kg_diff_before_0', strategy,  strategyFlag, one_line, test_points,
                       cluster_boundaries, cluster_boundaries_all)

    if one_line or cluster_boundaries or cluster_boundaries_all:
        return

    training = DistanceToLine.select_attributes(training, ['datetime', 'min_pp_5', 'min_pp_10', 'min_pp_25',
                                                           'min_pl_' + strategyFlag + '5',
                                                           'min_pl_' + strategyFlag + '10',
                                                           'min_' + strategyFlag + 'pl_25',
                                                           'VentilationLength_event__'])


    testing = op.exec([5, 10, 25], testing,
                      'InLinear_rh_in2_specific_g_kg_before_1200',
                      'InLinear_rh_in2_specific_g_kg_after_1200',
                      'InOutDiff_rh_in2_specific_g_kg_diff_before_0', strategy, strategyFlag, False, test_points,
                      cluster_boundaries, cluster_boundaries_all)
    testing = DistanceToLine.select_attributes(testing, ['datetime', 'min_pp_5', 'min_pp_10', 'min_pp_25',
                                                         'min_pl_' + strategyFlag + '5',
                                                         'min_pl_' + strategyFlag + '10',
                                                         'min_pl_' + strategyFlag + '25',
                                                         'VentilationLength_event__'])

    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    CSVUtil.create_csv_file(training, 'training' + str(number) + '.csv')
    CSVUtil.create_csv_file(testing, 'testing' + str(number) + '.csv')
    logging.info('end preparing file of training and testing set')


def training_testing_data_without_distance(training, testing, number, strategy, strategyFlag, one_line, test_points,
                                           cluster_boundaries, cluster_boundaries_all):
    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    CSVUtil.create_csv_file(training, 'training' + str(number) + '.csv')
    CSVUtil.create_csv_file(testing, 'testing' + str(number) + '.csv')
    logging.info('end preparing file of training and testing set')


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
    # filtered = FilterUtil.temperature_diff(filtered, 5, 17.5)
    # filtered = FilterUtil.temperature_diff(filtered, 17.5, 30)
    # filtered = FilterUtil.temperature_diff(filtered, 5, 13.3)
    # filtered = FilterUtil.temperature_diff(filtered, 13.3, 21.6)
    # filtered = FilterUtil.temperature_diff(filtered, 21.6, 30)
    # filtered = FilterUtil.temperature_diff(filtered, 10, 15)
    # filtered = FilterUtil.temperature_diff(filtered, 15, 20)
    # filtered = FilterUtil.temperature_diff(filtered, 20, 25)
    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = SimpleIntervalSelector(con, table_name)

    # datova mnozina
    logging.info('start computing of data set')
    data = AttributeUtil.training_data_without_opposite(con, table_name, filtered, func,
                                                        row_selector, interval_selector)
    logging.info('data set contains %d events' % len(data))
    logging.info('end computing of data set')

    # rozdelenie dat na trenovaciu a testovaciu mnozinu
    random.seed(len(data)//2)
    random.shuffle(data)
    training, testing, minimum = training_testing_data(data, 0.7)

    logging.info('training set contains %d records, each %d-krat' % (len(training), minimum))
    logging.info('testing set contains %d records' % len(testing))

    training_testing_data_with_distance(copy.deepcopy(training), copy.deepcopy(testing), 0,
                                        CenterLineCoefficients(), "trendline_", False, False, False, False)
    training_testing_data_with_distance(copy.deepcopy(training), copy.deepcopy(testing), 1,
                                        PolyfitLineCoefficients(), "polyfit_", False, False, False, False)
    training_testing_data_with_distance(copy.deepcopy(training), copy.deepcopy(testing), 2,
                                        CenterLineCoefficients(), "center_", False, False, False, False)
    training_testing_data_only_distance(copy.deepcopy(training), copy.deepcopy(testing), 3,
                                        CenterLineCoefficients(), "trendline_", False, False, False, False)
    training_testing_data_only_distance(copy.deepcopy(training), copy.deepcopy(testing), 4,
                                        PolyfitLineCoefficients(), "polyfit_", False, False, False, False)
    training_testing_data_only_distance(copy.deepcopy(training), copy.deepcopy(testing), 5,
                                        CenterLineCoefficients(), "center_", False, False, False, False)

    training_testing_data_without_distance(copy.deepcopy(training), copy.deepcopy(testing), 6,
                                           CenterLineCoefficients(), "trendline_", False, False, False, False)

    logging.info('end')


def main_test_pt(events_file_training: str, events_file_testing: str, no_event_time_shift: int):
    logging.info('start')

    table_name_training = 'measured_klarka'
    table_name_testing = 'measured_peto'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage_training = Storage(events_file_training, no_event_time_shift, table_name_training)
    d_training = storage_training.load_data(con, 0, 0, 'rh_in2_specific_g_kg')
    logging.info('downloaded events for training: %d' % len(d_training))

    storage_testing = Storage(events_file_testing, no_event_time_shift, table_name_testing)
    d_testing = storage_testing.load_data(con, 0, 0, 'temperature_in_celsius')
    logging.info('downloaded events for testing: %d' % len(d_testing))

    # aplikovanie filtrov na eventy
    filtered_training = FilterUtil.only_valid_events(d_training)
    filtered_training = FilterUtil.temperature_diff(filtered_training, 5, 100)
    filtered_training = FilterUtil.temperature_out_max(filtered_training, 15)
    filtered_training = FilterUtil.humidity(filtered_training, 6, 1.6, 100)

    # for travis
    if ConnectionUtil.is_testable_system():
        filtered_training = filtered_training[:ConnectionUtil.MAX_TESTABLE_EVENTS]

    logging.info('events for training after applying the filter: %d' % len(filtered_training))

    # aplikovanie filtrov na eventy
    filtered_testing = FilterUtil.only_valid_events(d_testing)
    filtered_testing = FilterUtil.temperature_diff(filtered_testing, 5, 100)
    filtered_testing = FilterUtil.temperature_out_max(filtered_testing, 15)
    filtered_testing = FilterUtil.humidity(filtered_testing, 6, 1.6, 100)

    # for travis
    if ConnectionUtil.is_testable_system():
        filtered_testing = filtered_testing[:ConnectionUtil.MAX_TESTABLE_EVENTS]

    logging.info('events for testing after applying the filter: %d' % len(filtered_testing))

    # selector pre data
    row_selector_training = CachedDiffRowWithIntervalSelector(con, table_name_training, 0, 0)
    interval_selector_training = SimpleIntervalSelector(con, table_name_training)

    # selector pre data
    row_selector_testing = CachedDiffRowWithIntervalSelector(con, table_name_testing, 0, 0)
    interval_selector_testing = SimpleIntervalSelector(con, table_name_testing)

    # datova mnozina
    logging.info('start computing of training set')
    data_training = AttributeUtil.training_data_without_opposite(con, table_name_training, filtered_training,
                                                                 func,
                                                                 row_selector_training, interval_selector_training)
    logging.info('training set contains %d events' % len(data_training))
    logging.info('end computing of training set')

    # datova mnozina
    logging.info('start computing of testing set')
    data_testing = AttributeUtil.training_data_without_opposite(con, table_name_testing, filtered_testing, func,
                                                                row_selector_testing, interval_selector_testing)
    logging.info('testing set contains %d events' % len(data_testing))
    logging.info('end computing of testing set')

    op = DistanceToLine(data_training)
    data_training = op.exec([5, 10], data_training,
                            'InLinear_rh_in2_specific_g_kg_before_1200',
                            'InLinear_rh_in2_specific_g_kg_after_1200',
                            'InOutDiff_rh_in2_specific_g_kg_diff_before_0')
    data_testing = op.exec([5, 10], data_testing,
                           'InLinear_rh_in2_specific_g_kg_before_1200',
                           'InLinear_rh_in2_specific_g_kg_after_1200',
                           'InOutDiff_rh_in2_specific_g_kg_diff_before_0')

    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    CSVUtil.create_csv_file(data_training, 'training.csv')
    CSVUtil.create_csv_file(data_testing, 'testing.csv')
    logging.info('end preparing file of training and testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka.json', -500)
    # main_test_pt('examples/events_klarka.json', 'examples/events_peto.json', -500)
