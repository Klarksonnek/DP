#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging


if __name__ == '__main__':
    # Nutne zrevidovat cely priklad a pouzivane funkcie
    exit(0)

    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_examples.json', '../events_examples.json')

    dw1 = storage.download_data_for_normalization(['co2'])

    his_data = dp.gen_histogram(dw1, 10, 400, 2000, 200, 'value')

    estimate_values = [dp.his_to_data_for_normalization(his_data, dp.his_first_value)]

    graphs = []
    for item in dw1:
        one_values = dp.filter_one_values(item, 'co2')
        his_values = dp.filter_one_values(estimate_values[0], 'estimate')

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.gen_simple_graph(one_values, 'green', 'Namerana hodnota', 'value_norm'),
                dp.value_estimate(estimate_values, 6, 'red', 'Odhadnuta hodnota', 'value_norm'),
                dp.gen_simple_graph(his_values, 'blue', 'Idealny graf', 'value_norm')
            ]
        }

        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
