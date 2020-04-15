import csv
import os
from logger.DataFormatParser import DataFormatParser


class DataLogger(DataFormatParser):
    def __init__(self, filename, format_str="%f,%f,%f", header="", flush_data=False):
        super().__init__(format_str)
        self.filename = filename
        self.format_str = format_str
        self.flush_data = flush_data

        # https://stackabuse.com/reading-and-writing-csv-files-in-python/
        self.csv_file = open(filename, 'w')
        self.csv_writer = csv.writer(self.csv_file)

        if header != "":
            parts = header.split(',')
            self.csv_writer.writerow(parts)

    def __del__(self):
        self.stop()

    def stop(self):
        if not self.csv_file.closed:
            self.csv_file.close()

    def is_closed(self):
        return not self.csv_file.closed

    def write_to_file(self, arr):
        if not self.csv_file.closed:
            self.csv_writer.writerow(arr)
            if self.flush_data:
                self.csv_file.flush()
                os.fsync(self.csv_file.fileno())

    def append_data(self, arr):
        if len(arr) > 0:
            self.write_to_file(arr)