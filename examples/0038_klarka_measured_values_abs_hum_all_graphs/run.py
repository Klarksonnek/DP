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

    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'temperature_in', 'humidity_in')
    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'temperature_out', 'humidity_out')
    all = dp.convert_absolute_humidity_to_relative_humidity(all, 'temperature_in', 'humidity_out')

    norm = dp.norm_all(all)
    filtered = storage.filter_downloaded_data(norm, 'temperature_in', 'value',
                                              'temperature_out', 'value', 0.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'relative_humidity_in', 5.0, 100.0)
    #filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value', 30.0)
    #filtered = storage.filter_downloaded_data_general_attribute(filtered, "window", "ventilacka")

    one_norm_graph = []
    graphs = []

    for i in range(0, len(filtered)):
        norm_values_temp_in = dp.filter_one_values(filtered[i], 'temperature_in')
        norm_values_hum_in = dp.filter_one_values(filtered[i], 'humidity_in')
        norm_values_temp_out = dp.filter_one_values(filtered[i], 'temperature_out')
        norm_values_hum_out = dp.filter_one_values(filtered[i], 'humidity_out')

        g = {
            'title': 'Hum in - partial pressure',
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'DarkBlue', 'hum in', 'absolute_humidity'),
                dp.gen_simple_graph(norm_values_hum_out, 'DarkTurquoise', 'hum out', 'absolute_humidity')
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0, 'line', global_range=True)
