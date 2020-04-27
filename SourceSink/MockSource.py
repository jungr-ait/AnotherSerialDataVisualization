import time
import serial
import threaded_serial
import threading
import signal
import random
from SourceSink.IDataSource import IDataSource
from SourceSink.IDataSink import IDataSink
from SourceSink.ICyclic import ICyclic
from SourceSink.TSDataSource import TSDataSource


class MockSource(ICyclic, TSDataSource):
    def __init__(self, rate_ms = 500, format_str='%f,%f,%f',add_timestamp=False):
        ICyclic.__init__(self,rate_ms)
        TSDataSource.__init__(self)

        self.format_str = format_str
        self.add_timestamp = add_timestamp
        self.set_continue()
        self.init_timestamp = time.time()

    ## override from IDataSource and ICyclic
    def stop(self):
        self.do_run = False
        self.join()
        self.remove_all_sinks()

    ## ICyclic -- Interface
    def periodic_call(self):
        num_axis = self.format_str.count('%')
        line = ''
        if not self.add_timestamp:
            for i in range(0, num_axis):
                line = line + str('%f,'%random.random())
        else:
            timestamp = time.time()-self.init_timestamp
            line = str('%f,' % timestamp)
            for i in range(1, num_axis):
                line = line + str('%f,'%random.random())

        self.distribute_data(line)

if __name__ == '__main__':
    mock = MockSource(500, 'acc:')

    print('Let the Mock produce')
    mock.start()

    print('main thread rests a bit....')
    time.sleep(4)

    print('stop the Mock')
    mock.stop()