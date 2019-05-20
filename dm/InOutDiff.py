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

class InOutDiff(AbstractPrepareAttr):
    def execute(self, timestamp, column, precision, intervals_before, intervals_after,
                prefix):

        before = []
        after = []

        for interval in intervals_before:
            res = round(self.row_selector.row(column, timestamp - interval), precision)
            name = self.attr_name(column, prefix, 'before', interval)
            before.append((name, res))

        for interval in intervals_after:
            res = round(self.row_selector.row(column, timestamp + interval), precision)
            name = self.attr_name(column, prefix, 'after', interval)
            before.append((name, res))

        return before, after
