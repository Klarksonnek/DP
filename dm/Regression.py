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


from dm.AbstractPrepareAttr import AbstractPrepareAttr


class Regression(AbstractPrepareAttr):
    def __init__(self, con, table_name, row_selector, interval_selector, method):
        self._method = method
        super(Regression, self).__init__(con, table_name, row_selector, interval_selector)

    def execute(self, timestamp_start, timestamp_end, column, precision, prefix, enable_error):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        x = np.asarray(x)
        y = np.asarray(y)

        param, err = self._method.compute_parameter(x, y)
        name = self.attr_name(column, prefix, 'before', 0)
        before = [(name, round(param * 3600, precision))]

        if enable_error:
            before.append(('err', round(float(err), 8)))

        return before, []

    @staticmethod
    def gen_f_lambda(co2_start, co2_out):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a * x)

    @staticmethod
    def gen_f_prietok(co2_start, co2_out, volume):
        return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)
