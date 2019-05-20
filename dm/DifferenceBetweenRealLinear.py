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


class DifferenceBetweenRealLinear(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                window_size_before, window_size_after, prefix=''):

        intervals_before = [0] + intervals_before
        before = []
        after = []
        infix = '_windowSize{0}_{1}'.format(window_size_before,window_size_after )

        # compute before
        x = []
        y = []
        values = {}

        start = timestamp - window_size_before
        end = timestamp + 1
        for time in range(start, end, 1):
            value = self.row_selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_before:
            if interval > window_size_before:
                break

            time = timestamp - interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = round(linear_value - orig_value, precision)
            name = self.attr_name(column, prefix, infix + '_before', interval)
            before.append((name, self.transform(diff, interval)))

        # compute after
        x = []
        y = []
        values = {}

        start = timestamp
        end = timestamp + window_size_after + 1
        for time in range(start, end, 1):
            value = self.row_selector.row(column, time)
            x.append(time)
            y.append(value)
            values[time] = value
        slope, intercept, _, _, _ = stats.linregress(x, y)

        for interval in intervals_after:
            if interval > window_size_after:
                break

            time = timestamp + interval
            orig_value = values[time]
            linear_value = intercept + slope * time

            diff = round(linear_value - orig_value, precision)
            name = self.attr_name(column, prefix, infix + '_after', interval)
            after.append((name, self.transform(diff, interval)))

        return before, after
