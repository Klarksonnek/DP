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

    dw1 = storage.download_data_for_normalization(['co2'])
    client.logout()

    his_data = dp.gen_histogram(dw1, 60, 400, 2000, 200)
    histograms = dp.gen_histogram_graph(his_data)

    g = dp.Graph("./../../src/graph")
    g.gen(histograms, 'test_g.html', 0, 0, 'bar')
