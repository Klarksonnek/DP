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
    storage.read_meta_data('../devices_peto.json', '../events_peto.json')

    modules = ['beeeon_temperature_in', 'beeeon_humidity_in', 'beeeon_temperature_out', 'beeeon_humidity_out']
    all = storage.download_data_for_normalization(modules)
    all = storage.filter_general_attribute_value(all, 'out_sensor', 'yes')

    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'beeeon_temperature_in', 'beeeon_humidity_in')
    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'beeeon_temperature_out', 'beeeon_humidity_out')
    all = dp.convert_absolute_humidity_to_relative_humidity(all, 'beeeon_temperature_in', 'beeeon_humidity_out')

    norm = dp.norm_all(all)
    filtered = storage.filter_downloaded_data(norm, 'beeeon_temperature_in', 'value',
                                              'beeeon_temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'beeeon_humidity_in', 'value',
                                              'beeeon_humidity_out', 'relative_humidity_in', 10.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'beeeon_temperature_out', 'value', 30.0)

    one_norm_graph = []
    graphs = []

    for i in range(0, len(filtered)):
        norm_values_temp_in = dp.filter_one_values(filtered[i], 'beeeon_temperature_in')
        norm_values_hum_in = dp.filter_one_values(filtered[i], 'beeeon_humidity_in')
        norm_values_temp_out = dp.filter_one_values(filtered[i], 'beeeon_temperature_out')
        norm_values_hum_out = dp.filter_one_values(filtered[i], 'beeeon_humidity_out')

        g = {
            'title': 'Rel hum in and rel hum out re-counted to rel hum in',
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'DarkBlue', 'hum in', 'value'),
                dp.gen_simple_graph(norm_values_hum_out, 'DarkTurquoise', 'hum out', 'relative_humidity_in')
            ],
            'group': 'one'
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0, 'line', global_range=True)
