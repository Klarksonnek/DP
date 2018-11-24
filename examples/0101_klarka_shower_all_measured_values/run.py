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
    client.api_key = dp.api_key(CODE_DIR + '/config.ini')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_klarka.json', '../events_klarka_shower.json')

    dw1 = storage.download_data_for_normalization(['temperature_bathroom_i', 'temperature_bathroom_ii'])
    dw2 = storage.download_data_for_normalization(['humidity_bathroom_i', 'humidity_bathroom_ii'])

    one_norm_graph = []
    graphs = []

    for i in range(0, len(dw1)):
        one_values_temp_in = dw1[i]['data'][0]['values'][0]['measured']
        one_values_hum_in = dw2[i]['data'][0]['values'][0]['measured']
        norm_values_hum_in = dp.compute_norm_values(one_values_hum_in)
        norm_values_temp_in = dp.compute_norm_values(one_values_temp_in)

        g = {
            'title': 'Temp in and hum in',
            'graphs': [
                dp.gen_simple_graph(norm_values_temp_in, 'red', 'temp in', 'value_norm', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in', 'value_norm', 100)
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
