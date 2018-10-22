#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import json
import env_dp.core as dp
import logging


def download_weather_without_cache():
    w = dp.WeatherData(cache=False)

    logging.info(json.dumps(w.weather_data(1525240913, 1525240929), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525240903, 1525240919), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525504009, 1525504025), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525503999, 1525504015), indent=4, sort_keys=True))


def download_weather_with_cache():
    w = dp.WeatherData(cache=True)

    logging.info(json.dumps(w.weather_data(1525240913, 1525240929), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525240903, 1525240919), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525504009, 1525504025), indent=4, sort_keys=True))
    logging.info(json.dumps(w.weather_data(1525503999, 1525504015), indent=4, sort_keys=True))


def data_storage_without_cache():
    cl = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=False)
    cl.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(cl, dp.WeatherData(cache=False))
    storage.read_meta_data('../devices_examples.json', '../events_examples.json')
    storage.set_no_event_time(-10)

    events = storage.download_data(10, 6)
    data = storage.common_data(events)
    logging.info(json.dumps(data, indent=4, sort_keys=True))


def data_storage_with_cache():
    cl = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=True)
    cl.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(cl, dp.WeatherData(cache=True))
    storage.read_meta_data('../devices_examples.json', '../events_examples.json')
    storage.set_no_event_time(-10)

    events = storage.download_data(10, 6)

    common_data = storage.common_data(events)
    logging.info(json.dumps(common_data, indent=4, sort_keys=True))

    return storage


def weka_create_arff_file(filename):
    weka_content = [
        {
            'title': 'open_close',
            'data': [1, 0, 1, 0]
        },
        {
            'title': 'der10',
            'data': [20, 21, 22, 23]
        },
        {
            'title': 'der20',
            'data': [55, 56, 57, 58]
        },
    ]

    dp.to_weka_file(weka_content, filename)


def compute_derivation():
    input_data = [
        {
            'at': 1531224000,
            'value': 1492,
        },
        {
            'at': 1531224001,
            'value': 1485,
        },
        {
            'at': 1531224002,
            'value': 1479,
        },
        {
            'at': 1531224003,
            'value': 1487,
        },
        {
            'at': 1531224004,
            'value': 1498,
        },
        {
            'at': 1531224005,
            'value': 1497,
        },
        {
            'at': 1531224006,
            'value': 1495,
        },
        {
            'at': 1531224007,
            'value': 1493,
        },
        {
            'at': 1531224008,
            'value': 1495,
        },
        {
            'at': 1531224009,
            'value': 1496,
        },
        {
            'at': 1531224010,
            'value': 1502,
        }
    ]

    derivation = dp.Derivation()

    input_data.reverse()
    logging.info(derivation.compute(input_data, 5))


def simple_web_graph(library_path, filename):
    data = {
        'title': 'Test graph',
        'graphs': [
            {
                'timestamps': [10, 11, 12],
                'values': [5, 20, 7],
                'label_x': 'x label',
                'color': 'red',
            },
            {
                'timestamps': [10, 11, 12],
                'values': [15, 16, 17],
                'label_x': 'x label 2',
                'color': 'blue',
            }
        ]
    }

    g = dp.Graph(library_path)
    g.gen([data], filename, 2, 2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    library_path = './../../src/graph'

    download_weather_without_cache()
    download_weather_with_cache()

    data_storage_without_cache()
    default_storage = data_storage_with_cache()

    weka_create_arff_file('weka_test_file.arff')

    compute_derivation()

    simple_web_graph(library_path, 'components_g_0.html')
