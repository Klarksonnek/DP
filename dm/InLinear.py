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


class InLinear(AbstractPrepareAttr):
    def execute(self, timestamp_before, timestamp_after, column, precision,
                start_before, end_before, start_after, end_after, prefix):
        def compute(start, end, timestamp, interval_name):
            res = self.interval_selector.interval(column, start, end)
            x = []
            y = []
            for i in range(0, len(res)):
                x.append(i + start)
                y.append(res[i])

            slope, intercept, _, _, _ = stats.linregress(x, y)
            res = round(intercept + slope * timestamp, precision)

            if interval_name == 'before':
                interval = end_before - start_before
            else:
                interval = end_after - start_after
            name = self.attr_name(column, prefix, interval_name, str(interval))

            return name, res

        before = [compute(start_before, end_before, timestamp_before, 'before')]
        after = [compute(start_after, end_after, timestamp_after, 'after')]

        return before, after
