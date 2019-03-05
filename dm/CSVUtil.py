import csv
import logging


class CSVUtil:
    @staticmethod
    def create_csv_file(data: list, filename: str):
        if data == []:
            logging.warning('empty data to write')
            return

        field_names = []
        for key, _ in data[0].items():
            field_names.append(key)

        with open(filename, 'w') as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_names)

            csv_writer.writeheader()
            for item in data:
                csv_writer.writerow(item)
