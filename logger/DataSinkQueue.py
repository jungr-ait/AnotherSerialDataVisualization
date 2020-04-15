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

        # check if Queue is full: https://www.programcreek.com/python/example/2533/Queue.Full
        try:
            if self.data_queue.full():
                #print('DataSinkQueue is full! --> dropping oldest msg')
                self.data_queue.get()

            self.data_queue.put(data, timeout=0.001)
            #print('DataSinkQueue.sink: ' + str(data))

        except AttributeError:
            # self.pool is None.
            pass

        except queue.Full:
            # This should never happen if self.block == True
            print('DataSinkQueue is full!')

    def stop(self):
        print("stop handle")