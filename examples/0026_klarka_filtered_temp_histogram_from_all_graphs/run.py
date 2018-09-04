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

    dw1_filtered, dw2_filtered, dw3_filtered, dw4_filtered = \
        storage.filter_downloaded_data(dw1, dw2, dw3, dw4, 07.0, 100.0, 15.0, 100.0)

    his_data = dp.gen_histogram(dw1_filtered, 10, 13, 31, 1, 'value')
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'test_g.html', 0, 0, 'bar')
