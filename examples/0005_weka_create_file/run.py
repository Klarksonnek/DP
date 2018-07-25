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

    e.to_weka_file(weka_content, 'weak_test_file.arff')
