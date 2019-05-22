"""Converts relative humidity to absolute humidity, relative humidity to specific humidity and
   ppm to milligrams per cubic meter.
"""
from math import exp

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class ValueConversionUtil:
    CO_MOLECULAR_WEIGHT = 44.0095  # g / mol

    @staticmethod
    def rh_to_absolute_g_m3(temp: float, rh: float) -> float:
        result = (6.112 * exp((17.67 * temp) / (temp + 243.5)) * rh * 2.1674)
        result = result / (273.15 + temp)

        return result

    @staticmethod
    def rh_to_specific_g_kg(temp: float, rh: float) -> float:
        saturated_partial_pressure = exp(23.58 - (4044.6 / (235.63 + temp)))
        partial_pressure = (rh * saturated_partial_pressure) / 100
        res = (622 * partial_pressure) / (101500 - partial_pressure)

        return res

    @staticmethod
    # http://www.aresok.org/npg/nioshdbs/calc.htm
    def co2_ppm_to_mg_m3(co2):
        return co2 * ValueConversionUtil.CO_MOLECULAR_WEIGHT / 24.45
