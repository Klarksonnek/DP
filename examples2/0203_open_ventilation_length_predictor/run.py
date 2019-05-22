"""CO2 ventilation length predictor.
"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))


from dm.AttributeUtil import AttributeUtil
from dm.CSVUtil import CSVUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.FilterUtil import FilterUtil
from dm.Storage import Storage
from dm.attrs.CO2VentilationLength import CO2VentilationLength
from dm.attrs.InOutDiff import InOutDiff
from dm.attrs.Regression import Regression
from dm.co2regression.SimpleExpRegression import SimpleExpRegression
from dm.selectors.interval.CachedDiffRowWithIntervalSelector import CachedDiffRowWithIntervalSelector
import logging
import random

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


no_events_records = [
]


def func(con, table_name, timestamp, row_selector, interval_selector, end=None):
    attrs = []
    columns = [
        'rh_in_specific_g_kg_diff',
        'rh_in_absolute_g_m3_diff',
        'temperature_in_celsius_diff',
        'co2_in_ppm_diff'
    ]
    precision = 2

    for column in columns:
        intervals_before = [1]
        intervals_after = []

        op = InOutDiff(con, table_name, row_selector, interval_selector)
        b, a = op.execute(timestamp=timestamp, column=column, precision=precision,
                          intervals_before=intervals_before,
                          intervals_after=intervals_after,
                          prefix='')
        attrs += b + a

    model = SimpleExpRegression(350, None)
    op = CO2VentilationLength(con, table_name, row_selector, interval_selector)
    b, a = op.execute(timestamp_start=timestamp, timestamp_end=end,
                      compute_timestamp=5*60, intervals=[], method=model,
                      co2_out=350,
                      column='co2_in_ppm', precision=0, prefix='')
    attrs += b + a

    model = SimpleExpRegression(350, None)
    op = Regression(con, table_name, row_selector, interval_selector, model)
    b, a = op.execute(timestamp_start=timestamp, timestamp_end=end,
                      column='co2_in_ppm', precision=0, prefix='', enable_error=False)
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

    # for travis
    if ConnectionUtil.is_testable_system():
        filtered = filtered[:ConnectionUtil.MAX_TESTABLE_EVENTS]

    logging.info('events after applying the filter: %d' % len(filtered))

    # selector pre data
    row_selector = CachedDiffRowWithIntervalSelector(con, table_name, 0, 0)
    interval_selector = None

    # datova mnozina
    logging.info('start computing of data set')
    data = AttributeUtil.training_data_without_opposite(con, table_name, filtered, func,
                                                        row_selector, interval_selector)
    logging.info('data set contains %d events' % len(data))
    logging.info('end computing of data set')

    # generovanie suborov
    logging.info('start preparing file of training and testing set')
    random.seed(len(data) // 2)
    random.shuffle(data)

    CSVUtil.create_csv_file(data, 'data.csv')
    logging.info('end preparing file of training and testing set')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    table_name = 'measured_filtered_peto'
    training_set('examples/events_peto.json', -500, table_name)
