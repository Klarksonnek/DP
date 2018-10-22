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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    download_weather_without_cache()
    download_weather_with_cache()
