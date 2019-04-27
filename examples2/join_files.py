import csv
import os
import logging
from dm.CSVUtil import CSVUtil

BLOCK_SIZE = 8192


def peto_co2_testing():
    output_file = '0202_open_detector/co2/co2_m4_testing.csv'

    file_names = [
        '0202_open_detector/co2/co2_1_oktober.csv',
        '0202_open_detector/co2/co2_2_november.csv',
        '0202_open_detector/co2/co2_3_december.csv',
        '0202_open_detector/co2/co2_4_januar.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_co2_general_testing():
    output_file = '0202_open_detector/co2/co2_m2_general_testing.csv'

    file_names = [
        '0202_open_detector/co2/co2_5_februar.csv',
        '0202_open_detector/co2/co2_6_marec.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_co2_t_h_testing():
    output_file = '0202_open_detector/co2_t_h/co2_t_h_m4_testing.csv'

    file_names = [
        '0202_open_detector/co2_t_h/co2_t_h_1_oktober.csv',
        '0202_open_detector/co2_t_h/co2_t_h_2_november.csv',
        '0202_open_detector/co2_t_h/co2_t_h_3_december.csv',
        '0202_open_detector/co2_t_h/co2_t_h_4_januar.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_co2_t_h_general_testing():
    output_file = '0202_open_detector/co2_t_h/co2_t_h_m2_general_testing.csv'

    file_names = [
        '0202_open_detector/co2_t_h/co2_t_h_5_februar.csv',
        '0202_open_detector/co2_t_h/co2_t_h_6_marec.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_co2_t_h_out_testing():
    output_file = '0202_open_detector/co2_t_h_out/co2_t_h_out_m4_testing.csv'

    file_names = [
        '0202_open_detector/co2_t_h_out/co2_t_h_out_1_oktober.csv',
        '0202_open_detector/co2_t_h_out/co2_t_h_out_2_november.csv',
        '0202_open_detector/co2_t_h_out/co2_t_h_out_3_december.csv',
        '0202_open_detector/co2_t_h_out/co2_t_h_out_4_januar.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_co2_t_h_out_general_testing():
    output_file = '0202_open_detector/co2_t_h_out/co2_t_h_out_m2_general_testing.csv'

    file_names = [
        '0202_open_detector/co2_t_h_out/co2_t_h_out_5_februar.csv',
        '0202_open_detector/co2_t_h_out/co2_t_h_out_6_marec.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def copy_one_file(filename, output_file):
    logging.info('processed: {0}'.format(filename))
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        out = []
        for j, row in enumerate(csv_reader):
            if j != 0 and j % BLOCK_SIZE == 0:
                CSVUtil.create_csv_file(out, output_file, True)
                out = []

            out.append(row)
        CSVUtil.create_csv_file(out, output_file, True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # peto_co2_testing()
    # peto_co2_general_testing()

    # peto_co2_t_h_testing()
    # peto_co2_t_h_general_testing()

    # peto_co2_t_h_out_testing()
    # peto_co2_t_h_out_general_testing()

    output_file = 'output.csv'

    file_names = [
        '0202_open_detector_co2/testing_only_co2/file1.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)
