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

    # kwargs
    start = int(DateTimeUtil.local_time_str_to_utc('2018/12/1 07:28:28').timestamp())
    kwargs = {
        'con': con,
        'table_name': table_name,
        'columns': ['co2_in_ppm'],
        'events': filtered,
        'intervals_before': [x for x in range(15, 45, 15)],
        'intervals_after': [x for x in range(15, 45, 15)],
        'value_delay': [x for x in range(5, 10, 5)],
        'precision': 2,
        'start': start,
        'end': start + 100,
        'no_event_records': no_events_records,
        'write_each': 30,
        'counts': [x for x in range(5, 10, 5)],
        'delays': [x for x in range(5, 10, 5)],
        'step_yts': [x for x in range(5, 10, 5)],
        'window_sizes': [x for x in range(50, 65, 15)],
    }

    # trenovacia mnozina
    logging.info('start computing of training set')
    training = AttributeUtil.training_data(**kwargs)
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count/2, count))

    training2 = AttributeUtil.additional_training_set(**kwargs)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')

    # testovacia mnozina
    logging.info('start computing of testing set')
    testing = AttributeUtil.testing_data(**kwargs)
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
