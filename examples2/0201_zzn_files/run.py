from collections import OrderedDict
from os.path import dirname, abspath, join
import csv
import sys
import logging
import numpy as np
from scipy.optimize import curve_fit

THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage
from dm.Differences import Differences


def prepare_no_event_value(values: tuple, precision: int):
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


def detect_action(values_count: int, actual_index: int):
    if actual_index == 0:
        return 'open'
    elif values_count - 1 == actual_index:
        return 'close'
    else:
        return 'nothing'


def prepare_one_row(measured: dict, value_index: int, timestamp: int, precision: int):
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
        ('event', detect_action(len(measured['co2_in_ppm']), value_index)),

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


def prepare_file_1(events: list):
    precision = 2
    out = []

    for event in events:
        start = event['e_start']['timestamp']

        values_count = len(event['measured']['co2_in_ppm'])
        for i in range(0, values_count):
            # zapiseme len prvy zaznam
            if i != 0:
                continue

            item = prepare_one_row(event['measured'], i, start + i, precision)
            item['wind'] = event['wind']
            item['sun'] = event['sun']
            item['sky'] = event['sky']
            item['rain'] = event['rain']
            item['people'] = event['people']
            out.append(item)

            item = prepare_no_event_value(event['no_event_values'], precision)
            item['wind'] = event['wind']
            item['sun'] = event['sun']
            item['sky'] = event['sky']
            item['rain'] = event['rain']
            item['people'] = event['people']
            out.append(item)

    return out


def prepare_file_2(events: list):
    out = []

    for event in events:
        start = event['e_start']['timestamp']
        derivation = event['derivation']

        item = [
            ('datetime', DateTimeUtil.utc_timestamp_to_str(start, '%Y-%m-%d %H:%M:%S')),
            ('event', 'open')
        ]
        Differences.prepare_one_row(derivation, 'before', 'before', item)
        Differences.prepare_one_row(derivation, 'after', 'after', item)
        out.append(OrderedDict(item))

        t = start + event['no_event_time_shift']
        item2 = [
            ('datetime', DateTimeUtil.utc_timestamp_to_str(t, '%Y-%m-%d %H:%M:%S')),
            ('event', 'nothing')
        ]
        Differences.prepare_one_row(derivation, 'before', 'no_event_before', item2)
        Differences.prepare_one_row(derivation, 'after', 'no_event_after', item2)
        out.append(OrderedDict(item2))

    return out


def prepare_file_3(events: list, last_index=-1, precision=1):
    out = []
    p = precision

    k = last_index

    for event in events:
        start = event['e_start']['timestamp']
        end = event['e_end']['timestamp']

        if k > (end - start):
            # logging.warning('event with start in `%s` is too short' % event['e_start']['readable'])
            continue

        measured = event['measured']
        values_count = len(measured['co2_in_ppm'])
        co2_values = measured['co2_in_ppm']

        temperature_diff = measured['temperature_in_celsius'][0] - \
                           measured['temperature_out_celsius'][-1]

        humidity_rh_diff = measured['rh_in_percentage'][0] - \
                           measured['rh_out_percentage'][-1]
        humidity_abs_diff = measured['rh_in_absolute_g_m3'][0] - \
                            measured['rh_out_absolute_g_m3'][-1]
        humidity_spec_diff = measured['rh_in_specific_g_kg'][0] - \
                             measured['rh_out_specific_g_kg'][-1]

        item = [
            ('datetime', DateTimeUtil.utc_timestamp_to_str(start, '%Y-%m-%d %H:%M:%S')),
            ('air_exchange_rate', round(event['exp_reg']['a_hod'], p)),
            ('duration', end - start),
            ('co2_ppm_diff', round(co2_values[0] - co2_values[values_count - 1], p)),

            ('temperature_diff', round(temperature_diff, p)),
            ('humidity_rh_diff', round(humidity_rh_diff, p)),
            ('humidity_abs_diff', round(humidity_abs_diff, p)),
            ('humidity_spec_diff', round(humidity_spec_diff, p)),

            ('start_co2_in_ppm', round(measured['co2_in_ppm'][0], p)),
            ('start_temperature_in_celsius', round(measured['temperature_in_celsius'][0], p)),
            ('start_temperature_out_celsius', round(measured['temperature_out_celsius'][0], p)),
            ('start_humidity_in_relative_percent', round(measured['rh_in_percentage'][0], p)),
            ('start_humidity_in_absolute_g_m3', round(measured['rh_in_absolute_g_m3'][0], p)),
            ('start_humidity_in_specific_g_kg', round(measured['rh_in_specific_g_kg'][0], p)),
            ('start_humidity_out_relative_percent', round(measured['rh_out_percentage'][0], p)),
            ('start_humidity_out_absolute_g_m3', round(measured['rh_out_absolute_g_m3'][0], p)),
            ('start_humidity_out_specific_g_kg', round(measured['rh_out_specific_g_kg'][0], p)),
            ('start_pressure_in_hpa', round(measured['pressure_in_hpa'][0], p)),

            ('end_co2_in_ppm', round(measured['co2_in_ppm'][-1], p)),
            ('end_temperature_in_celsius', round(measured['temperature_in_celsius'][-1], p)),
            ('end_temperature_out_celsius', round(measured['temperature_out_celsius'][-1], p)),
            ('end_humidity_in_relative_percent', round(measured['rh_in_percentage'][-1], p)),
            ('end_humidity_in_absolute_g_m3', round(measured['rh_in_absolute_g_m3'][-1], p)),
            ('end_humidity_in_specific_g_kg', round(measured['rh_in_specific_g_kg'][-1], p)),
            ('end_humidity_out_relative_percent', round(measured['rh_out_percentage'][-1], p)),
            ('end_humidity_out_absolute_g_m3', round(measured['rh_out_absolute_g_m3'][-1], p)),
            ('end_humidity_out_specific_g_kg', round(measured['rh_out_specific_g_kg'][-1], p)),
            ('end_pressure_in_hpa', round(measured['pressure_in_hpa'][-1], p)),
        ]

        out.append(OrderedDict(item))

    return out


