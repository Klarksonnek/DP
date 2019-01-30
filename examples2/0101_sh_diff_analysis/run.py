from collections import OrderedDict
import logging
import sys
from os.path import dirname, abspath, join
from scipy import stats

CODE_DIR = abspath(join(dirname(__file__), '../..', ''))
sys.path.append(CODE_DIR)

from dm.DateTimeUtil import DateTimeUtil
from dm.Graph import Graph
from dm.FilterUtil import FilterUtil
from dm.ConnectionUtil import ConnectionUtil
from dm.Storage import Storage
from dm.CSVUtil import CSVUtil


def liner_reg_before(event: dict, column: str):
    values = event['measured'][column]

    x = []
    y = []

    for i in range(0, event['start_shift']*(-1)):
        x.append(i)
        y.append(values[i])

    slope, intercept, _, _, _ = stats.linregress(x, y)

    return slope, intercept


def linear_reg_after(event: dict, column: str):
    values = event['measured'][column]

    x = []
    y = []

    t = len(values) - event['end_shift']
    for i in range(t, len(values)):
        x.append(i - t)
        y.append(values[i])

    slope, intercept, _, _, _ = stats.linregress(x, y)

    return slope, intercept


def gen_graphs(event: dict, number_output_records: int, sh_attr_name: str,
               lin_reg_attr_name: str):
    """Vygenerovanie grafu zo senzora cislo jedna.

    :param event: event, ktory sa pouzije pre generovanie statistiky
    :param number_output_records: pocet bodov, ktore maju byt vo vyslednom grafe
    :param sh_attr_name:
    :param lin_reg_attr_name:
    :return: vysledny grah, ktory moze v sebe obsahovat niekolko grafov
    """

    n = number_output_records
    graphs = []

    t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
    t += ' - '
    t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

    g = {
        'title': 'Specific hum in and out ' + t,
        'group': 'one',
        'graphs': [
            Graph.db_to_simple_graph(event, sh_attr_name, 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_specific_g_kg', 'red', 'hum out', n),
            Graph.db_to_simple_graph(event, lin_reg_attr_name, 'orange', 'Lin reg', n),
        ]
    }
    graphs.append(g)

    return graphs


def linear_reg(sensor1_events: list, input_attr_name: str, output_attr_name: str):
    for i in range(0, len(sensor1_events)):
        event = sensor1_events[i]

        slope_b, intercept_b = liner_reg_before(event, input_attr_name)
        slope_a, intercept_a = linear_reg_after(event, input_attr_name)

        out = []
        values = event['measured']['rh_in_specific_g_kg']
        for k in range(0, len(values)):
            if k < (event['start_shift'] * (-1)):
                out.append(intercept_b + slope_b * k)
                continue

            if k > (len(values) - event['end_shift']):
                out.append(intercept_a + slope_a * (k - (len(values) - event['end_shift'])))
                continue

            out.append(None)

        event['measured'][output_attr_name] = out


def humidity_info_csv(events, start_shift, end_shift, precision=2):
    out = []

    for event in events:
        specific_in_start = event['measured']['linear1_sh'][0 - (start_shift + 1)]
        specific_in_end = event['measured']['linear1_sh'][-end_shift + 1]

        absolute_in_start = event['measured']['linear1_ah'][0 - (start_shift + 1)]
        absolute_in_end = event['measured']['linear1_ah'][-end_shift + 1]

        temp_in_start = event['measured']['linear1_temp'][0 - (start_shift + 1)]
        temp_in_end = event['measured']['linear1_temp'][-end_shift + 1]

        specific_in_start_2 = event['measured']['linear2_sh'][0 - (start_shift + 1)]
        specific_in_end_2 = event['measured']['linear2_sh'][-end_shift + 1]

        absolute_in_start_2 = event['measured']['linear2_ah'][0 - (start_shift + 1)]
        absolute_in_end_2 = event['measured']['linear2_ah'][-end_shift + 1]

        temp_in_start_2 = event['measured']['linear2_temp'][0 - (start_shift + 1)]
        temp_in_end_2 = event['measured']['linear2_temp'][-end_shift + 1]

        specific_in = event['measured']['rh_in_specific_g_kg'][0 - (start_shift + 1)]
        specific_out = event['measured']['rh_out_specific_g_kg'][-end_shift + 1]

        absolute_in = event['measured']['rh_in_absolute_g_m3'][0 - (start_shift + 1)]
        absolute_out = event['measured']['rh_out_absolute_g_m3'][-end_shift + 1]

        temp_in = event['measured']['temperature_in_celsius'][0 - (start_shift + 1)]
        temp_out = event['measured']['temperature_out_celsius'][-end_shift + 1]

        specific_in_2 = event['measured']['rh_in2_specific_g_kg'][0 - (start_shift + 1)]
        absolute_in_2 = event['measured']['rh_in2_absolute_g_m3'][0 - (start_shift + 1)]
        temp_in_2 = event['measured']['temperature_in2_celsius'][0 - (start_shift + 1)]

        out.append(OrderedDict([
            ('start_datetime', event['e_start']['readable']),
            ('end_datetime', event['e_end']['readable']),
            ('diff_sh_in_1', round(abs(specific_in_start - specific_in_end), precision)),
            ('diff_sh_1', round(abs(specific_out - specific_in), precision)),
            ('diff_ah_in_1', round(abs(absolute_in_start - absolute_in_end), precision)),
            ('diff_ah_1', round(abs(absolute_out - absolute_in), precision)),
            ('diff_temp_in_1', round(abs(temp_in_start - temp_in_end), precision)),
            ('diff_temp_1', round(abs(temp_out - temp_in), precision)),
            ('diff_sh_in_2', round(abs(specific_in_start_2 - specific_in_end_2), precision)),
            ('diff_sh_2', round(abs(specific_out - specific_in_2), precision)),
            ('diff_ah_in_2', round(abs(absolute_in_start_2 - absolute_in_end_2), precision)),
            ('diff_ah_2', round(abs(absolute_out - absolute_in_2), precision)),
            ('diff_temp_in_2', round(abs(temp_in_start_2 - temp_in_end_2), precision)),
            ('diff_temp_2', round(abs(temp_out - temp_in_2), precision))
        ]))

    CSVUtil.create_csv_file(out, 'humidity_info.csv')

    return out


def main(events_file: str, start_shift: int, end_shift: int, output_filename: str,
         output_records: int):
    logging.info('start')
    graphs = Graph("./../../src/graph")

    # stiahnutie dat
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, 0, 'measured_klarka')
    d = storage.load_data(con, start_shift, end_shift, 'temperature_in_celsius')
    logging.info('downloaded events: %d' % len(d))

    # aplikovanie filtrov na eventy
    filtered = FilterUtil.only_valid_events(d)

    min_timestamp = int(DateTimeUtil.local_time_str_to_utc('2018/11/01 00:01:00').timestamp())
    filtered = FilterUtil.min_timestamp(filtered, min_timestamp)

    logging.info('events after applying the filters: %d' % len(filtered))

    # data pre generovanie grafov zo senzora 1
    sensor1_events = filtered
    logging.info('event count: %d for senzor 1' % len(sensor1_events))
    linear_reg(sensor1_events, 'rh_in_specific_g_kg', 'linear1_sh')
    linear_reg(sensor1_events, 'rh_in_absolute_g_m3', 'linear1_ah')
    linear_reg(sensor1_events, 'temperature_in_celsius', 'linear1_temp')

    # generovanie grafov pre senzor 1
    logging.info('start generating graphs of events from sensor 1')
    graphs_sensor_1 = []
    for event in sensor1_events:
        graphs_sensor_1 += gen_graphs(event, output_records, 'rh_in_specific_g_kg', 'linear1_sh')
        graphs_sensor_1 += gen_graphs(event, output_records, 'rh_in_absolute_g_m3', 'linear1_ah')

    graphs.gen(graphs_sensor_1, 'sensor1_' + output_filename, 0, 0, global_range=True)
    logging.info('end generating graphs of events from sensor 1')

    # data pre generovanie grafov zo senzora 2
    sensor2_events = filtered
    logging.info('event count: %d for sensor 2' % len(sensor2_events))

    sensor2_events = FilterUtil.measured_values_not_empty(sensor2_events, 'rh_in2_specific_g_kg')
    sensor2_events = FilterUtil.measured_values_not_empty(sensor2_events, 'rh_in2_absolute_g_m3')
    sensor2_events = FilterUtil.measured_values_not_empty(sensor2_events, 'temperature_in2_celsius')
    logging.info('events after applying the filter: %d' % len(sensor2_events))

    linear_reg(sensor2_events, 'rh_in2_specific_g_kg', 'linear2_sh')
    linear_reg(sensor2_events, 'rh_in2_absolute_g_m3', 'linear2_ah')
    linear_reg(sensor2_events, 'temperature_in2_celsius', 'linear2_temp')

    humidity_info_csv(sensor2_events, start_shift, end_shift)

    # generovanie grafov pre senzor 2
    logging.info('start generating graphs of events from sensor 2')
    graphs_sensor_2 = []
    for event in sensor2_events:
        graphs_sensor_2 += gen_graphs(event, output_records, 'rh_in2_specific_g_kg', 'linear2_sh')

    graphs.gen(graphs_sensor_2, 'sensor2_' + output_filename, 0, 0, global_range=True)
    logging.info('end generating graphs of events from sensor 2')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    main('examples/events_klarka.json', -600, 600, 'spec_hum.html', 120)
