"""Calculation of CO2 regression using outdoor CO2, room volume.

Calculates regression when the window is open.
"""
from dm.co2regression.AbstractRegression import AbstractRegression
from scipy.optimize import curve_fit
import numpy as np

__author__ = ''
__email__ = ''


class SimpleExpRegression(AbstractRegression):
    def __init__(self, co2_out, volume):
        self._volume = volume
        super(SimpleExpRegression, self).__init__(co2_out)

    @staticmethod
    def gen_f(co2_start, co2_out):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a * x)

    @staticmethod
    def gen_f_volume(co2_start, co2_out, volume):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)

    def compute_parameter(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)

        if self._volume is None:
            f = SimpleExpRegression.gen_f(y[0], self._co2_out)
        else:
            f = SimpleExpRegression.gen_f_volume(y[0], self._co2_out, self._volume)

        popt, pcov = curve_fit(f, x, y)
        return popt[0], np.sqrt(np.diag(pcov))

    def compute_curve(self, x, y):
        # index 0 - parameter, index 1 - error
        param = self.compute_parameter(x, y)[0]

        if self._volume is None:
            f = SimpleExpRegression.gen_f(y[0], self._co2_out)
        else:
            f = SimpleExpRegression.gen_f_volume(y[0], self._co2_out, self._volume)

        out = []
        for i in range(0, len(x)):
            out.append(f(i, param))

        return out
