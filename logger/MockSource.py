import time
import serial
import threaded_serial
import threading
import signal
import random
from logger.IDataSource import IDataSource
from logger.IDataSink import IDataSink
from logger.ICyclic import ICyclic
from logger.TSDataSource import TSDataSource


class MockSource(ICyclic, TSDataSource):
    data_sink_map = {}  # thread safe access to map ensured
    map_lock = None
    def __init__(self, rate_ms = 500, prefix=''):
        ICyclic.__init__(self,rate_ms)
        TSDataSource.__init__(self)
        self.map_lock = threading.Lock()

        self.prefix = prefix

    ## override from IDataSource and ICyclic
    def stop(self):
        self.do_run = False
        self.join()
        self.remove_all_sinks()

    ## ICyclic -- Interface
    def periodic_call(self):
        line = self.prefix + str('%f,%f,%f' % (random.random(), random.random(), random.random()))

        self.distribute_data(line)

if __name__ == '__main__':
    mock = MockSource(500, 'acc:')

    print('Let the Mock produce')
    mock.start()
    mock.set_continue()


    print('main thread rests a bit....')
    time.sleep(4)

    print('stop the Mock')
    mock.stop()