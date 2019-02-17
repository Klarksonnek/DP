import logging
import sys
from os.path import dirname, abspath, join

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Graph import Graph
from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage


def check_attributes(events):
    wind = ['calm', 'light', 'medium', 'strong']
    sky = ['clear', 'partly_cloudy', 'overcast', 'smog', 'night_sky']
    sun = ['yes', 'no']
    rain = ['yes', 'no']

    for item in events:
        if item['wind'] not in wind:
            raise ValueError('wind attribute contains invalid input: %s' % item['wind'])

        if item['sky'] not in sky:
            raise ValueError('sky attribute contains invalid input: %s' % item['sky'])

        if item['sun'] not in sun:
            raise ValueError('sun attribute contains invalid input: %s' % item['sun'])

        if item['rain'] not in rain:
            raise ValueError('rain attribute contains invalid input: %s' % item['rain'])


def generate_file(con, start_shift, end_shift, output_file):
    logging.info('start: ' + output_file)

    graphs = Graph("./../../src/graph")

    # stiahnutie dat
    storage = Storage('examples/events_peto.json', 0, 'measured_peto')
    d = storage.load_data(con, start_shift, end_shift, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    logging.info('start generating graphs')
    gr = []
    for event in filtered:
        t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
        t += ' - '
        t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

        g = {
            'title': t,
            'graphs': [
                Graph.db_to_simple_graph(event, 'co2_in_ppm', 'green', 'CO2', 50)
            ]
        }
        gr.append(g)

    graphs.gen(gr, output_file + '.html', 0, 0)
    logging.info('end generating graphs')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', )

    con = ConnectionUtil.create_con()

    generate_file(con, -1800, +1800, 'inner_co2_with_shift')
    generate_file(con, 0, 0, 'inner_co2')
