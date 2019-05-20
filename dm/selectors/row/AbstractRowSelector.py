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


class AbstractRowSelector(ABC):
    def __init__(self, con, table_name):
        self.con = con
        self.table_name = table_name
        super(AbstractRowSelector, self).__init__()

    @abstractmethod
    def row(self, column_name, time):
        pass

    @abstractmethod
    def clear(self):
        pass
