"""Calculates slope of a line passing through a point.
"""
from dm.coefficients.AbstractLineCoefficients import AbstractLineCoefficients

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class CenterLineSlope(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        a = point_y
        b = -point_x

        return -a / b

