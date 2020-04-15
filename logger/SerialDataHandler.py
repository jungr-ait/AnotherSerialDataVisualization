import time
import serial
import threaded_serial
import threading
import signal
from logger.DataLogger import DataLogger
from logger.IDataSink import IDataSink
from logger.DataSinkQueue import DataSinkQueue

class SerialDataHandler:
    data_sink_map = {}  # thread safe access to map ensured
    map_lock = None
    def __init__(self, port, baud_rate, timeout):

        # https://stackoverflow.com/a/46810180
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())
        self.terminated = False

        self.map_lock = threading.Lock()
        self.serial = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout)
        self.threaded = threaded_serial.ThreadedSerialManager(connection=self.serial, callback=self.data_received)

    def add_sink(self, sink):
        if isinstance(sink, IDataSink):
            with self.map_lock:
                self.data_sink_map[sink.ID] = sink
        else:
            print('-- SerialDataHandler: could not add sink (not a IDataSink!)')

    def remove_sink(self, sink):
        if isinstance(sink, IDataSink):
            with self.map_lock:
                del self.data_sink_map[sink.ID]
        elif isinstance(sink, int):
            with self.map_lock:
                del self.data_sink_map[sink]
        else:
            print('-- SerialDataHandler: could not remove sink (not a IDataSink!)')

    def remove_all_sinks(self):
        with self.map_lock:
            for key in self.data_sink_map:
                self.data_sink_map[key].stop()
            self.data_sink_map = {}

    def _signal_handler(self):
        self.terminated = True

    def data_received(self, byte_arr):

        print("data received:" + str(byte_arr))

        # decode bytes object to produce a string: https://stackoverflow.com/a/606199
        line = byte_arr.decode("ascii")
        line = line.replace('\r\n', '')

        with self.map_lock:
            for key in self.data_sink_map:
                self.data_sink_map[key].sink(line)


    def start(self):
        self.threaded.start()

    def stop(self):
        self.threaded.stop()
        self.remove_all_sinks()





if __name__ == '__main__':
    ser = SerialDataHandler(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    log1 = DataLogger('acc.csv', 'acc:%f,%f,%f,', 'acc.x,acc.y,acc.z', flush_data=False)
    print('ID of log1 ' + str(log1.ID));
    log2 = DataLogger('acc.csv', 'acc:%f,%f,%f,', 'acc.x,acc.y,acc.z', flush_data=False)
    print('ID of log2 ' + str(log2.ID));
    ser.add_sink(log1)
    ser.add_sink(DataLogger('gyr.csv', 'gyr:%f,%f,%f,', 'gyr.x,gyr.y,gyr.z', flush_data=False))
    ser.add_sink(DataSinkQueue(len=100))

    ser.start()
    time.sleep(4)
    print("remove a sink")
    ser.remove_sink(log1)
    ser.remove_sink(int(2))

    #ser.add_datalogger(
    #    DataPlotter(title='gyroscope', format_str='gyr:%f,%f,%f,', use_timestamp=False, legend='gyr.x,gyr.y,gyr.z',
    #                update_interval_ms=500, max_samples=50))
    ser.stop()


    print("terminated")

    exit(0)