import csv
import logging
from dm.CSVUtil import CSVUtil

BLOCK_SIZE = 8192


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


def peto_intrak_testing(directory):
    output_file = '0202_open_detector/{0}/m4_testing.csv'.format(directory)

    file_names = [
        '0202_open_detector/{0}/1_oktober.csv'.format(directory),
        '0202_open_detector/{0}/2_november.csv'.format(directory),
        '0202_open_detector/{0}/3_december.csv'.format(directory),
        '0202_open_detector/{0}/4_januar.csv'.format(directory),
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def peto_intrak_general_testing(directory):
    output_file = '0202_open_detector/{0}/m2_general_testing.csv'.format(directory)

    file_names = [
        '0202_open_detector/{0}/5_februar.csv'.format(directory),
        '0202_open_detector/{0}/6_marec.csv'.format(directory),
    ]

    for file in file_names:
        copy_one_file(file, output_file)


def other():
    output_file = 'output.csv'

    file_names = [
        '0202_open_detector_co2/testing_only_co2/file1.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # peto_intrak_testing('co2')
    # peto_intrak_general_testing('co2')

    # peto_intrak_testing('co2_t_h')
    # peto_intrak_general_testing('co2_t_h')

    # peto_intrak_testing('co2_t_h_out')
    # peto_intrak_general_testing('co2_t_h_out')

    other()
