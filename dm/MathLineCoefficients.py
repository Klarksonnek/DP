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

from dm.AbstractLineCoefficients import AbstractLineCoefficients
from dm.DistanceToLine import DistanceToLine


class MathLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            b = -(float(row[col1]) - float(row[col2]))
            a = float(row[col3])
            direction.append(-a / b)

        return sum(direction) / float(len(direction))

