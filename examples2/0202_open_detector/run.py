from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.CSVUtil import CSVUtil
from dm.Attributes import *
from dm.GraphUtil import GraphUtil

no_events_records = [
]


def func(con, table_name, timestamp, row_selector, interval_selector):
    attrs = []
    columns = ['co2_in_ppm']
    precision = 2

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(5, 901, 10)]
            intervals_after = [x for x in range(5, 181, 10)]

            #
            # linearny posun
            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += b + a

            pr = ''
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            #
            # linearny posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += b + a

            pr = 'B_linearne'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=20*60, window_size_after=3*60,
                              prefix='')
            attrs += b + a

            #
            # x^2 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(2, 31, 1)]],
                              selected_after=[[x * x for x in range(2, 14, 1)]])
            attrs += b + a

            pr = 'B_x2'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(2, 31, 1)],
                              intervals_after=[x * x for x in range(2, 14, 1)],
                              window_size_before=20 * 60, window_size_after=3 * 60,
                              prefix='_x2')
            attrs += b + a

            #
            # x^3 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(2, 10, 1)]],
                              selected_after=[[x * x * x for x in range(2, 6, 1)]])
            attrs += b + a

            pr = 'B_x3'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(2, 10, 1)],
                              intervals_after=[x * x * x for x in range(2, 6, 1)],
                              window_size_before=20 * 60, window_size_after=3 * 60,
                              prefix='_x3')
            attrs += b + a

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column='co2_in_ppm_diff', precision=precision,
                          intervals_before=[1],
                          intervals_after=[],

                          prefix='_x3')
        attrs += b + a

    return attrs


def training_set(events_file: str, no_event_time_shift: int, table_name: str):
    logging.info('start')

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = None

    # trenovacia mnozina
    logging.info('start computing of training set')
    training, tr_events = AttributeUtil.training_data(con, table_name, filtered, func,
                                                      row_selector, interval_selector, 'open')
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count / 2, count))

    GraphUtil.gen_duration_histogram(tr_events, 'save', ['png'], 'Histogram dlzok vetrania',
                                     [x for x in range(5, 60, 5)], 1)

    training2 = AttributeUtil.additional_training_set(con, table_name, no_events_records, func,
                                                      row_selector, interval_selector)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')


def testing_set(table_name: str):
    logging.info('start')

    con = ConnectionUtil.create_con()

    # testovacia mnozina
    start = int(DateTimeUtil.local_time_str_to_utc('2018/10/07 06:00:00').timestamp())
    end = start + 100

    logging.info('start computing of testing set')
    length = AttributeUtil.testing_data_with_write(con, table_name, start, end, 30, func,
                                                   None, None, 'open', 'testing.csv')
    logging.info('testing set contains %d records' % length)
    logging.info('end computing of testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    table_name = 'measured_peto'

    training_set('examples/events_peto.json', -500, table_name)
    testing_set(table_name)
