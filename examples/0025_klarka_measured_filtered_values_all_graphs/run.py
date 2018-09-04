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

    modules = ['temperature_in', 'humidity_in', 'temperature_out', 'humidity_out']
    all = storage.download_data_for_normalization(modules)

    client.logout()

    norm = dp.norm_all(all)
    dw1 = dp.filter_data(norm, ['temperature_in'])
    dw2 = dp.filter_data(norm, ['humidity_in'])
    dw3 = dp.filter_data(norm, ['temperature_out'])
    dw4 = dp.filter_data(norm, ['humidity_out'])

    dw1_filtered, dw2_filtered, dw3_filtered, dw4_filtered =\
        storage.filter_downloaded_data(dw1, dw2, dw3, dw4, 5.0, 10.0, 10.0, 20.0)

    one_norm_graph = []
    graphs = []

    for i in range(0, len(dw1_filtered)):
        norm_values_temp_in = dp.filter_one_values(dw1_filtered[i], 'temperature_in')
        norm_values_hum_in = dp.filter_one_values(dw2_filtered[i], 'humidity_in')
        norm_values_temp_out = dp.filter_one_values(dw3_filtered[i], 'temperature_out')
        norm_values_hum_out = dp.filter_one_values(dw4_filtered[i], 'humidity_out')

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
