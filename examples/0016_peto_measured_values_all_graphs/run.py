#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import datetime
import env_dp.core as dp
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_peto.json', '../events_peto.json')

    dw1 = storage.download_data_for_normalization(['co2'])
    client.logout()

    norm = dp.norm_all(dw1)

    graphs = []

    # True ak sa maju zobrazit aj grafy s nameranou hodnotou
    enable_value_graph = False

    for item in norm:
        one_values = dp.filter_one_values(item, 'co2')
        norm_values = one_values

        start = item['times']['event_start']
        end = item['times']['event_end']

        t = datetime.datetime.fromtimestamp(start).strftime('%d.%m. %H:%M:%S')
        t += ' - '
        t += datetime.datetime.fromtimestamp(end).strftime('%H:%M:%S')

        g = {
            'title': t,
            'graphs': [
                dp.gen_simple_graph(norm_values, 'green', 'CO2', 'norm')
            ]
        }
        graphs.append(g)

        if not enable_value_graph:
            continue

        g = {
            'title': 'Namerana hodnota',
            'graphs': [
                dp.gen_simple_graph(norm_values, 'green', 'CO2', 'value')
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
