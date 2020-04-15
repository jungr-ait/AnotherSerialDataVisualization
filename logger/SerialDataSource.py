import time
import serial
import threaded_serial
import threading
import signal
from logger.DataLogger import DataLogger
from logger.IDataSink import IDataSink
from logger.DataSinkQueue import DataSinkQueue
from logger.TSDataSource import TSDataSource



class SerialDataSource(TSDataSource):
    def __init__(self, port, baud_rate, timeout):
        super().__init__()
        # https://stackoverflow.com/a/46810180
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())
        self.terminated = False
        self.serial = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout)
        self.threaded = threaded_serial.ThreadedSerialManager(connection=self.serial, callback=self.data_received)


    def _signal_handler(self):
        self.terminated = True

    def data_received(self, byte_arr):
        # decode bytes object to produce a string: https://stackoverflow.com/a/606199
        line = byte_arr.decode("ascii")
        line = line.replace('\r\n', '')
        self.distribute_data(line)

    def start(self):
        self.threaded.start()

    def stop(self):
        self.threaded.stop()
        self.remove_all_sinks()





if __name__ == '__main__':
    ser = SerialDataSource(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    log1 = DataLogger('acc.csv', 'acc:%f,%f,%f,', 'acc.x,acc.y,acc.z', flush_data=False)
    print('ID of log1 ' + str(log1.ID));
    log2 = DataLogger('acc.csv', 'acc:%f,%f,%f,', 'acc.x,acc.y,acc.z', flush_data=False)
    print('ID of log2 ' + str(log2.ID));
    ser.add_sink(log1)
    ser.add_sink(DataLogger('gyr.csv', 'gyr:%f,%f,%f,', 'gyr.x,gyr.y,gyr.z', flush_data=False))
    ser.add_sink(DataSinkQueue(len=100))

    ser.start()
    time.sleep(4)
    print("stop sink log1")
    log1.stop()
    time.sleep(2)
    print("remove a sink")
    ser.remove_sink(log1)
    ser.remove_sink(int(2))
    ser.stop()


    print("terminated")

    exit(0)