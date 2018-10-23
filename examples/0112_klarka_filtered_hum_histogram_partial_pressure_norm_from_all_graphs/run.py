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

    all = dp.convert_relative_humidity_to_partial_pressure(all, 'temperature_in', 'humidity_in')
    all = dp.convert_relative_humidity_to_partial_pressure(all, 'temperature_out', 'humidity_out')

    norm = dp.norm_all(all)
    filtered = storage.filter_downloaded_data(norm, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'partial_pressure',
                                              'humidity_out', 'partial_pressure', 1.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value', 30.0)
    filtered = storage.filter_downloaded_data_general_attribute(filtered, "window", "ventilacka")

    filtered_one_value = dp.filter_data(filtered, ['humidity_in'])
    his_data = dp.gen_histogram(filtered_one_value, 15, 0, 1, 0.1, 'partial_pressure_norm')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'test_g.html', 0, 0, 'bar', global_range=True)
