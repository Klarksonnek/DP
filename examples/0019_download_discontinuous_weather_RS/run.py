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
    # mezi 25. 1. 2018 6:25 (1516857900) a 28. 1. 2018 17:50 (1517158200) nebyla namerena
    # zadna data, proto je vystupem prazdny seznam
    out_detailed = w.download_data(1516857900, 1517158200)
    print(json.dumps(out_detailed, indent=4, sort_keys=True))
