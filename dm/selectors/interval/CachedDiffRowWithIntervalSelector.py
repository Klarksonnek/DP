"""Cached row selector for selection of differences of values.
"""
from dm.selectors.interval.CachedRowWithIntervalSelector import CachedRowWithIntervalSelector

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


class CachedDiffRowWithIntervalSelector(CachedRowWithIntervalSelector):
    def row(self, column_name, time):
        value = None
        if column_name == 'rh_in_percentage_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in_percentage', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_percentage', time)
            value = v1 - v2

        elif column_name == 'rh_in_specific_g_kg_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in_specific_g_kg', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_specific_g_kg', time)
            value = v1 - v2

        elif column_name == 'rh_in_absolute_g_m3_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in_absolute_g_m3', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_absolute_g_m3', time)
            value = v1 - v2

        elif column_name == 'temperature_in_celsius_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('temperature_in_celsius', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('temperature_out_celsius', time)
            value = v1 - v2

        elif column_name == 'rh_in2_percentage_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in2_percentage', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_percentage', time)
            value = v1 - v2

        elif column_name == 'rh_in2_specific_g_kg_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in2_specific_g_kg', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_specific_g_kg', time)
            value = v1 - v2

        elif column_name == 'rh_in2_absolute_g_m3_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('rh_in2_absolute_g_m3', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('rh_out_absolute_g_m3', time)
            value = v1 - v2

        elif column_name == 'temperature_in2_celsius_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('temperature_in2_celsius', time)
            v2 = super(CachedDiffRowWithIntervalSelector, self).row('temperature_out_celsius', time)
            value = v1 - v2

        elif column_name == 'co2_in_ppm_diff':
            v1 = super(CachedDiffRowWithIntervalSelector, self).row('co2_in_ppm', time)
            v2 = 300
            value = v1 - v2

        else:
            value = super(CachedDiffRowWithIntervalSelector, self).row(column_name, time)

        return value
