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

    one_values = dw1[0]['data'][0]['values'][0]['measured']
    norm_values = dp.compute_norm_values(one_values)

    graph1 = {
        'title': 'Normalizovane namerane hodnoty',
        'graphs': [
            dp.gen_simple_graph(norm_values, 'green', 'Namerana hodnota <0, 1>', 'norm')
        ]
    }

    graph2 = {
        'title': 'Namerane hodnoty',
        'graphs': [
            dp.gen_simple_graph(norm_values, 'green', 'Namerana hodnota')
        ]
    }

    g = dp.Graph("./../../src/graph")
    g.gen([graph1, graph2], 'test_g.html', 0, 0)
