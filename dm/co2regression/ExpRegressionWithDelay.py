"""Calculation of CO2 regression using outdoor CO2, room volume, window_size and threshold.

Calculates regression when the CO2 decrease is noticed using threshold in window.
"""
from dm.ValueUtil import ValueUtil
from dm.co2regression.SimpleExpRegression import SimpleExpRegression

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


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