def create_csv_file(data: list, filename: str):
    field_names = []
    for key, _ in data[0].items():
        field_names.append(key)

    with open(filename, 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=field_names)

        csv_writer.writeheader()
        for item in data:
            csv_writer.writerow(item)


def detect_sensor_delays(events, time_interval, threshold):
    for i in range(0, len(events)):
        event = events[i]

        values = event['measured']['co2_in_ppm']
        event['co2_sensor_delays'] = 0

        for k in range(0, len(values) - time_interval):
            first_value = values[k] - threshold
            second_value = values[k + time_interval]

            if first_value > second_value:
                event['co2_sensor_delays'] = k
                break

    return events


def gen_f_variant1(co2_start, co2_out, volume):
    return lambda x, a: co2_out + (co2_start - co2_out) * np.exp(-a / volume * x)


def exp_regression(events, co2_out, volume):
    for i in range(0, len(events)):
        event = events[i]

        values = event['measured']['co2_in_ppm']
        start = event['e_start']['timestamp']
        end = event['e_end']['timestamp']

        shift = event['co2_sensor_delays']

        x = []
        y = values[shift:]
        for k in range(0, end - start - shift +1 ):
            x.append(k)

        x = np.asarray(x)
        y = np.asarray(y)

        f_1 = gen_f_variant1(values[0], co2_out, volume)
        popt_1, pcov_1 = curve_fit(f_1, x, y)

        event['exp_reg'] = {
            'a': tuple(popt_1)[0],
            'a_hod': tuple(popt_1)[0] * 3600,
            'eq': str(co2_out) + ' + (' + str(
                values[0]) + ' - ' + str(
                co2_out) + ') * exp(-(' + str(
                tuple(popt_1)[0]) + ') / ' + str(volume) + ' * x)',
        }

    return events


def main(events_file: str, interval_before: list, interval_after: list,
         no_event_time_shift: int):
    logging.info('start')

    table_name = 'measured_peto'

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, no_event_time_shift, table_name)
    d = storage.load_data(con, 0, 0, 'co2_in_ppm')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter: %d' % len(filtered))

    # pocitanie derivacii
    logging.info('start computing of derivation')
    Differences.prepare_derivation(con, filtered, interval_before, interval_after, table_name,
                                   2, 'co2_in_ppm', 16)
    logging.info('end computing of derivation')

    # aplikovanie filtra na overenie spravnosti eventov po vypocitani derivacii
    # dovodom nevalidneho eventu po tejto operacii moze byt napr. chybaju hodnota
    # v case, z ktoreho sa mala pocitat derivacia
    filtered = FilterUtil.only_valid_events(d)
    logging.info('events after applying the filter (invalid derivation): %d' % len(filtered))

    # aplikovanie filtra na nenulove derivacie
    filtered = FilterUtil.derivation_not_zero(filtered)
    logging.info('events after applying the filter (non zero derivation): %d' % len(filtered))

    logging.info('start preparing file with number: 1')
    data_1 = prepare_file_1(filtered)
    create_csv_file(data_1, 'f1.csv')
    logging.info('end preparing file with number: 1')

    logging.info('start preparing file with number: 2')
    data_2 = prepare_file_2(filtered)
    create_csv_file(data_2, 'f2.csv')
    logging.info('end preparing file with number: 2')

    logging.info('start detecting of sensor delays')
    filtered = detect_sensor_delays(filtered, 10, 10)
    logging.info('end detecting of sensor delays')

    logging.info('start exp regression')
    filtered = exp_regression(filtered, 450, 48)
    logging.info('end exp regression')

    logging.info('start preparing file with number: 3')
    for k in [5*60, 10*60, 15*60, 20*60, 30*60, 40*60, 50*60, 60*60]:
        data_3 = prepare_file_3(filtered, k)
        filename = 'f3_{0}.csv'.format(k)
        create_csv_file(data_3, filename)
        logging.info('%s with row: %s' % (filename, len(data_3)))
    logging.info('end preparing file with number: 3')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    interval = [60, 75, 90, 105, 120, 135, 150, 165, 180]
    main('examples/events_peto.json', interval, interval, -500)
