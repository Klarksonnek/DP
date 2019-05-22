""" Calculates average slope of multiple lines.
"""
from dm.coefficients import AbstractLineCoefficients
from dm.coefficients.DistanceToLine import DistanceToLine

__author__ = ''
__email__ = ''


class MathLineAvgSlope(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            b = -(float(row[col1]) - float(row[col2]))
            a = float(row[col3])
            direction.append(-a / b)

        return sum(direction) / float(len(direction))

