from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.CSVUtil import CSVUtil
from dm.Attributes import *


def main(events_file: str, intervals_before: list, intervals_after: list,
         no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_klarka'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'rh_in2_specific_g_kg')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    logging.info('start computing of training set')
    training = AttributeUtil.training_data(con, table_name, ['rh_in2_specific_g_kg'], filtered,
                                           intervals_before, intervals_after, 10)
    count = len(training)
    logging.info('training set contains %d events (%d records)' % (count/2, count))
    logging.info('end computing of training set')

    logging.info('start preparing file of training set')
    CSVUtil.create_csv_file(training, 'training.csv')
    logging.info('end preparing file of training set')

    logging.info('start computing of testing set')
    s = int(DateTimeUtil.local_time_str_to_utc('2018/11/30 22:50:00').timestamp())
    testing = AttributeUtil.testing_data(con, table_name, ['rh_in2_specific_g_kg'], s, s + 300,
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
    main('examples/events_klarka.json', before, after, -500)
