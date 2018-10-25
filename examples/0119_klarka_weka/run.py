#!/usr/bin/env python3

from os.path import dirname, abspath, join
import datetime
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging


def reduce_classes(events):
    for i in range(0, len(events)):
        type = events[i]['g_type'].split('_')

        if type[0] == 'mirny':
            events[i]['g_type'] = 'mirny'
        elif type[0] == 'strmy':
            events[i]['g_type'] = 'strmy'
        else:
            events[i]['g_type'] = 'unclassified'

    return events


def prepare(events):
    file = open('out.arff', 'w')
    file.write('@relation events\n\n')

    class_name = 'g_type'
    out = ''
    values = []


    for event in events:
        norm_values_temp_in = dp.find_module_measured(event, 'temperature_in')
        norm_values_temp_out = dp.find_module_measured(event, 'temperature_out')
        norm_values_hum_in = dp.find_module_measured(event, 'humidity_in')
        norm_values_hum_out = dp.find_module_measured(event, 'humidity_out')

        precision = 2

        values = [
            ('teplota_dnu', round(norm_values_temp_in[0]['value'], precision)),
            ('teplota_von', round(norm_values_temp_out[0]['value'], precision)),
            ('rozdiel_teplot', round(abs(
                norm_values_temp_out[0]['value'] - norm_values_temp_in[0]['value']),
                                     precision)),

            ('rh_dnu', round(norm_values_hum_in[0]['value'], precision)),
            ('rh_von', round(norm_values_hum_out[0]['value'], precision)),
            ('rozdiel_rh',
             round(abs(norm_values_hum_in[0]['value'] - norm_values_hum_out[0]['value']),
                   precision)),

            ('abs_rh_dnu', round(norm_values_hum_in[0]['absolute_humidity'], precision)),
            ('abs_rh_von', round(norm_values_hum_out[0]['absolute_humidity'], precision)),
            ('rozdiel_abs_rh', round(abs(
                norm_values_hum_in[0]['absolute_humidity'] - norm_values_hum_out[0][
                    'absolute_humidity']), precision)),

            ('spec_rh_dnu', round(norm_values_hum_in[0]['specific_humidity'], precision)),
            ('spec_rh_von', round(norm_values_hum_out[0]['specific_humidity'], precision)),
            ('rozdiel_spec_rh', round(abs(
                norm_values_hum_in[0]['specific_humidity'] - norm_values_hum_out[0][
                    'specific_humidity']), precision)),
            (class_name, event['g_type']),
        ]

        for i in range(0, len(values)):
            value = values[i]

            out += str(value[1])

            if i != len(values) - 1:
                out += ','

        out += "\n"

    for item, _ in values:
        if item == class_name:
            file.write('@attribute class {strmy, mirny}\n')
            continue

        file.write('@attribute %s numeric\n' % item)

    file.write('\n')
    file.write('@data\n\n')

    file.write('%s' % out)
    file.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_klarka.json', '../events_klarka.json')

    modules = ['temperature_in', 'humidity_in', 'temperature_out', 'humidity_out']
    all = storage.download_data_for_normalization(modules)

    all = dp.cut_events(all, 0, 900)
    all = dp.filter_number_events(all, 900)

    all = reduce_classes(all)
    all = storage.filter_downloaded_data_general_attribute(all, "g_type", "unclassified")
    all = storage.filter_downloaded_data_general_attribute(all, "location", "na stolku")

    all = dp.cut_events(all, 0, 900)
    all = dp.filter_number_events(all, 900)

    all = dp.convert_relative_humidity_to_specific_humidity(all, 'temperature_in', 'humidity_in')
    all = dp.convert_relative_humidity_to_specific_humidity(all, 'temperature_out', 'humidity_out')

    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'temperature_in', 'humidity_in')
    all = dp.convert_relative_humidity_to_absolute_humidity(all, 'temperature_out', 'humidity_out')

    norm = dp.norm_all(all)
    filtered = storage.filter_downloaded_data(norm, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value', 15.0)
    filtered = storage.filter_downloaded_data_two_conditions(filtered, 'humidity_out', 'specific_humidity',
                                              6.0, 'humidity_in', 'specific_humidity', 1.6, 100.0)
    filtered = storage.filter_downloaded_data_general_attribute(filtered, "window", "ventilacka")
    filtered = dp.estimate_relative_humidity(filtered, 'humidity_in', 'humidity_out', 'temperature_in')
    print("Event count: %d" % len(filtered))

    one_norm_graph = []
    graphs = []

    prepare(filtered)

    for i in range(0, len(filtered)):
        norm_values_temp_in = dp.filter_one_values(filtered[i], 'temperature_in')
        norm_values_hum_in = dp.filter_one_values(filtered[i], 'humidity_in')
        norm_values_temp_out = dp.filter_one_values(filtered[i], 'temperature_out')
        norm_values_hum_out = dp.filter_one_values(filtered[i], 'humidity_out')
        start = filtered[i]['times']['event_start']
        end = filtered[i]['times']['event_end']

        t = datetime.datetime.fromtimestamp(start).strftime('%d.%m. %H:%M:%S')
        t += ' - '
        t += datetime.datetime.fromtimestamp(end).strftime('%H:%M:%S')

        precision = 2

        stat = [
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
                dp.gen_simple_graph(norm_values_hum_in, 'red', 'hum in', 'value', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'green', 'hum in estimated 1', 'hum_in_estimated1', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'blue', 'hum in estimated 2', 'hum_in_estimated2', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'magenta', 'hum in estimated 3', 'hum_in_estimated3', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'brown', 'hum in estimated 4', 'hum_in_estimated4', 100),
                # dp.gen_simple_graph(norm_values_hum_in, 'cyan', 'hum in estimated 5', 'hum_in_estimated5', 100),
                dp.gen_simple_graph(norm_values_hum_in, 'pink', 'hum in estimated 6', 'hum_in_estimated6', 100)
            ]
        }

        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    # g = dp.Graph("src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)