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
    client.logout()

    his_data = dp.gen_histogram(dw1, 10, 400, 2000, 200)
    data_from_histogram = dp.his_to_data_for_normalization(his_data, dp.his_first_value)

    graphs = []
    for i in range(0, len(dw1)):
        one_values = dw1[i]['data'][0]['values'][0]['measured']
        norm_values = dp.compute_norm_values(one_values)
        his = data_from_histogram['data'][0]['values'][0]['measured']

        g = {
            'title': 'Estimate of measured values',
            'graphs': [
                dp.gen_simple_graph(norm_values, 'green', 'Namerana hodnota', 'norm'),
                dp.value_estimate(data_from_histogram, 6, 'red', 'Odhadnuta hodnota', 'norm'),
                dp.gen_simple_graph(his, 'blue', 'Idealny graf', 'norm')
            ]
        }

        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
