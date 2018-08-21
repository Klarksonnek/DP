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
    storage.read_meta_data('../devices_klarka.json', '../events_klarka.json')

    dw1 = storage.download_data_for_normalization(['temperature_in'])
    dw2 = storage.download_data_for_normalization(['humidity_in'])
    dw3 = storage.download_data_for_normalization(['temperature_out'])
    dw4 = storage.download_data_for_normalization(['humidity_out'])
    client.logout()

    one_norm_graph = []
    graphs = []

    for i in range(0, len(dw1)):
        one_values_temp_in = dw1[i]['data'][0]['values'][0]['measured']
        norm_values_temp_in = dp.compute_norm_values(one_values_temp_in)
        one_values_hum_in = dw2[i]['data'][0]['values'][0]['measured']
        norm_values_hum_in = dp.compute_norm_values(one_values_hum_in)
        one_values_temp_out = dw3[i]['data'][0]['values'][0]['measured']
        norm_values_temp_out = dp.compute_norm_values(one_values_temp_out)
        one_values_hum_out = dw4[i]['data'][0]['values'][0]['measured']
        norm_values_hum_out = dp.compute_norm_values(one_values_hum_out)

        g = {
            'title': 'Temp in and hum in',
            'graphs': [
                dp.gen_simple_graph(norm_values_temp_in, 'red', 'temp in', 'norm'),
                dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in', 'norm')
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Temp out and hum out',
            'graphs': [
                dp.gen_simple_graph(norm_values_temp_out, 'red', 'temp out', 'norm'),
                dp.gen_simple_graph(norm_values_hum_out, 'blue', 'hum out', 'norm')
            ]
        }
        graphs.append(g)

        g = {
                'title': 'Temp in and temp out',
            'graphs': [
                dp.gen_simple_graph(norm_values_temp_in, 'DarkRed', 'temp in', 'value'),
                dp.gen_simple_graph(norm_values_temp_out, 'LightCoral', 'temp out', 'value')
            ]
        }

        graphs.append(g)

        g = {
            'title': 'Hum in and hum out',
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'DarkBlue', 'hum in', 'value'),
                dp.gen_simple_graph(norm_values_hum_out, 'DarkTurquoise', 'hum out', 'value')
            ]
        }

        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
