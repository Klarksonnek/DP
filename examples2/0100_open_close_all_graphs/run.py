"""Generates graph of temperature and humidity with basic information (window opening).
"""
from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '../..', '')))

from dm.ConnectionUtil import ConnectionUtil
from dm.DateTimeUtil import DateTimeUtil
from dm.FilterUtil import FilterUtil
from dm.Graph import Graph
from dm.Storage import Storage
import logging

__author__ = 'Klára Nečasová'
__email__ = 'xnecas24@stud.fit.vutbr.cz'


def generate_info(event: dict, owner: str, precision: int=2):
    """Generates basic information about given event

    :param event: basic information about event
    :param owner: sensor owner(klarka|peto), name must be the same as in database
    :param precision: number of decimal places for result rounding
    :return: basic information about event
    """

    measured = event['measured']

    out = [
        ('teplota dnu', round(measured['temperature_in_celsius'][0], precision)),
        ('teplota von', round(measured['temperature_out_celsius'][0], precision)),
        ('rozdiel teplot', round(abs(
            measured['temperature_in_celsius'][0] - measured['temperature_out_celsius'][0]),
                                 precision)),

        ('', ''),
        ('rh dnu', round(measured['rh_in_percentage'][0], precision)),
        ('rh von', round(measured['rh_out_percentage'][0], precision)),
        ('rozdiel rh',
         round(abs(measured['rh_in_percentage'][0] - measured['rh_out_percentage'][0]),
               precision)),

        ('', ''),
        ('abs rh dnu', round(measured['rh_in_absolute_g_m3'][0], precision)),
        ('abs rh von', round(measured['rh_out_absolute_g_m3'][0], precision)),
        ('rozdiel abs rh',
         round(abs(measured['rh_in_absolute_g_m3'][0] - measured['rh_out_absolute_g_m3'][0]),
               precision)),

        ('', ''),
        ('spec rh dnu', round(measured['rh_in_specific_g_kg'][0], precision)),
        ('spec rh von', round(measured['rh_out_specific_g_kg'][0], precision)),
        ('rozdiel spec rh',
         round(abs(measured['rh_in_specific_g_kg'][0] - measured['rh_out_specific_g_kg'][0]),
               precision)),
    ]

    if owner == 'klarka':
        out.append(('typ grafu', event['graph_hum_type_1']))

    return out


