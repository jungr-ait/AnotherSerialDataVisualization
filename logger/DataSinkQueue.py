import queue
from logger.IDataSink import  IDataSink


class DataSinkQueue(IDataSink):
    data_queue = None
    def __init__(self, len=100):
        super().__init__()

        self.data_queue =queue.Queue(len)

    def available(self):
        return self.data_queue.qsize() > 0

    ## IDataSink -- Interface:
    def sink(self, data):
        try:
            self.data_queue.put(data, timeout=0.001)
            print('DataSinkQueue.sink: ' + str(data))

        except AttributeError:
            # self.pool is None.
            pass

        except queue.Full:
            # This should never happen if self.block == True
            print('DataSinkQueue is full! --> dropping oldest msg')
            self.data_queue.get()
            self.sink(data)

    def stop(self):
        print("stop handle")