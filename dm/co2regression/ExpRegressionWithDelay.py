from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.ValueUtil import ValueUtil
from sympy import *

DATA_CACHE = None


from dm.co2regression import SimpleExpRegression


class ExpRegressionWithDelay(SimpleExpRegression):
    def __init__(self, co2_out, volume, window_size, threshold):
        self._window_size = window_size
        self._threshold = threshold
        super(ExpRegressionWithDelay, self).__init__(co2_out, volume)

    def compute_parameter(self, x, y):
        delay = ValueUtil.detect_sensor_delay(x, self._window_size, self._threshold)
        return super(ExpRegressionWithDelay, self).compute_parameter(x[delay:], y[delay:])

    def compute_curve(self, x, y):
        delay = ValueUtil.detect_sensor_delay(y, self._window_size, self._threshold)

        new_x = []
        for i in range(0, len(x) - delay):
            new_x.append(i)

        values = super(ExpRegressionWithDelay, self).compute_curve(new_x, y[delay:])

        if delay == 0:
            return values

        out = []
        for k in range(0, delay):
            out.append(y[k])

        return out + values
