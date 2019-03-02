from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.CSVUtil import CSVUtil
from dm.Attributes import *

no_events_records = [
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in2_specific_g_kg',
        'rh_in2_absolute_g_m3']
    precision = 5

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(15, 601, 30)]
            intervals_after = [x for x in range(15, 181, 30)]

            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            # linearni posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            # x^2 posun
            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(4, 25, 1)],
                              intervals_after=[x * x for x in range(4, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            # x^3 posun
            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(3, 9, 1)],
                              intervals_after=[x * x * x for x in range(3, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

    return attrs


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

    row_selector = SimpleDiffRowSelector(con, table_name)
    interval_selector = SimpleIntervalSelector(con, table_name)

    logging.info('start computing of training set')
    training = AttributeUtil.training_data(con, table_name, filtered, func,
                                           row_selector, interval_selector, 'open')

    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count/2, count))
    training2 = AttributeUtil.additional_training_set(con, table_name, no_events_records, func,
                                                      row_selector, interval_selector)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')

    s = int(DateTimeUtil.local_time_str_to_utc('2018/12/26 06:00:00').timestamp())

    logging.info('start computing of testing set')
    testing = AttributeUtil.testing_data(con, table_name, s, s + 300, 30, func,
                                         row_selector, interval_selector, 'open')
    logging.info('testing set contains %d records' % len(testing))
    logging.info('end computing of testing set')

    logging.info('start preparing file of testing set')
    CSVUtil.create_csv_file(testing, 'testing.csv')
    logging.info('end preparing file of testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka.json', -500)
