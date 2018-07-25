#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as e
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

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

    derivation = e.Derivation()

    input_data.reverse()
    out = derivation.compute(input_data, 5)

    print(out)
