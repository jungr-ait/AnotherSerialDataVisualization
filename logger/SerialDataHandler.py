import time
import serial
import threaded_serial
import signal
from logger.DataLogger import DataLogger
from logger.IDataSink import IDataSink
from logger.DataSinkQueue import DataSinkQueue

class SerialDataHandler:
    data_sink_vec = []

    def __init__(self, port, baud_rate, timeout):

        # https://stackoverflow.com/a/46810180
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())
        self.terminated = False


        self.serial = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout)
        self.threaded = threaded_serial.ThreadedSerialManager(connection=self.serial, callback=self.data_received)

    def add_datalogger(self, sink):
        if isinstance(sink, IDataSink):
            self.data_sink_vec.append(sink)
        else:
            print('-- SerialDataHandler: could not add logger (not a IDataSink!)')

    def _signal_handler(self):
        self.terminated = True

    def data_received(self, byte_arr):

        print("data received:" + str(byte_arr))

        # decode bytes object to produce a string: https://stackoverflow.com/a/606199
        line = byte_arr.decode("ascii")
        line = line.replace('\r\n', '')

        for logger in self.data_sink_vec:
            logger.sink(line)

    def stop(self):
        self.terminated = True

    def run(self):

        print('terminate program using ctrl+c');
        self.threaded.start()
        while not self.terminated:
            # loop until terminated
            time.sleep(1)

        self.threaded.stop()
        for logger in self.data_sink_vec:
            logger.stop()




if __name__ == '__main__':
    ser = SerialDataHandler(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    log1 = DataLogger('acc.csv', 'acc:%f,%f,%f,', 'acc.x,acc.y,acc.z', flush_data=False)
    ser.add_datalogger(log1)
    ser.add_datalogger(DataLogger('gyr.csv', 'gyr:%f,%f,%f,', 'gyr.x,gyr.y,gyr.z', flush_data=False))
    ser.add_datalogger(DataSinkQueue(len=100))
    #ser.add_datalogger(
    #    DataPlotter(title='gyroscope', format_str='gyr:%f,%f,%f,', use_timestamp=False, legend='gyr.x,gyr.y,gyr.z',
    #                update_interval_ms=500, max_samples=50))
    ser.run()
    print("terminated")

    exit(0)