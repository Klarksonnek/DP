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
    ('2018/12/01 07:03:30', 'nothing'),
    ('2018/12/01 08:58:00', 'nothing'),
    ('2018/12/01 09:20:00', 'nothing'),
    ('2018/12/01 11:41:00', 'nothing'),
    ('2018/12/01 12:37:00', 'nothing'),
    ('2018/12/01 14:11:00', 'nothing'),
    ('2018/12/01 15:43:30', 'nothing'),
    ('2018/12/01 23:11:30', 'nothing'),
    ('2018/12/02 01:24:00', 'nothing'),
    ('2018/12/02 10:43:00', 'nothing'),

    ('2018/12/01 08:37:30', 'nothing'),
    ('2018/12/01 11:18:00', 'nothing'),
    ('2018/12/01 11:24:00', 'nothing'),
    ('2018/12/01 18:37:00', 'nothing'),
    ('2018/12/01 21:39:00', 'nothing'),
    ('2018/12/02 00:57:30', 'nothing'),
    ('2018/12/02 03:18:30', 'nothing'),
    #2018/12/02 08:26:30
    ('2018/12/02 11:36:00', 'nothing'),
    ('2018/12/02 12:50:00', 'nothing'),
    ('2018/12/02 18:52:00', 'nothing'),

    ('2018/12/01 09:38:00', 'nothing'),
    ('2018/12/01 11:42:00', 'nothing'),
    ('2018/12/01 17:50:30', 'nothing'),
    ('2018/12/02 05:14:30', 'nothing'),
    ('2018/12/02 06:55:00', 'nothing'),
    ('2018/12/02 08:26:30', 'nothing'),
    ('2018/12/02 13:19:30', 'nothing'),
    ('2018/12/02 15:11:00', 'nothing'),
    ('2018/12/02 19:15:30', 'nothing'),
    ('2018/12/02 20:03:30', 'nothing'),

    ('2018/12/01 06:23:30', 'nothing'),
    ('2018/12/01 08:28:00', 'nothing'),
    ('2018/12/01 09:38:00', 'nothing'),
    ('2018/12/01 09:48:00', 'nothing'),
    ('2018/12/02 03:17:00', 'nothing'),
    ('2018/12/02 15:08:30', 'nothing'),
    ('2018/12/02 17:07:00', 'nothing'),
    ('2018/12/02 17:16:30', 'nothing'),
    ('2018/12/03 05:04:00', 'nothing'),
    ('2018/12/03 15:07:30', 'nothing'),

    ('2018/12/01 07:28:00', 'nothing'),
    ('2018/12/01 12:45:30', 'nothing'),
    ('2018/12/02 08:51:00', 'nothing'),
    ('2018/12/02 21:41:00', 'nothing'),
    ('2018/12/03 02:20:30', 'nothing'),
    ('2018/12/03 04:53:00', 'nothing'),
    ('2018/12/03 04:59:00', 'nothing'),
    ('2018/12/03 15:07:30', 'nothing'),
    ('2018/12/03 23:19:30', 'nothing'),
    ('2018/12/04 07:01:30', 'nothing'),

    ('2018/12/01 11:20:00', 'nothing'),
    ('2018/12/02 05:14:30', 'nothing'),
    ('2018/12/02 14:37:00', 'nothing'),
    ('2018/12/02 17:08:00', 'nothing'),
    ('2018/12/03 06:45:30', 'nothing'),
    ('2018/12/03 23:19:30', 'nothing'),
    ('2018/12/04 06:27:30', 'nothing'),
    ('2018/12/04 10:10:00', 'nothing'),
    ('2018/12/04 17:48:30', 'nothing'),
    ('2018/12/04 21:01:30', 'nothing'),

    ('2018/12/01 12:48:00', 'nothing'),
    ('2018/12/02 14:53:30', 'nothing'),
    ('2018/12/03 05:31:30', 'nothing'),
    ('2018/12/03 06:45:00', 'nothing'),
    ('2018/12/03 23:13:00', 'nothing'),
    ('2018/12/03 23:19:30', 'nothing'),
    ('2018/12/05 17:14:00', 'nothing'),
    ('2018/12/06 09:24:00', 'nothing'),
    ('2018/12/06 13:53:30', 'nothing'),
    ('2018/12/06 17:45:30', 'nothing'),

    ('2018/12/02 15:01:30', 'nothing'),
    ('2018/12/02 15:06:30', 'nothing'),
    ('2018/12/04 13:29:30', 'nothing'),
    ('2018/12/06 06:50:30', 'nothing'),
    ('2018/12/06 16:43:00', 'nothing'),
    ('2018/12/06 21:15:30', 'nothing'),
    ('2018/12/06 23:28:00', 'nothing'),
    ('2018/12/07 07:36:30', 'nothing'),
    ('2018/12/07 14:01:30', 'nothing'),
    ('2018/12/07 15:39:30', 'nothing'),

    ('2018/12/02 14:58:00', 'nothing'),
    ('2018/12/03 20:46:00', 'nothing'),
    ('2018/12/04 15:45:30', 'nothing'),
    ('2018/12/05 06:29:00', 'nothing'),
    ('2018/12/07 08:09:00', 'nothing'),
    ('2018/12/07 14:01:30', 'nothing'),
    ('2018/12/07 18:52:00', 'nothing'),
    ('2018/12/07 23:11:30', 'nothing'),
    ('2018/12/08 10:14:30', 'nothing'),
    ('2018/12/08 10:30:00', 'nothing'),

    ('2018/12/01 14:21:00', 'nothing'),
    ('2018/12/01 17:00:30', 'nothing'),
    ('2018/12/03 02:22:00', 'nothing'),
    ('2018/12/04 17:08:30', 'nothing'),
    ('2018/12/06 06:50:30', 'nothing'),
    ('2018/12/06 23:26:30', 'nothing'),
    ('2018/12/07 14:01:30', 'nothing'),
    ('2018/12/08 14:05:00', 'nothing'),
    ('2018/12/13 20:15:00', 'nothing'),
    ('2018/12/14 07:03:00', 'nothing'),
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in_specific_g_kg',
        'rh_in_absolute_g_m3',
        'temperature_in_celsius']
    precision = 5

    for column in columns:
        for normalize in [False]:
            intervals_before = [x for x in range(0, 601, 15)]
            intervals_after = [x for x in range(0, 181, 15)]

            op = FirstDifferenceAttrA(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            pr = ''
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            # linearni posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            pr = 'B_linearne'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              normalize=normalize,
                              enable_count=True,
                              prefix='',
                              selected_before=[intervals_before],
                              selected_after=[intervals_after])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='')
            attrs += a + b

            # x^2 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(4, 25, 1)],
                              intervals_after=[x * x for x in range(4, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(4, 25, 1)]],
                              selected_after=[[x * x for x in range(4, 14, 1)]])
            attrs += a + b

            pr = 'B_x2'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x for x in range(4, 25, 1)],
                              intervals_after=[x * x for x in range(4, 14, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x2',
                              selected_before=[[x * x for x in range(4, 25, 1)]],
                              selected_after=[[x * x for x in range(4, 14, 1)]])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='_x2')
            attrs += a + b

            # x^3 posun
            op = FirstDifferenceAttrB(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(3, 9, 1)],
                              intervals_after=[x * x * x for x in range(3, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(3, 9, 1)]],
                              selected_after=[[x * x * x for x in range(3, 6, 1)]])
            attrs += a + b

            pr = 'B_x3'
            be, af = op.geometric_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.arithmetic_mean(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.variance(column, precision, b, a, pr)
            attrs += be + af
            be, af = op.standard_deviation(column, precision, b, a, pr)
            attrs += be + af

            op = SecondDifferenceAttr(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=[x * x * x for x in range(3, 9, 1)],
                              intervals_after=[x * x * x for x in range(3, 6, 1)],
                              normalize=normalize,
                              enable_count=True,
                              prefix='_x3',
                              selected_before=[[x * x * x for x in range(3, 9, 1)]],
                              selected_after=[[x * x * x for x in range(3, 6, 1)]])
            attrs += a + b

            op = DifferenceBetweenRealLinear(con, table_name, row_selector, interval_selector)
            a, b = op.execute(timestamp=timestamp, column=column, precision=precision,
                              intervals_before=intervals_before,
                              intervals_after=intervals_after,
                              window_size_before=15 * 60, window_size_after=3 * 60,
                              prefix='_x3')
            attrs += a + b

    return attrs


def main(events_file: str, no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_klarka_shower'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'rh_in_specific_g_kg')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    #filtered = FilterUtil.temperature_diff(filtered, 5, 100)
    #filtered = FilterUtil.temperature_out_max(filtered, 15)
    #filtered = FilterUtil.humidity(filtered, 6, 1.6, 100)
    filtered = FilterUtil.min_length(filtered, 5 * 60)
    logging.info('events after applying the filter: %d' % len(filtered))

    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = SimpleIntervalSelector(con, table_name)

    logging.info('start computing of training set')
    training, tr_events = AttributeUtil.training_data(con, table_name, filtered, func,
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

    # testovacia mnozina
    start = int(DateTimeUtil.local_time_str_to_utc('2018/12/01 06:00:00').timestamp())
    end = start + 100
    #end = start + 30*24*3600

    logging.info('start computing of testing set')
    length = AttributeUtil.testing_data_with_write(con, table_name, start, end, 30, func,
                                                   None, interval_selector, 'open', 'testing.csv')
    logging.info('testing set contains %d records' % length)
    logging.info('end computing of testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka_shower.json', -500)
