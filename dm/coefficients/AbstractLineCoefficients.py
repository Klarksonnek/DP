"""Gets coefficients of equation in form ax + by + c = 0 from equation in form y = kx + q.
"""
from abc import ABC, abstractmethod
from fractions import Fraction
from sympy import *
import numpy as np

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class AbstractLineCoefficients(ABC):
    def __init__(self):
        super(AbstractLineCoefficients, self).__init__()

    @abstractmethod
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        pass

    def convert_line(self, coeffs):
        if coeffs[1] == 0:
            return self._convert_line_to_general_without_c(coeffs)

        return self._convert_line_to_general(coeffs)

    def _convert_line_to_general(self, coeffs):
        """ Converts line equation y = kx + q to the form ax + by + c = 0 (general form).
        """

        # represents coeffs as fractions
        tmp = Fraction(str(coeffs[0])).limit_denominator(1000)
        n1 = tmp.numerator
        d1 = tmp.denominator

        tmp2 = Fraction(str(coeffs[1])).limit_denominator(1000)
        n2 = tmp2.numerator
        d2 = tmp2.denominator

        # find LCM
        L = np.lcm(d1, d2)

        # symbolic variable
        x = var('x')

        y1 = (n1 * x) / d1
        y2 = n2 / d2

        y_mult1 = y1 * L

        a = y_mult1.subs('x', 1) * (-1)

        y_mult2 = (y2 * L)
        c = y_mult2 * (-1)

        b = L

        return a, b, c

    def _convert_line_to_general_without_c(self, coeffs):
        """ Converts line equation y = kx to the form ax + by = 0 (general form)
        """

        # represents coeffs as fractions
        tmp = Fraction(str(coeffs[0])).limit_denominator(1000)
        n1 = tmp.numerator
        d1 = tmp.denominator

        # symbolic variable
        x = var('x')

        y1 = (n1 * x) / d1

        y_mult1 = y1 * d1

        a = y_mult1.subs('x', 1) * (-1)

        b = d1

        return a, b, 0
