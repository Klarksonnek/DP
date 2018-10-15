#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging


def convert_to_is_open(values, module_name, value_index):
    value = int(float(dp.extract_value(values, module_name, value_index)['value']))

    if value == 1:
        return 'open'

    return 'closed'


def convert_to_action(value_index, value_count, event_type):
    if value_index == 0:
        return 'open'
    elif value_index == value_count - 1 and event_type != 'no_event_start':
        return 'close'
    else:
        return 'nothing'


def one_row(event, modules, i, sep, value_count, start_time, event_type):
    # precision
    p = 2

    row = ''

    row += dp.utc_timestamp_to_str(start_time + i, '%Y/%m/%d') + sep
    row += dp.utc_timestamp_to_str(start_time + i, '%H:%M:%S') + sep
    row += str(round(dp.extract_value(modules, 'co2', i)['value'], p)) + sep
    row += str(
        round(dp.UtilCO2.co2_from_ppm_to_g_m3(dp.extract_value(modules, 'co2', i)['value']),
              p)) + sep
    row += str(round(435.0, p)) + sep
    row += str(round(dp.UtilCO2.co2_from_ppm_to_g_m3(435.0), p)) + sep

    row += str(round(dp.extract_value(modules, 'protronix_temperature', i)['value'], p)) + sep
    row += str(round(dp.extract_value(modules, 'beeeon_temperature_out', i)['value'], p)) + sep

    row += str(round(dp.extract_value(modules, 'protronix_humidity', i)['value'], p)) + sep
    row += str(
        round(dp.extract_value(modules, 'protronix_humidity', i)['absolute_humidity'], p)) + sep
    row += str(
        round(dp.extract_value(modules, 'protronix_humidity', i)['specific_humidity'], p)) + sep

    row += str(round(dp.extract_value(modules, 'beeeon_humidity_out', i)['value'], p)) + sep
    row += str(
        round(dp.extract_value(modules, 'beeeon_humidity_out', i)['absolute_humidity'], p)) + sep
    row += str(
        round(dp.extract_value(modules, 'beeeon_humidity_out', i)['specific_humidity'], p)) + sep

    row += str(round(dp.extract_value(modules, 'pressure_in', i)['value'], 4)) + sep

    row += str(round(dp.extract_value(modules, 'protronix_temperature', i)['value'] -
                     dp.extract_value(modules, 'beeeon_temperature_out', i)['value'], p)) + sep
    row += str(round(dp.extract_value(modules, 'protronix_humidity', i)['value'] -
                     dp.extract_value(modules, 'beeeon_humidity_out', i)['value'], p)) + sep
    row += str(round(dp.extract_value(modules, 'protronix_humidity', i)['absolute_humidity'] -
                     dp.extract_value(modules, 'beeeon_humidity_out', i)['absolute_humidity'], p)) + sep
    row += str(round(dp.extract_value(modules, 'protronix_humidity', i)['specific_humidity'] -
                     dp.extract_value(modules, 'beeeon_humidity_out', i)['specific_humidity'], p)) + sep

    row += event['graph_type'] + sep
    row += event['wind'] + sep
    row += event['sun'] + sep
    row += event['sky'] + sep
    row += event['rain'] + sep
    row += str(event['people']) + sep

    row += convert_to_is_open(modules, 'open_close', i) + sep
    row += convert_to_action(i, value_count, event_type)

    # return row.replace('.', ',')
    return row


def zzn_header(sep):
    header = ''

    header += 'date' + sep
    header += 'time' + sep
    header += 'co2_in_ppm' + sep
    header += 'co2_in_g_m3' + sep
    header += 'co2_out_ppm' + sep
    header += 'co2_out_g_m3' + sep

    header += 'temperature_in_celsius' + sep
    header += 'temperature_out_celsius' + sep

    header += 'humidity_in_relative_percent' + sep
    header += 'humidity_in_absolute_g_m3' + sep
    header += 'humidity_in_specific_g_kg' + sep

    header += 'humidity_out_relative_percent' + sep
    header += 'humidity_out_absolute_g_m3' + sep
    header += 'humidity_out_specific_g_kg' + sep

    header += 'pressure_in_hpa' + sep

    header += 'temperature_celsius_difference' + sep
    header += 'humidity_relative_percent_difference' + sep
    header += 'humidity_absolute_g_m3_difference' + sep
    header += 'humidity_specific_g_kg_difference' + sep

    header += 'graph_type' + sep
    header += 'wind' + sep
    header += 'sun' + sep
    header += 'sky' + sep
    header += 'rain' + sep
    header += 'people' + sep

    header += 'window_state' + sep
    header += 'event'
    header += '\n'

    return header


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_peto.json', '../events_peto.json')
    storage.set_no_event_time(-60)

    modules = [
        'co2',
        'protronix_temperature',
        'protronix_humidity',
        'beeeon_temperature_out',
        'beeeon_humidity_out',
        'open_close',
        'pressure_in',
    ]
    all = storage.download_data_for_normalization(modules)
    all = storage.filter_general_attribute_value(all, 'out_sensor', 'yes')

    all = dp.convert_relative_humidity_to_absolute_humidity(
        all, 'protronix_temperature', 'protronix_humidity')
    all = dp.convert_relative_humidity_to_absolute_humidity(
        all, 'beeeon_temperature_out', 'beeeon_humidity_out')

    all = dp.convert_relative_humidity_to_specific_humidity(
        all, 'protronix_temperature', 'protronix_humidity')
    all = dp.convert_relative_humidity_to_specific_humidity(
        all, 'beeeon_temperature_out', 'beeeon_humidity_out')

    norm = dp.norm_all(all)

    one_norm_graph = []
    graphs = []

    separator = ';'
    dp.to_zzn_csv(norm, separator, zzn_header(separator), one_row)
