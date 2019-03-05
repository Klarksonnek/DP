import csv
import logging
import os


class CSVUtil:
    @staticmethod
    def create_csv_file(data: list, filename: str, enable_append=False):
        if data == []:
            logging.warning('empty data to write')
            return

        write_header = True
        if os.path.isfile(filename) and enable_append:
            write_header = False

        field_names = []
        for key, _ in data[0].items():
            field_names.append(key)

        mode = 'w'
        if enable_append:
            mode = 'a'

        with open(filename, mode) as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_names)

            if write_header:
                csv_writer.writeheader()

            for item in data:
                csv_writer.writerow(item)

            f.close()
