from collections import OrderedDict
from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil


class ValueUtil:
    @staticmethod
    def detect_sensor_delay(values, window_size, threshold):
        for k in range(0, len(values) - window_size):
            first_value = values[k] - threshold
            second_value = values[k + window_size]

            if first_value - second_value > threshold:
                return k

        return 0

    @staticmethod
    def delays(events, delays_attr_name):
        out = []
        for event in events:
            out.append(event[delays_attr_name])

        return out

    @staticmethod
    def detect_window_action(values_count: int, actual_index: int):
        if actual_index == 0:
            return 'open'
        elif values_count - 1 == actual_index:
            return 'close'
        else:
            return 'nothing'

    @staticmethod
    def window_no_event_value(values: tuple, precision: int):
        outer_co2_ppm = 435

        p = precision

        temperature_diff = values[4] - values[6]
        humidity_rh_diff = values[7] - values[13]
        humidity_abs_diff = values[9] - values[14]
        humidity_spec_diff = values[11] - values[15]

        return OrderedDict([
            ('datetime', DateTimeUtil.utc_timestamp_to_str(values[0], '%Y-%m-%d %H:%M:%S')),
            ('event', 'nothing'),

            ('co2_in_ppm', round(values[16], p)),
            ('co2_out_ppm', round(outer_co2_ppm, p)),

            ('temperature_in_celsius', round(values[4], p)),
            ('temperature_out_celsius', round(values[6], p)),

            ('humidity_in_relative_percent', round(values[7], p)),
            ('humidity_in_absolute_g_m3', round(values[9], p)),
            ('humidity_in_specific_g_kg', round(values[11], p)),

            ('humidity_out_relative_percent', round(values[13], p)),
            ('humidity_out_absolute_g_m3', round(values[14], p)),
            ('humidity_out_specific_g_kg', round(values[15], p)),

            ('pressure_in_hpa', round(values[4], p)),

            ('temperature_celsius_difference', round(temperature_diff, p)),
            ('humidity_relative_percent_difference', round(humidity_rh_diff, p)),
            ('humidity_absolute_g_m3_difference', round(humidity_abs_diff, p)),
            ('humidity_specific_g_kg_difference', round(humidity_spec_diff, p)),
        ])

    @staticmethod
    def window_event_value(measured: dict, value_index: int, timestamp: int, precision: int):
        outer_co2_ppm = 435

        p = precision
        i = value_index

        temperature_diff = measured['temperature_in_celsius'][i] - \
                           measured['temperature_out_celsius'][i]

        humidity_rh_diff = measured['rh_in_percentage'][i] - \
                           measured['rh_out_percentage'][i]
        humidity_abs_diff = measured['rh_in_absolute_g_m3'][i] - \
                            measured['rh_out_absolute_g_m3'][i]
        humidity_spec_diff = measured['rh_in_specific_g_kg'][i] - \
                             measured['rh_out_specific_g_kg'][i]

        return OrderedDict([
            ('datetime', DateTimeUtil.utc_timestamp_to_str(timestamp, '%Y-%m-%d %H:%M:%S')),
            ('event', ValueUtil.detect_window_action(len(measured['co2_in_ppm']), value_index)),

            ('co2_in_ppm', round(measured['co2_in_ppm'][i], p)),
            ('co2_out_ppm', round(outer_co2_ppm, p)),

            ('temperature_in_celsius', round(measured['temperature_in_celsius'][i], p)),
            ('temperature_out_celsius', round(measured['temperature_out_celsius'][i], p)),

            ('humidity_in_relative_percent', round(measured['rh_in_percentage'][i], p)),
            ('humidity_in_absolute_g_m3', round(measured['rh_in_absolute_g_m3'][i], p)),
            ('humidity_in_specific_g_kg', round(measured['rh_in_specific_g_kg'][i], p)),

            ('humidity_out_relative_percent', round(measured['rh_out_percentage'][i], p)),
            ('humidity_out_absolute_g_m3', round(measured['rh_out_absolute_g_m3'][i], p)),
            ('humidity_out_specific_g_kg', round(measured['rh_out_specific_g_kg'][i], p)),

            ('pressure_in_hpa', round(measured['pressure_in_hpa'][i], p)),

            ('temperature_celsius_difference', round(temperature_diff, p)),
            ('humidity_relative_percent_difference', round(humidity_rh_diff, p)),
            ('humidity_absolute_g_m3_difference', round(humidity_abs_diff, p)),
            ('humidity_specific_g_kg_difference', round(humidity_spec_diff, p)),
        ])

    @staticmethod
    def events_duration(events, max_duration):
        durations = []
        for event in events:
            duration = event['event_duration']
            if max_duration is None or duration < max_duration:
                durations.append(event['event_duration'])

        return durations
