from abc import ABC, abstractmethod
from collections import OrderedDict

from os.path import dirname, abspath, join
import os
from functools import reduce
import sys
import logging
import math
import csv

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.CSVUtil import CSVUtil
from dm.Storage import Storage
from dm.ValueUtil import ValueUtil
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fractions import Fraction
from sympy import *
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull

DATA_CACHE = None


from dm.AbstractRegression import AbstractRegression


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
