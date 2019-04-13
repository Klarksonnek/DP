import csv
import os
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    output_file = 'output.csv'

    file_names = [
        '0202_open_detector_co2/testing_only_co2/file1.csv',
    ]

    for file in file_names:
        copy_one_file(file, output_file)
