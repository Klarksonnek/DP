from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

import numpy as np

DATA_CACHE = None


from dm.coefficients.AbstractLineCoefficients import AbstractLineCoefficients
from dm.coefficients.DistanceToLine import DistanceToLine


class PolyfitLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            sh_decrease_tmp = [0, float(row[col1]) - float(row[col2])]
            sh_diff_tmp = [0, float(row[col3])]
            coeffs_point = np.polyfit(sh_decrease_tmp, sh_diff_tmp, 1)
            direction.append(coeffs_point[0])

        return sum(direction) / float(len(direction))
