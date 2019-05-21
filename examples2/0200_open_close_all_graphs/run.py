from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.ConnectionUtil import ConnectionUtil
from dm.DateTimeUtil import DateTimeUtil
from dm.FilterUtil import FilterUtil
from dm.Graph import Graph
from dm.Storage import Storage
from dm.co2regression.ExpRegressionWithDelay import ExpRegressionWithDelay
from dm.co2regression.SimpleExpRegression import SimpleExpRegression
import logging
import numpy as np


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


def compute_regression(events):
    out_ppm = 350

    for i in range(0, len(events)):
        event = events[i]
        measured = event['measured']['co2_in_ppm']

        x = []
        y = []
        shift = 0
        for k in range(shift, len(measured)):
            x.append(k - shift)
            y.append(measured[k])

        x = np.asarray(x)
        y = np.asarray(y)

        op = SimpleExpRegression(out_ppm, None)
        event['measured']['co2_in_ppm_exp'] = op.compute_curve(x, y)

        op = ExpRegressionWithDelay(out_ppm, None, 11, 20)
        event['measured']['co2_in_ppm_exp2'] = op.compute_curve(x, y)

    return events


def generate_file(con, start_shift, end_shift, output_file, enable_regression):
    logging.info('start: ' + output_file)

    graphs = Graph("./../../src/graph")

    # stiahnutie dat
    storage = Storage('examples/events_peto.json', 0, 'measured_filtered_peto')
    d = storage.load_data(con, start_shift, end_shift, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    # spocitanie regresie
    if enable_regression:
        filtered = compute_regression(filtered)

    logging.info('start generating graphs')
    gr = []
    for event in filtered:
        t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
        t += ' - '
        t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

        if enable_regression:
            gg = [
                Graph.db_to_simple_graph(event, 'co2_in_ppm', 'green', 'CO2', 50),
                Graph.db_to_simple_graph(event, 'co2_in_ppm_exp', 'red', 'SimpleExpRegression', 50),
                Graph.db_to_simple_graph(event, 'co2_in_ppm_exp2', 'orange', 'ExpRegressionWithDelay', 50),
            ]
        else:
            gg = [
                Graph.db_to_simple_graph(event, 'co2_in_ppm', 'green', 'CO2', 50),
            ]

        g = {
            'title': t,
            'graphs': gg
        }
        gr.append(g)

    graphs.gen(gr, output_file + '.html', 0, 0)
    logging.info('end generating graphs')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', )

    con = ConnectionUtil.create_con()

    generate_file(con, -1800, +1800, 'inner_co2_with_shift', False)
    generate_file(con, 0, 0, 'inner_co2', True)
