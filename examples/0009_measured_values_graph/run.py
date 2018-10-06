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

    dw1 = storage.download_data_for_normalization(['co2'])

    norm = dp.norm_all(dw1)
    values = dp.filter_one_values(norm[0], 'co2')

    graph1 = {
        'title': 'Normalizovane namerane hodnoty',
        'graphs': [
            dp.gen_simple_graph(values, 'green', 'Namerana hodnota <0, 1>', 'value_norm', 30)
        ]
    }

    graph2 = {
        'title': 'Namerane hodnoty',
        'graphs': [
            dp.gen_simple_graph(values, 'green', 'Namerana hodnota', 'value', 30)
        ]
    }

    g = dp.Graph("./../../src/graph")
    g.gen([graph1, graph2], 'test_g.html', 0, 0)
