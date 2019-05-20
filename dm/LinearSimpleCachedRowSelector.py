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

from dm.AbstractRowSelector import AbstractRowSelector

class LinearSimpleCachedRowSelector(AbstractRowSelector):
    def __init__(self, con, table_name, half_window_size):
        self.cache = {}
        self.half_window_size = half_window_size
        super(LinearSimpleCachedRowSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}

        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            start = time - self.half_window_size
            end = time + self.half_window_size
            res = Storage.select_interval(self.con, start, end, column_name, self.table_name,
                                          without_none_value=False)

            error = False
            if res is None or None in res:
                error = True

            if error:
                self.cache[column_name][time] = None
                t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
                raise ValueError('empty value at %s' % t)

            x = []
            y = []
            for i in range(0, len(res)):
                x.append(i)
                y.append(res[i])

            slope, intercept, _, _, _ = stats.linregress(x, y)

            value = intercept + slope * self.half_window_size
            self.cache[column_name][time] = value

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)

        return value

    def clear(self):
        del self.cache
