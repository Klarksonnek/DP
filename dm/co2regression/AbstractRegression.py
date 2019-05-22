"""Abstract class for calculation of CO2 regression using various methods.
"""
from abc import ABC, abstractmethod

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


class AbstractRegression(ABC):
    def __init__(self, co2_out):
        self._co2_out = co2_out
        super(AbstractRegression, self).__init__()

    @abstractmethod
    def compute_parameter(self, x, y):
        pass

    @abstractmethod
    def compute_curve(self, x, y):
        pass
