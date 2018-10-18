#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging
import datetime


def prepare_weka_files(events):
    file = open('co2_weka.arff', 'w')
    file.write('@relation events\n\n')

    class_name = 'graph_type'
    out = ''

    values = []
    for ev in events:
        m_protronix_temperature = dp.find_module_measured(ev, 'protronix_temperature')
        m_beeeon_temperature_out = dp.find_module_measured(ev, 'beeeon_temperature_out')
        m_protronix_humidity = dp.find_module_measured(ev, 'protronix_humidity')
        m_beeeon_humidity_out = dp.find_module_measured(ev, 'beeeon_humidity_out')

        precision = 2

        values = [
            ('people', ev['people']),
            ('wind', ev['wind']),
            ('sky', ev['sky']),
            ('slnko', ev['sun']),
            ('teplota_dnu', round(m_protronix_temperature[0]['value'], precision)),
            ('teplota_von', round(m_beeeon_temperature_out[0]['value'], precision)),
            ('rozdiel_teplot', round(abs(
                m_beeeon_temperature_out[0]['value'] - m_protronix_temperature[0]['value']),
                                     precision)),

            ('rh_dnu', round(m_protronix_humidity[0]['value'], precision)),
            ('rh_von', round(m_beeeon_humidity_out[0]['value'], precision)),
            ('rozdiel_rh',
             round(abs(m_protronix_humidity[0]['value'] - m_beeeon_humidity_out[0]['value']),
                   precision)),

            ('abs_rh_dnu', round(m_protronix_humidity[0]['absolute_humidity'], precision)),
            ('abs_rh_von', round(m_beeeon_humidity_out[0]['absolute_humidity'], precision)),
            ('rozdiel_abs_rh', round(abs(
                m_protronix_humidity[0]['absolute_humidity'] - m_beeeon_humidity_out[0][
                    'absolute_humidity']), precision)),

            ('spec_rh_dnu', round(m_protronix_humidity[0]['specific_humidity'], precision)),
            ('spec_rh_von', round(m_beeeon_humidity_out[0]['specific_humidity'], precision)),
            ('rozdiel_spec_rh', round(abs(
                m_protronix_humidity[0]['specific_humidity'] - m_beeeon_humidity_out[0][
                    'specific_humidity']), precision)),
            (class_name, ev['graph_type']),
        ]

        for i in range(0, len(values)):
            value = values[i]

            out += str(value[1])

            if i != len(values) - 1:
                out += ','

        out += "\n"

    for item, _ in values:
        if item == class_name:
            file.write('@attribute class {exponential, linear, uneven}\n')
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
    storage.read_meta_data('../devices_peto.json', '../events_peto.json')

    modules = [
        'co2',
        'protronix_temperature',
        'protronix_humidity',
        'beeeon_temperature_out',
        'beeeon_humidity_out',
    ]
    all = storage.download_data_for_normalization(modules)

    # vystrihnutie prvych 10 minut
    all = dp.cut_events(all, 0, 604)

    # zobrazenie grafov, ktore obsahuju prave tych 10 minut
    all = dp.filter_number_events(all, 604)

    norm = storage.filter_general_attribute_value(all, 'out_sensor', 'yes')

    norm = dp.convert_relative_humidity_to_absolute_humidity(norm, 'protronix_temperature', 'protronix_humidity')
    norm = dp.convert_relative_humidity_to_absolute_humidity(norm, 'beeeon_temperature_out', 'beeeon_humidity_out')

    norm = dp.convert_relative_humidity_to_specific_humidity(norm, 'protronix_temperature', 'protronix_humidity')
    norm = dp.convert_relative_humidity_to_specific_humidity(norm, 'beeeon_temperature_out', 'beeeon_humidity_out')

    norm = dp.norm_all(norm)

    prepare_weka_files(norm)

    one_norm_graph = []
    graphs = []

    for i in range(0, len(norm)):
        ev = norm[i]
        co2 = dp.filter_one_values(norm[i], 'co2')
        protronix_temperature = dp.filter_one_values(norm[i], 'protronix_temperature')
        protronix_humidity = dp.filter_one_values(norm[i], 'protronix_humidity')
        beeeon_temperature_out = dp.filter_one_values(norm[i], 'beeeon_temperature_out')
        beeeon_humidity_out = dp.filter_one_values(norm[i], 'beeeon_humidity_out')

        abs_in = dp.filter_one_values(norm[i], 'protronix_humidity')
        abs_out = dp.filter_one_values(norm[i], 'beeeon_humidity_out')

        start = norm[i]['times']['event_start']
        end = norm[i]['times']['event_end']

        t = datetime.datetime.fromtimestamp(start).strftime('%d.%m. %H:%M:%S')
        t += ' - '
        t += datetime.datetime.fromtimestamp(end).strftime('%H:%M:%S')

        m_protronix_temperature = dp.find_module_measured(ev, 'protronix_temperature')
        m_beeeon_temperature_out = dp.find_module_measured(ev, 'beeeon_temperature_out')
        m_protronix_humidity = dp.find_module_measured(ev, 'protronix_humidity')
        m_beeeon_humidity_out = dp.find_module_measured(ev, 'beeeon_humidity_out')

        precision = 2

        stat = [
            ('people', ev['people']),
            ('wind', ev['wind']),
            ('obloha', ev['sky']),
            ('slnko', ev['sun']),
            ('', ''),
            ('teplota dnu', round(m_protronix_temperature[0]['value'], precision)),
            ('teplota von', round(m_beeeon_temperature_out[0]['value'], precision)),
            ('rozdiel teplot', round(abs(m_beeeon_temperature_out[0]['value'] - m_protronix_temperature[0]['value']), precision)),

            ('', ''),
            ('rh dnu', round(m_protronix_humidity[0]['value'], precision)),
            ('rh von', round(m_beeeon_humidity_out[0]['value'], precision)),
            ('rozdiel rh', round(abs(m_protronix_humidity[0]['value'] - m_beeeon_humidity_out[0]['value']), precision)),

            ('', ''),
            ('abs rh dnu', round(m_protronix_humidity[0]['absolute_humidity'], precision)),
            ('abs rh von', round(m_beeeon_humidity_out[0]['absolute_humidity'], precision)),
            ('rozdiel abs rh', round(abs(m_protronix_humidity[0]['absolute_humidity'] - m_beeeon_humidity_out[0]['absolute_humidity']), precision)),

            ('', ''),
            ('spec rh dnu', round(m_protronix_humidity[0]['specific_humidity'], precision)),
            ('spec rh von', round(m_beeeon_humidity_out[0]['specific_humidity'], precision)),
            ('rozdiel spec rh', round(abs(m_protronix_humidity[0]['specific_humidity'] - m_beeeon_humidity_out[0]['specific_humidity']), precision)),
        ]

        g = {
            'title': 'CO2 in: ' + t,
            'stat': stat,
            'graphs': [
                dp.gen_simple_graph(co2, 'blue', 'CO2 in', 'value', 50),
            ]
        }
        graphs.append(g)

        continue

        g = {
            'title': 'Abs humidity in/out: ' + t,
            'graphs': [
                dp.gen_simple_graph(abs_in, 'red', 'Humidity in', 'absolute_humidity', 50),
                dp.gen_simple_graph(abs_out, 'blue', 'Humidity out', 'absolute_humidity', 50),
            ]
        }
        graphs.append(g)

        g = {
            'title': 'Humidity in/out: ' + t,
            'graphs': [
                dp.gen_simple_graph(co2, 'blue', 'CO2 in', 'value_norm', 50),
                dp.gen_simple_graph(protronix_temperature, 'red', 'Temperature in', 'value_norm', 50),
                dp.gen_simple_graph(protronix_humidity, 'orange', 'Humidity in', 'value_norm', 50),
                dp.gen_simple_graph(abs_in, 'green', 'Humidity in abs', 'absolute_humidity_norm', 50),
                dp.gen_simple_graph(abs_out, 'black', 'Humidity out abs', 'absolute_humidity_norm', 50),
            ]
        }
        graphs.append(g)

    g = dp.Graph("./../../src/graph")
    g.gen(graphs, 'test_g.html', 0, 0)
