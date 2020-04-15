import time
import threading
from logger.DataFormatParser import DataFormatParser
from logger.MockSource import MockSource
import matplotlib.pyplot as plt


class DataPlotter(DataFormatParser):
    t_vec = []
    data = []
    data_lock = None
    num_samples = 0
    def __init__(self, title="title", format_str="%f,%f,%f",
                 use_timestamp=False, legend='', max_samples=200):
        DataFormatParser.__init__(self, format_str=format_str)

        self.data_lock = threading.Lock()
        self.title = title
        self.legend = legend

        self.use_timestamp = use_timestamp  # specifies wheater first entry is timestamp
        self.max_samples = int(max_samples)


        self.num_axis = format_str.count('%')

        self.clear_data()


        self.fig = plt.figure(figsize=(10, 5), dpi=50)
        self.fig.suptitle(title, fontsize=16)
        self.fig.set_label("over time")#
        self.ax = self.fig.add_subplot(111)

    def __del__(self):
        plt.close(self.fig)

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
        with self.data_lock:
            data = self.data.copy()

        self.ax.clear()
        if not self.use_timestamp:
            for i in range(0, self.num_axis):
                xs = data[i]
                ts = list(range(self.num_samples-len(xs), self.num_samples))
                self.ax.plot(ts, xs, label="x"+str(i))

        else:
            for i in range(1, self.num_axis):
                xs = data[i]
                ts = data[0]
                ts.sort()
                self.ax.plot(ts, xs, label="x"+str(i))
                self.ax.set_xlabel('t')

        self.ax.grid()
        self.ax.legend(shadow=True, loc='upper left')
        #self.fig.tight_layout()
        plt.pause(1e-6) # The pause is needed because the GUI events happen while the main code is sleeping, including drawing


    def append_data(self, arr):
        if len(arr) > 0:
            self.num_samples += 1
            with self.data_lock:
                index = 0
                for val in arr:
                    self.data[index].append(val)
                    l = len(self.data[index])
                    if l > self.max_samples:
                        del self.data[index][0] #:round(self.max_samples/4)]

                    index = index + 1


    def stop(self):
        pass


if __name__ == '__main__':
    use_timestamp = True
    format_str= '%f,%f,%f,%f,%f'
    mock = MockSource(rate_ms=100, format_str=format_str, add_timestamp=use_timestamp)
    plotter1 = DataPlotter(max_samples=50, format_str=format_str, use_timestamp=use_timestamp)

    plotter2 = DataPlotter(max_samples=50, format_str=format_str, use_timestamp=use_timestamp)

    mock.add_sink(plotter1)
    mock.add_sink(plotter2)
    print('Let the Mock produce')
    mock.start()

    for i in range(0,20):
        print('main thread rests a bit....')
        time.sleep(1)
        plotter1.plot_figure()
        time.sleep(1)
        plotter2.plot_figure()


    print('stop the Mock')
    mock.stop()
