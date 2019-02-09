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


def func(con, table_name, timestamp, selector):
    attrs = []
    columns = ['co2_in_ppm']
    precision = 2

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(5, 601, 15)]
            intervals_after = [x for x in range(5, 181, 10)]

            op = FirstDifferenceAttrA(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            # linearny posun
            op = FirstDifferenceAttrB(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            op = SecondDifferenceAttr(con, table_name, selector)
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
            op = SecondDifferenceAttr(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x*x for x in range(2, 25, 1)],
                              intervals_after=[x*x for x in range(2, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

            # x^3 posun
            op = SecondDifferenceAttr(con, table_name, selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x*x*x for x in range(2, 9, 1)],
                              intervals_after=[x*x*x for x in range(2, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[],
                              selected_after=[])
            attrs += a + b

    return attrs


def main(events_file: str, no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_peto'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    selector = SimpleCachedRowSelector(con, table_name)

    # trenovacia mnozina
    logging.info('start computing of training set')
    training = AttributeUtil.training_data(con, table_name, filtered, func, selector)
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count/2, count))

    training2 = AttributeUtil.additional_training_set(con, table_name, no_events_records, func, selector)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')

    # testovacia mnozina
    start = int(DateTimeUtil.local_time_str_to_utc('2018/12/1 07:28:28').timestamp())

    logging.info('start computing of testing set')
    testing = AttributeUtil.testing_data(con, table_name, start, start + 100, 30, func, selector)
    logging.info('testing set contains %d records' % len(testing))
    logging.info('end computing of testing set')

    logging.info('start preparing file of testing set')
    CSVUtil.create_csv_file(testing, 'testing.csv')
    logging.info('end preparing file of testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_peto.json', -500)
