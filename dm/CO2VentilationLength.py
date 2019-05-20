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


class CO2VentilationLength(AbstractPrepareAttr):
    def execute(self, timestamp_start, timestamp_end, compute_timestamp, intervals,
                method, co2_out, column, precision, prefix):
        x = []
        y = []
        for timestamp in range(timestamp_start, timestamp_end):
            y.append(self.row_selector.row(column, timestamp))
            x.append(timestamp - timestamp_start)

        return [('actual_value', y[compute_timestamp]), ('co2_start', y[0])], []