def generate_graphs_sensor_1(event: dict, owner: str, number_output_records: int):
    """Generates graph based on data measured using sensor 1.

    :param event: basic information about event
    :param owner: sensor owner(klarka|peto), name must be the same as in database
    :param number_output_records: number of points that are required in graph
    :return: graph that can contain several graphs
    """

    n = number_output_records
    graphs = []

    t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
    t += ' - '
    t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

    g = {
        'title': 'Temp in and out ' + t,
        'stat': generate_info(event, owner),
        'graphs': [
            Graph.db_to_simple_graph(event, 'temperature_in_celsius', 'DarkRed', 'temp in', n),
            Graph.db_to_simple_graph(event, 'temperature_out_celsius', 'LightCoral', 'temp out', n)
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Relative hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in_percentage', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_percentage', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Specific hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in_specific_g_kg', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_specific_g_kg', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Absolute hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in_absolute_g_m3', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_absolute_g_m3', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    return graphs


def generate_graphs_sensor_2(event: dict, owner: str, number_output_records: int):
    """Generates graph based on data measured using sensor 2.

    :param event: basic information about event
    :param owner: sensor owner(klarka|peto), name must be the same as in database
    :param number_output_records: number of points that are required in graph
    :return: graph that can contain several graphs
   """

    n = number_output_records
    graphs = []

    t = DateTimeUtil.utc_timestamp_to_str(event['e_start']['timestamp'], '%d.%m. %H:%M:%S')
    t += ' - '
    t += DateTimeUtil.utc_timestamp_to_str(event['e_end']['timestamp'], '%H:%M:%S')

    g = {
        'title': 'Temp in and out ' + t,
        'stat': generate_info(event, owner),
        'graphs': [
            Graph.db_to_simple_graph(event, 'temperature_in_celsius', 'DarkRed', 'temp in', n),
            Graph.db_to_simple_graph(event, 'temperature_out_celsius', 'LightCoral', 'temp out', n)
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in2_percentage', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_percentage', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Specific hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in2_specific_g_kg', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_specific_g_kg', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    g = {
        'title': 'Absolute hum in and out ' + t,
        'graphs': [
            Graph.db_to_simple_graph(event, 'rh_in2_absolute_g_m3', 'blue', 'hum in', n),
            Graph.db_to_simple_graph(event, 'rh_out_absolute_g_m3', 'red', 'hum out', n),
        ]
    }
    graphs.append(g)

    return graphs


def main(events_file: str, owner: str, start_shift: int, end_shift: int,
         output_filename: str, number_output_records: int):
    """

    :param events_file: path to file containing list of events
    :param owner: sensor owner(klarka|peto), name must be the same as in database
    :param start_shift: shift of beginning of data downloading
    :param end_shift: shift of end of data downloading
    :param output_filename: filename to store a graph
    :param number_output_records: number of points that are required in graph
    :return:
    """

    logging.info('start: ' + output_filename)
    graphs = Graph("./../../src/graph")

    # download data
    con = ConnectionUtil.create_con()
    storage = Storage(events_file, 0, 'measured_' + owner)
    d = storage.load_data(con, start_shift, end_shift, 'temperature_in_celsius')
    logging.info('downloaded events: %d' % len(d))

    # apply filters to downloaded data
    filtered = FilterUtil.only_valid_events(d)
    filtered = FilterUtil.temperature_diff(filtered, 5, 100)
    filtered = FilterUtil.temperature_out_max(filtered, 15)
    filtered = FilterUtil.humidity(filtered, 6, 1.6, 100)

    # for travis
    if ConnectionUtil.is_testable_system():
        filtered = filtered[:ConnectionUtil.MAX_TESTABLE_EVENTS]

    if owner == 'klarka':
        filtered = FilterUtil.attribute(filtered, 'window', 'dokoran')

    logging.info('events after applying the filter: %d' % len(filtered))

    # data for graph generation measured using sensor 1
    sensor1_events = filtered
    logging.info('event count: %d for senzor 1' % len(sensor1_events))

    # data for graph generation measured using sensor 2
    sensor2 = ['rh_in2_percentage', 'rh_in2_specific_g_kg', 'rh_in2_absolute_g_m3']
    sensor2_events = FilterUtil.measured_values_not_empty(filtered, sensor2)
    logging.info('event count: %d for senzor 2' % len(sensor2_events))

    # graph generation - sensor 1
    logging.info('start generating graphs of events from sensor 1')
    graphs_sensor_1 = []
    for event in sensor1_events:
        graphs_sensor_1 += generate_graphs_sensor_1(event, owner, number_output_records)

    graphs.gen(graphs_sensor_1, 'sensor1_' + output_filename, 0, 0)
    logging.info('end generating graphs of events from sensor 1')

    # graph generation - sensor 2
    logging.info('start generating graphs of events from sensor 2')
    graphs_sensor_2 = []
    for event in sensor2_events:
        graphs_sensor_2 += generate_graphs_sensor_2(event, owner, number_output_records)

    graphs.gen(graphs_sensor_2, 'sensor2_' + output_filename, 0, 0)
    logging.info('end generating graphs of events from sensor 2')

    logging.info('end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',)

    main('examples/events_klarka.json', 'klarka', 0, 0, 'klarka_temp_hum_abs_spec.html', 75)
    main('examples/events_peto.json', 'filtered_peto', 0, 0, 'peto_temp_hum_abs_spec.html', 75)

    main('examples/events_klarka.json', 'klarka', -3600, 3600,
         'klarka_temp_hum_abs_spec_shift.html', 75)
    main('examples/events_peto.json', 'filtered_peto', 3600, 3600,
         'peto_temp_hum_abs_spec_shift.html', 75)
