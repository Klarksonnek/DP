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
from dm.SimpleCachedRowSelector import SimpleCachedRowSelector
from dm.LinearSimpleCachedRowSelector import LinearSimpleCachedRowSelector


class CachedRowWithIntervalSelector(SimpleCachedRowSelector):
    def __init__(self, con, table_name, start, end):
        self.start = start
        self.end = end
        self.cache = {}
        super(CachedRowWithIntervalSelector, self).__init__(con, table_name)

    def row(self, column_name, time):
        if column_name not in self.cache:
            self.cache[column_name] = {}
            res = Storage.select_interval(self.con, self.start, self.end, column_name,
                                          self.table_name, without_none_value=False)

            actual_timestamp = self.start
            for row in res:
                if row is None:
                    self.cache[column_name][actual_timestamp] = None
                else:
                    self.cache[column_name][actual_timestamp] = float(row)
                actual_timestamp += 1

        if time in self.cache[column_name]:
            value = self.cache[column_name][time]
        else:
            value = super(CachedRowWithIntervalSelector, self).row(column_name, time)

        if value is None:
            t = DateTimeUtil.utc_timestamp_to_str(time, '%Y/%m/%d %H:%M:%S')
            raise ValueError('empty value at %s' % t)
        return value
