import threading
from logger.IDataSource import IDataSource
from logger.IDataSink import IDataSink

class TSDataSource(IDataSource):
    data_sink_map = {}  # thread safe access to map ensured
    map_lock = None
    def __init__(self):
        IDataSource.__init__(self)
        self.map_lock = threading.Lock()

    ## IDataSource Interface
    def add_sink(self, sink):
        if isinstance(sink, IDataSink):
            with self.map_lock:
                self.data_sink_map[sink.ID] = sink
        else:
            print('-- TSDataSource: could not add sink (not a IDataSink!)')

    def remove_sink(self, sink):
        if isinstance(sink, IDataSink):
            with self.map_lock:
                del self.data_sink_map[sink.ID]
        elif isinstance(sink, int):
            with self.map_lock:
                del self.data_sink_map[sink]
        else:
            print('-- TSDataSource: could not remove sink (not a IDataSink!)')

    def remove_all_sinks(self):
        with self.map_lock:
            for key in self.data_sink_map:
                self.data_sink_map[key].stop()
            self.data_sink_map = {}

    def distribute_data(self, msg):
        print("TSDataSource.distribute_data():" + str(msg))

        with self.map_lock:
            for key in self.data_sink_map:
                self.data_sink_map[key].sink(msg)
