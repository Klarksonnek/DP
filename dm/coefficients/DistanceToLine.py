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


class DistanceToLine:
    def __init__(self, training):
        self.training = training
        self.model = None

    @staticmethod
    def ventilation_length_events(training: list, ventilation_length: int):
        out = []

        for row in training:
            if row['VentilationLength_event__'] == "'" + str(ventilation_length) + "'":
                out.append(row)

        return out

    def humidity_clusters(self, training, col1, col2, col3, intervals, strategy, strategyFlag, one_line,
                          cluster_boundaries, cluster_boundaries_all):
        """

        :param training:
        :param col1:
        :param col2:
        :param col3:
        :param intervals:
        :param strategy:
        :return:
        """

        # colors
        if cluster_boundaries_all:
            colors_trendline = [(0.854, 0.035, 0.027), (0.101, 0.454, 0.125), (0, 0.545, 0.545), (0.545, 0, 0.545), (0, 0, 1)]
            colors_line = [(1, 0.5, 0.5), (0.5, 1, 0.5), (0, 1, 1), (1, 0, 1), (0.5, 0.5, 1)]
        else:
            colors_trendline = [(0.854, 0.035, 0.027), (0.101, 0.454, 0.125), (0, 0, 1)]
            colors_line = [(1, 0.5, 0.5), (0.5, 1, 0.5), (0.5, 0.5, 1)]
        # counter for colors
        i = 0
        fig = plt.figure()
        out_point_line = {}
        out_point_point = {}

        for interval in intervals:
            sh_decrease = []
            sh_diff = []
            for res in self.ventilation_length_events(training, interval * 60):
                sh_decrease.append(float(res[col1]) - float(res[col2]))
                sh_diff.append(float(res[col3]))

            logging.debug('sh_decrease: %s, sh_diff: %s' % (str(sh_decrease), str(sh_diff)))

            # k-means clustering
            X = np.array(list(zip(sh_decrease, sh_diff)))
            # number of clusters (we assume one cluster: K=1)
            kmeans = KMeans(n_clusters=1)
            # fitting the input data
            kmeans = kmeans.fit(X)
            # centroid values
            C = kmeans.cluster_centers_

            # get coefficients of the line (1st order polynom = line)
            coeffs = np.polyfit(sh_decrease, sh_diff, 1)

            if one_line and strategyFlag == 'polyfit_':
                for j in range(0, len(DistanceToLine.ventilation_length_events(training, interval * 60))):
                    b = -sh_decrease[j]
                    a = sh_diff[j]
                    direction = -a / b
                    y = direction * sh_decrease[j]
                    plt.plot([0, sh_decrease[j]], [0, y], color=colors_line[i], linewidth=0.75)
                    plt.xlim(0.0, 3.0)
                    plt.ylim(0.0, 7.0)
                    j += 1

            direction = strategy.calculate(training, interval * 60, col1, col2, col3, C[0][0], C[0][1])
            y = direction * max(sh_decrease)

            if strategyFlag == "polyfit_" or strategyFlag == "center_":
                # convert the line equation
                (a, b, c) = strategy.convert_line([direction, 0])
            if strategyFlag == "trendline_":
                (a, b, c) = strategy.convert_line(coeffs)

            out_point_line[interval] = {
                'a': a,
                'b': b,
                'c': c
            }

            out_point_point[interval] = {
                'cx': C[0][0],
                'cy': C[0][1],
            }

            # evaluate polynom
            yFitted = np.polyval(coeffs, sh_decrease)

            # plot graphs
            # plot points
            plt.scatter(sh_decrease, sh_diff, marker='x', color=colors_trendline[i], zorder=3)

            if not cluster_boundaries and not cluster_boundaries_all:
                # plot cluster centroid
                plt.scatter(C[0][0], C[0][1], marker='o', color=colors_trendline[i], zorder=3)

                if strategyFlag == 'polyfit_':
                    plt.plot([0, max(sh_decrease)], [0, y], color=colors_trendline[i], label=str(interval) + ' min')
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 7.0)
                    plt.grid(zorder=0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        return out_point_line, out_point_point, fig

                if strategyFlag == 'center_':
                    plt.plot([0, max(sh_decrease)], [0, y], color=colors_trendline[i], label=str(interval) + ' min')
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 6.0)
                    plt.grid(zorder=0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        return out_point_line, out_point_point, fig

                if strategyFlag == 'trendline_':
                    # plot trendline of the cluster
                    plt.plot(sh_decrease, yFitted, color=colors_trendline[i], label=str(interval) + ' min')
                    plt.grid(zorder=0)
                    plt.xlim(0.0, 4.0)
                    plt.ylim(0.0, 6.0)
                    if one_line:
                        plt.xlim(0.0, 3.0)
                        plt.ylim(0.0, 5.0)
                        return out_point_line, out_point_point, fig

            if cluster_boundaries or cluster_boundaries_all:
                plt.plot(C[0][0], C[0][1], marker="o", color=colors_trendline[i], markersize=10, markeredgecolor='k',
                     markeredgewidth=2)

                # plot filled boundaries
                xy = np.array([sh_decrease, sh_diff])
                xy = np.transpose(xy)

                # get boundaries
                hull = ConvexHull(xy)

                for simplex in hull.simplices:
                    plt.plot(xy[simplex, 0], xy[simplex, 1], '-k', linewidth=1.0)

                plt.fill(xy[hull.vertices, 0], xy[hull.vertices, 1], color=colors_line[i], label=str(interval) + ' min')
            i += 1

        if not one_line:
            plt.legend()
        plt.grid(zorder=0)

        return out_point_line, out_point_point, fig

    def distance_point_line(self, a1, a2, a, b, c):
        """ Calculates distance from point to line

        :param a1: point coordinate x
        :param a2: point coordinate y
        :param a: parameter of the line equation
        :param b: parameter of the line equation
        :param c: parameter of the line equation
        """

        return float(abs(a * a1 + b * a2 + c) / (np.sqrt(a ** 2 + b ** 2)))

    def distance_point_point_Euclidean(self, a1, a2, b1, b2):
        """ Calculates distance from point to point (Euclidean)

        :param a1: point 1 coordinate x
        :param a2: point 1 coordinate y
        :param b1: point 2 coordinate x
        :param b2: point 2 coordinate y
        """

        return float(np.sqrt((b1 - a1) ** 2 + (b2 - a2) ** 2))

    def exec(self, intervals, data_testing, col1, col2, col3, strategy, strategyFlag, one_line, test_points,
             cluster_boundaries, cluster_boundaries_all, precision=2):
        if self.model is None:
            line, point, fig = self.humidity_clusters(self.training, col1, col2, col3, intervals,
                                                      strategy, strategyFlag, one_line, cluster_boundaries,
                                                      cluster_boundaries_all)

            self.model = {
                'line' + strategyFlag: line,
                'point' + strategyFlag: point,
                'fig' + strategyFlag: fig,
            }

            if not cluster_boundaries:
                if strategyFlag == 'trendline_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('trendline.eps')

                if strategyFlag == 'polyfit_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('avg_trendline.eps')

                if strategyFlag == 'center_':
                    plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                    plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                    self.model['fig' + strategyFlag].savefig('trendline_passing_cluster_centroid.eps')

            if one_line:
                return

            if cluster_boundaries:
                plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                plt.xlim(0.0, 5.0)
                plt.ylim(1.0, 6.0)
                self.model['fig' + strategyFlag].savefig('model.pdf')
                return

            if cluster_boundaries_all:
                plt.xlabel('Decrease of $SH_{in}$ [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ [g/kg]')
                plt.xlim(0.0, 5.0)
                plt.ylim(1.0, 6.0)
                self.model['fig' + strategyFlag].savefig('model_all.pdf')
                return

        out = []
        for row in data_testing:
            dist_point_line = []
            dist_point_point = []
            x = float(row[col1]) - float(row[col2])
            y = float(row[col3])

            for interval in intervals:
                coeff = self.model['line' + strategyFlag][interval]

                # calculate the distance point-line
                dist = self.distance_point_line(x, y,
                                                float(coeff['a']),
                                                float(coeff['b']),
                                                coeff['c'])
                row['min_pl_' + strategyFlag + str(interval)] = round(dist, precision)
                dist_point_line.append(dist)
                coord = self.model['point' + strategyFlag][interval]

                # calculate the distance point-point
                dist = self.distance_point_point_Euclidean(x, y, coord['cx'], coord['cy'])
                row['min_pp_' + str(interval)] = round(dist, precision)
                dist_point_point.append(dist)

            out.append(row)

            if test_points:
                plt.scatter(x, y, 80, marker='o', color='black')
                fname = 'out_{0}_{1}.png'.format(x, y)
                title_graph = 'P = [%g, %g]' % (x, y)
                plt.title(title_graph)
                plt.xlabel('Decrease of $SH_{in}$ sensor 2 [g/kg]')
                plt.ylabel('$SH_{in}$ - $SH_{out}$ sensor 2 [g/kg]')
                self.model['fig' +  strategyFlag].savefig(fname)
                plt.scatter(x, y, 80, marker='o', color='white')

        return out

    @staticmethod
    def select_attributes(data, attributes):
        out = []
        for row in data:
            new_row = []
            for key, value in row.items():
                if key in attributes:
                    new_row.append((key, value))
            out.append(OrderedDict(new_row))

        return out