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
        'rh_in_specific_g_kg_diff',
        'rh_in_absolute_g_m3_diff',
        'rh_in_percentage_diff',
        'temperature_in_celsius_diff',
        'rh_in2_specific_g_kg_diff',
        'rh_in2_absolute_g_m3_diff',
        'rh_in2_percentage_diff',
        'temperature_in2_celsius_diff']
    precision = 5

    for column in columns:
        intervals_before = [x for x in range(15, 61, 15)]
        intervals_after = [x for x in range(15, 61, 15)]

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

    # rozdelenie dat na trenovaciu a testovaciu mnozinu
    training, testing, minimum = training_testing_data(data, 0.7)
    logging.info('training set contains %d records, each %d-krat' % (len(training), minimum))
    logging.info('testing set contains %d records' % len(testing))

    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    CSVUtil.create_csv_file(training, 'training.csv')
    CSVUtil.create_csv_file(testing, 'testing.csv')
    logging.info('end preparing file of training and testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka.json', -500)
