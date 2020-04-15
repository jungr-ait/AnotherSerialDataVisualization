import time
import threading
from logger.DataFormatParser import DataFormatParser
from logger.MockSource import MockSource

class DataPlotter(DataFormatParser):
    t_vec = []
    data = []
    data_lock = None
    def __init__(self, title="", format_str="%f,%f,%f",
                 use_timestamp=False, legend="", update_interval_ms=100, max_samples=200):
        DataFormatParser.__init__(self, format_str=format_str)

        self.data_lock = threading.Lock()
        self.title = title
        self.legend = legend
        self.update_interval = update_interval_ms
        self.use_timestamp = use_timestamp  # specifies wheater first entry is timestamp
        self.max_samples = max_samples


        self.num_axis = format_str.count('%')
        if use_timestamp:
            self.num_axis = min(0, self.num_axis - 1)

        self.clear_data()


    def clear_data(self):
        with self.data_lock:
            self.data = []
            for i in range(0, self.num_axis):
                row = []
                self.data.append(row)

    def update(self):
        self.plot_figure()

    def plot_figure(self):
        if self.use_timestamp:
            t_arr = self.data[0];

        print("plot figure...")


    def append_data(self, arr):
        if len(arr) > 0:
            with self.data_lock:
                index = 0
                for val in arr:
                    self.data[index].append(val)
                    l = len(self.data[index])
                    if l > self.max_samples:
                        del self.data[index][1:10]

                    index = index + 1


    def stop(self):
        pass


if __name__ == '__main__':
    mock = MockSource(500, 'acc:')
    plotter = DataPlotter()

    mock.add_sink(plotter)
    print('Let the Mock produce')
    mock.start()

    for i in range(1,10):
        print('main thread rests a bit....')
        time.sleep(2)
        plotter.plot_figure()


    print('stop the Mock')
    mock.stop()
