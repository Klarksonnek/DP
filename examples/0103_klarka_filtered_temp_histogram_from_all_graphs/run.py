#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp
import logging
import copy


def filtered_temp_histogram_from_all_graphs(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 7.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'value', 15.0, 100.0)

    filtered_one_value = dp.filter_data(filtered, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 10, 13, 31, 1, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_1.html', 0, 0, 'bar')


def filtered_hum_histogram_from_all_graphs(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 7.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'value', 15.0, 100.0)

    filtered_one_value = dp.filter_data(filtered, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 30, 20, 70, 5, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_2.html', 0, 0, 'bar')


def temp_histogram_from_all_graphs(events):
    filtered_one_value = dp.filter_data(events, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 20, 0, 1, 0.1, 'value_norm')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_3.html', 0, 0, 'bar')


def hum_histogram_from_all_graphs(events):
    filtered_one_value = dp.filter_data(events, ['humidity_in'])
    his_data = dp.gen_histogram(filtered_one_value, 20, 0, 1, 0.1, 'value_norm')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_4.html', 0, 0, 'bar')


def filtered_hum_histogram_from_all_graphs2(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 7.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'value', 5.0, 100.0)

    filtered_one_value = dp.filter_data(filtered, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 10, 10, 70, 2, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_5.html', 0, 0, 'bar')


def filtered_temp_histogram_from_all_graphs2(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 7.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'value', 5.0, 100.0)

    filtered_one_value = dp.filter_data(filtered, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 15, 13, 31, 1, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_6.html', 0, 0, 'bar')


def filtered_hum_histogram_from_all_graphs3(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'value',
                                              'humidity_out', 'value', 7.0, 100.0)

    filtered_one_value = dp.filter_data(filtered, ['temperature_in'])
    his_data = dp.gen_histogram(filtered_one_value, 10, 20, 70, 2, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_7.html', 0, 0, 'bar')


def filtered_hum_histogram_partial_pressure_from_all_graphs(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'partial_pressure',
                                              'humidity_out', 'partial_pressure', 1.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value',
                                                         30.0)
    filtered = storage.filter_downloaded_data_general_attribute(filtered, "window",
                                                                "ventilacka")

    filtered_one_value = dp.filter_data(filtered, ['humidity_in'])
    his_data = dp.gen_histogram(filtered_one_value, 15, 5, 20, 1, 'partial_pressure')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_8.html', 0, 0, 'bar', global_range=True)


def filtered_hum_histogram_partial_pressure_norm_from_all_graphs(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'partial_pressure',
                                              'humidity_out', 'partial_pressure', 1.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value',
                                                         30.0)
    filtered = storage.filter_downloaded_data_general_attribute(filtered, "window",
                                                                "ventilacka")

    filtered_one_value = dp.filter_data(filtered, ['humidity_in'])
    his_data = dp.gen_histogram(filtered_one_value, 15, 0, 1, 0.1, 'partial_pressure_norm')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_9.html', 0, 0, 'bar', global_range=True)


def stacked_hum_in_histogram_from_all_graphs(events):
    filtered = storage.filter_downloaded_data(events, 'temperature_in', 'value',
                                              'temperature_out', 'value', 5.0, 100.0)
    filtered = storage.filter_downloaded_data(filtered, 'humidity_in', 'partial_pressure',
                                              'humidity_out', 'partial_pressure', 1.0, 100.0)
    filtered = storage.filter_downloaded_data_one_module(filtered, 'temperature_out', 'value',
                                                         30.0)
    filtered = storage.filter_downloaded_data_general_attribute(filtered, "window",
                                                                "ventilacka")

    filtered_one_value = dp.filter_data(filtered, ['humidity_in'])
    his_data = dp.gen_histogram(filtered_one_value, 15, 0, 1, 0.1, 'partial_pressure_norm')
    histograms = dp.gen_histogram_graph_with_factor(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'histogram_10.html', 0, 0, 'bar', 0.0, 35.0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_klarka.json', '../events_klarka.json')

    modules = ['temperature_in', 'humidity_in', 'temperature_out', 'humidity_out']
    all = storage.download_data_for_normalization(modules)

    all = dp.convert_relative_humidity_to_partial_pressure(all, 'temperature_in',
                                                           'humidity_in')
    all = dp.convert_relative_humidity_to_partial_pressure(all, 'temperature_out',
                                                           'humidity_out')

    norm = dp.norm_all(all)

    filtered_temp_histogram_from_all_graphs(copy.deepcopy(norm))
    filtered_hum_histogram_from_all_graphs(copy.deepcopy(norm))
    temp_histogram_from_all_graphs(copy.deepcopy(norm))
    hum_histogram_from_all_graphs(copy.deepcopy(norm))
    filtered_hum_histogram_from_all_graphs2(copy.deepcopy(norm))
    filtered_temp_histogram_from_all_graphs2(copy.deepcopy(norm))
    filtered_hum_histogram_from_all_graphs3(copy.deepcopy(norm))
    filtered_hum_histogram_partial_pressure_from_all_graphs(copy.deepcopy(norm))
    filtered_hum_histogram_partial_pressure_norm_from_all_graphs(copy.deepcopy(norm))
    stacked_hum_in_histogram_from_all_graphs(copy.deepcopy(norm))