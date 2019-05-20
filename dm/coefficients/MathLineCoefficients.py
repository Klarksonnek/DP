from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

DATA_CACHE = None

from dm.coefficients.AbstractLineCoefficients import AbstractLineCoefficients
from dm.coefficients.DistanceToLine import DistanceToLine


class MathLineCoefficients(AbstractLineCoefficients):
    def calculate(self, data, interval, col1, col2, col3, point_x, point_y):
        direction = []
        for row in DistanceToLine.ventilation_length_events(data, interval):
            b = -(float(row[col1]) - float(row[col2]))
            a = float(row[col3])
            direction.append(-a / b)

        return sum(direction) / float(len(direction))

