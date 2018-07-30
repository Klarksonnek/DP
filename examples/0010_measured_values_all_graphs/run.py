#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_examples.json', '../events_examples.json')

    dw1 = storage.download_data_for_normalization(type_id='co2')
    client.logout()

    one_norm_graph = []
    graphs = []

    for i in range(0, len(dw1)):
        one_values = dw1[i]['data'][0]['values'][0]['measured']
        norm_values = dp.compute_norm_values(one_values)

        norm_graph = dp.gen_simple_graph(norm_values, dp.COLORS[i], 'Namerana hodnota', 'norm')
        one_norm_graph.append(norm_graph)

        g = {
            'title': 'Measured values',
            'graphs': [
                dp.gen_simple_graph(norm_values, 'green', 'Namerana hodnota', 'norm')
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Measured values',
            'graphs': [
                dp.gen_simple_graph(norm_values, 'green', 'Namerana hodnota', 'value')
            ]
        }

        graphs.append(g)

    graphs.append({
        'title': 'Measured values',
        'graphs': one_norm_graph
    })

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
