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


def main(events_file: str, intervals_before: list, intervals_after: list,
         no_event_time_shift: int):
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

    # trenovacia mnozina
    logging.info('start computing of training set')
    training = AttributeUtil.training_data(con, table_name, ['co2_in_ppm'], filtered,
                                           intervals_before, intervals_after, 10)
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count/2, count))

    training2 = AttributeUtil.additional_training_set(con, table_name, ['co2_in_ppm'],
                                                      no_events_records,
                                                      intervals_before, intervals_after, 10)
    count2 = len(training2)
    logging.info('additional training set contains %d records' % count2)

    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    balanced = AttributeUtil.balance_set(training, training2)
    CSVUtil.create_csv_file(balanced, 'training.csv')
    logging.info('end preparing file of training set')

    # testovacia mnozina
    logging.info('start computing of testing set')
    s = int(DateTimeUtil.local_time_str_to_utc('2018/12/1 07:28:28').timestamp())
    testing = AttributeUtil.testing_data(con, table_name, ['co2_in_ppm'], s, s + 300,
                                         intervals_before, intervals_after, 10, 30)
    logging.info('testing set contains %d records' % len(testing))
    logging.info('end computing of testing set')

    logging.info('start preparing file of testing set')
    CSVUtil.create_csv_file(testing, 'testing.csv')
    logging.info('end preparing file of testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    before = [60, 75, 90]
    after = [60, 75, 90]
    main('examples/events_peto.json', before, after, -500)
