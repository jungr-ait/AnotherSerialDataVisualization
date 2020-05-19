import time
import threading
from SourceSink.DataFormatParser import DataFormatParser
from SourceSink.MockSource import MockSource
import matplotlib.pyplot as plt
import numpy as np
from SourceSink.drawing_utils import *

class VectorPlot3D(DataFormatParser):
    t_vec = []
    data = []
    data_lock = None
    num_samples = 0
    def __init__(self, title="title", format_str="%f,%f,%f",
                 legend='', max_samples=200):
        DataFormatParser.__init__(self, format_str=format_str)

        self.data_lock = threading.Lock()
        self.title = title
        self.legend = legend

        self.max_samples = int(max_samples)

        self.num_axis = format_str.count('%')
        assert(self.num_axis < 4)
        self.clear_data()

        self.fig = plt.figure(figsize=(10, 5), dpi=50)
        self.fig.suptitle(title, fontsize=16)
        self.fig.set_label("over time")#
        self.ax = self.fig.add_subplot(111, projection='3d')
        #self.ax.set_aspect('equal')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

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
        with self.data_lock:
            data = self.data.copy()

        self.ax.clear()

        vec_mean = np.empty(self.num_axis)
        vec_curr = np.empty(self.num_axis)
        vec_std  = np.empty(self.num_axis)
        vec_arr  = np.empty( (3, len(data[0])) )
        for i in range(0, self.num_axis):
            xs = np.array(data[i])
            array_length = len(xs)
            vec_arr[i] = xs
            vec_mean[i] = np.mean(xs)
            vec_curr[i] = xs[array_length - 1];
            vec_std[i] = np.std(xs)

        plot_coordinate_reference_frame(self.ax)
        plot_vec3d(self.ax, linewidth=2, start=(0, 0, 0), stop=vec_curr, color='black')
        plot_vec3d(self.ax, linewidth=2, start=(0, 0, 0), stop=vec_mean, color='grey')
        self.ax.scatter(vec_arr[0], vec_arr[1], vec_arr[2], marker='o')

        self.ax.grid()
        #self.ax.legend(shadow=True, loc='upper left')
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.fig.tight_layout()

        textstr = '\n'.join((
            r'$\mu=%.2f$' % (vec_mean[0],),
            r'$\sigma=%.2f$' % (vec_std[0],)))
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        self.ax.text(0.95, 0.95, 0.95, s=textstr, fontsize=14,
                verticalalignment='top', bbox=props)
        plt.pause(1e-6) # The pause is needed because the GUI events happen while the main code is sleeping, including drawing

    # DataFormatParser - Interface
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
    format_str= '%f,%f,%f'
    mock = MockSource(rate_ms=100, format_str=format_str)
    plotter1 = VectorPlot3D(max_samples=50, format_str=format_str)
    plotter2 = VectorPlot3D(max_samples=50, format_str=format_str)

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
