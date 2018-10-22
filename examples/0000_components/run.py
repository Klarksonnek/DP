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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    download_weather_without_cache()
    download_weather_with_cache()

    data_storage_without_cache()
