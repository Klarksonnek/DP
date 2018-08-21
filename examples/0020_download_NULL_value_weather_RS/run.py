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

    w = e.WeatherDataRS()

    out_detailed = []
    # mezi 1. 1. 2018 0:50 (1514767800) a 1. 1. 2018 0:55 (1514768100) byla namerena
    # hodnota smeru vetru NULL
    out_detailed = w.download_data(1514764200, 1514764500)
    print(json.dumps(out_detailed, indent=4, sort_keys=True))
