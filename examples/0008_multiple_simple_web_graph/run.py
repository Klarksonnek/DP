#!/usr/bin/env python3

from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import env_dp.core as dp


if __name__ == '__main__':
    g1 = {
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

    g2 = {
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

    g = dp.Graph("./../../src/graph")
    g.gen([g1, g2], 'test_g.html', 2, 2)
