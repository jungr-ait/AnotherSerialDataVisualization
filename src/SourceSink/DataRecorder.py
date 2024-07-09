import csv
import os
import time
from SourceSink.IDataSink import IDataSink
from SourceSink.SerialDataSource import SerialDataSource

class DataRecorder(IDataSink):
    def __init__(self, filename, header="", flush_data=False):
        super().__init__()
        self.filename = filename
        self.flush_data = flush_data

        # https://stackabuse.com/reading-and-writing-csv-files-in-python/
        self.file = open(filename, 'w')

        if header != "":
            self.file.write(header + '\n')

    def __del__(self):
        self.stop()

    def stop(self):
        if not self.file.closed:
            self.file.close()

    def is_closed(self):
        return not self.file.closed

    def write_to_file(self, arr):
        if not self.file.closed:
            self.file.writelines(arr + '\n')
            if self.flush_data:
                self.file.flush()
                os.fsync(self.file.fileno())

    ## IDataSink -- Interface:
    def sink(self, data):
        if len(data) > 0:
            self.write_to_file(data)


if __name__ == '__main__':
    ser = SerialDataSource(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    rec = DataRecorder(filename="rec_orient.txt", header='recording session')
    ser.add_sink(rec)


    print('Lets record data')
    ser.start()
    time.sleep(10)

    print('main thread rests a bit....')
    time.sleep(10)

    print("remove a sink")
    ser.remove_sink(rec)
    ser.stop()


    print("terminated")

    exit(0)