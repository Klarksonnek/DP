#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import json
import env_dp.core as e
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    w = e.WeatherData(cache=True)

    print(json.dumps(w.weather_data(1525240913, 1525240929), indent=4, sort_keys=True))
    print(json.dumps(w.weather_data(1525240903, 1525240919), indent=4, sort_keys=True))
    print(json.dumps(w.weather_data(1525504009, 1525504025), indent=4, sort_keys=True))
    print(json.dumps(w.weather_data(1525503999, 1525504015), indent=4, sort_keys=True))
