#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import json
import env_dp.core as dp
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = dp.BeeeOnClient("ant-work.fit.vutbr.cz", 8010, cache=False)
    client.api_key = dp.api_key(CODE_DIR + '/api_key.config')

    storage = dp.DataStorage(client, dp.WeatherData(cache=False))
    storage.read_meta_data('devices.json', 'events.json')
    storage.set_no_event_time(-10)

    dw = storage.download_data(10, 6)
    client.logout()

    common_data = storage.common_data(dw)
    print(json.dumps(common_data, indent=4, sort_keys=True))
