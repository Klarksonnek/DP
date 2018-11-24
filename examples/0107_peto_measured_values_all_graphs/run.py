#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import datetime
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

    all = dp.cut_events(all, 0, 900)
    all = dp.filter_number_events(all, 900)

    all = storage.filter_general_attribute_value(all, 'out_sensor', 'yes')
    all = dp.convert_relative_humidity_to_specific_humidity(all, 'beeeon_temperature_in', 'beeeon_humidity_in')
    all = dp.convert_relative_humidity_to_specific_humidity(all, 'beeeon_temperature_out', 'beeeon_humidity_out')
    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'beeeon_temperature_in', 'beeeon_humidity_in')
    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'beeeon_temperature_out', 'beeeon_humidity_out')

    norm = dp.norm_all(all)

    filtered = storage.filter_downloaded_data(norm, 'beeeon_temperature_in', 'value',
                                              'beeeon_temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'beeeon_temperature_out', 'value', 15.0)
    filtered = storage.filter_downloaded_data_two_conditions(filtered, 'beeeon_humidity_out', 'specific_humidity',
                                                             6.0, 'beeeon_humidity_in', 'specific_humidity', 1.6, 100.0)
    filtered = dp.estimate_relative_humidity(filtered, 'beeeon_humidity_in', 'beeeon_humidity_out', 'beeeon_temperature_in')
    print("Event count: %d" % len(filtered))

    one_norm_graph = []
    graphs = []

    for i in range(0, len(filtered)):
        norm_values_temp_in = dp.filter_one_values(filtered[i], 'beeeon_temperature_in')
        norm_values_hum_in = dp.filter_one_values(filtered[i], 'beeeon_humidity_in')
        norm_values_temp_out = dp.filter_one_values(filtered[i], 'beeeon_temperature_out')
        norm_values_hum_out = dp.filter_one_values(filtered[i], 'beeeon_humidity_out')

        start = filtered[i]['times']['event_start']
        end = filtered[i]['times']['event_end']

        t = datetime.datetime.fromtimestamp(start).strftime('%d.%m. %H:%M:%S')
        t += ' - '
        t += datetime.datetime.fromtimestamp(end).strftime('%H:%M:%S')

        precision = 2

        stat = [
            ('people', filtered[i]['people']),
            ('wind', filtered[i]['wind']),
            ('obloha', filtered[i]['sky']),
            ('slnko', filtered[i]['sun']),
            ('', ''),
            ('teplota dnu', round(norm_values_temp_in[0]['value'], precision)),
            ('teplota von', round(norm_values_temp_out[0]['value'], precision)),
            ('rozdiel teplot',
             round(abs(norm_values_temp_out[0]['value'] - norm_values_temp_in[0]['value']), precision)),

            ('', ''),
            ('rh dnu', round(norm_values_hum_in[0]['value'], precision)),
            ('rh von', round(norm_values_hum_out[0]['value'], precision)),
            ('rozdiel rh', round(abs(norm_values_hum_in[0]['value'] - norm_values_hum_out[0]['value']), precision)),

            ('', ''),
            ('abs rh dnu', round(norm_values_hum_in[0]['absolute_humidity'], precision)),
            ('abs rh von', round(norm_values_hum_out[0]['absolute_humidity'], precision)),
            ('rozdiel abs rh',
             round(abs(norm_values_hum_in[0]['absolute_humidity'] - norm_values_hum_out[0]['absolute_humidity']),
                   precision)),

            ('', ''),
            ('spec rh dnu', round(norm_values_hum_in[0]['specific_humidity'], precision)),
            ('spec rh von', round(norm_values_hum_out[0]['specific_humidity'], precision)),
            ('rozdiel spec rh',
             round(abs(norm_values_hum_in[0]['specific_humidity'] - norm_values_hum_out[0]['specific_humidity']),
                   precision)),
        ]

        #g = {
        #    'title': 'Temp in and hum in',
        #    'graphs': [
        #        dp.gen_simple_graph(norm_values_temp_in, 'red', 'temp in', 'value_norm', 100),
        #        dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in', 'value_norm', 100)
        #    ]
        #}
        #graphs.append(g)

        #g = {
        #    'title': 'Temp out and hum out',
        #    'graphs': [
        #        dp.gen_simple_graph(norm_values_temp_out, 'red', 'temp out', 'value_norm', 100),
        #        dp.gen_simple_graph(norm_values_hum_out, 'blue', 'hum out', 'value_norm', 100)
        #    ]
        #}
        #graphs.append(g)

        g = {
            'title': 'Temp in and temp out ' + t,
            'stat': stat,
            'graphs': [
                dp.gen_simple_graph(norm_values_temp_in, 'DarkRed', 'temp in', 'value', 100),
                dp.gen_simple_graph(norm_values_temp_out, 'LightCoral', 'temp out', 'value', 100)
            ]
        }

        graphs.append(g)

        g = {
            'title': 'Hum in and hum out ' + t,
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in', 'value', 100),
                dp.gen_simple_graph(norm_values_hum_out, 'red', 'hum out', 'value', 100)
            ]
        }

        graphs.append(g)

        g = {
            'title': 'Spec hum in and spec hum out ' + t,
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in', 'specific_humidity', 100),
                dp.gen_simple_graph(norm_values_hum_out, 'red', 'hum out', 'specific_humidity', 100)
            ]
        }

        graphs.append(g)

        g = {
            'title': 'Hum in and hum in estimated ' + t,
            'graphs': [
                dp.gen_simple_graph(norm_values_hum_in, 'DarkBlue', 'hum in', 'value', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'DarkRed', 'hum in estimated', 'hum_in_estimated1', 100)
            ]
        }

        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    #g = dp.Graph("src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
