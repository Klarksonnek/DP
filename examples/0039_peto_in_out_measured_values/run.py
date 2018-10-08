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
    storage.read_meta_data('../devices_peto.json', '../events_peto.json')

    modules = [
        'co2',
        'protronix_temperature',
        'protronix_humidity',
        'beeeon_temperature_out',
        'beeeon_humidity_out',
    ]
    all = storage.download_data_for_normalization(modules)

    norm = dp.norm_all(all)
    norm = storage.filter_general_attribute_value(norm, 'out_sensor', 'yes')

    one_norm_graph = []
    graphs = []

    for i in range(0, len(norm)):
        co2 = dp.filter_one_values(norm[i], 'co2')
        protronix_temperature = dp.filter_one_values(norm[i], 'protronix_temperature')
        protronix_humidity = dp.filter_one_values(norm[i], 'protronix_humidity')
        beeeon_temperature_out = dp.filter_one_values(norm[i], 'beeeon_temperature_out')
        beeeon_humidity_out = dp.filter_one_values(norm[i], 'beeeon_humidity_out')


        g = {
            'title': 'CO2 in',
            'graphs': [
                dp.gen_simple_graph(co2, 'blue', 'CO2 in', 'value', 50),
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Temperature in/out',
            'graphs': [
                dp.gen_simple_graph(protronix_temperature, 'red', 'Temperature in', 'value', 50),
                dp.gen_simple_graph(beeeon_temperature_out, 'blue', 'Temperature out', 'value', 50),
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Humidity in/out',
            'graphs': [
                dp.gen_simple_graph(protronix_humidity, 'red', 'Humidity in', 'value', 50),
                dp.gen_simple_graph(beeeon_humidity_out, 'blue', 'Humidity out', 'value', 50),
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Humidity in/out',
            'graphs': [
                dp.gen_simple_graph(co2, 'blue', 'CO2 in', 'value_norm', 50),
                dp.gen_simple_graph(protronix_temperature, 'red', 'Temperature in', 'value_norm', 50),
                dp.gen_simple_graph(protronix_humidity, 'orange', 'Humidity in', 'value_norm', 50),
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
