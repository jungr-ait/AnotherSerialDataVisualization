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
                 legend='', max_samples=200, axis_length=1.0):
        DataFormatParser.__init__(self, format_str=format_str)

        self.data_lock = threading.Lock()
        self.title = title
        self.legend = legend

        self.max_samples = int(max_samples)
        self.axis_length = max(0.01, axis_length)
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

        vec_mean = np.zeros(3)
        vec_curr = np.zeros(3)
        vec_std  = np.zeros(3)
        vec_arr  = np.zeros( (3, len(data[0])) )

        if len(data[0]) > 0:
            for i in range(0, self.num_axis):
                xs = np.array(data[i])
                array_length = len(xs)
                vec_arr[i] = xs
                vec_mean[i] = np.mean(xs)
                vec_curr[i] = xs[array_length - 1]
                vec_std[i] = np.std(xs)


        # statistics
        str1 = r'$\mu=$'
        str2 = '\n' + r'$\sigma=$'
        for i in range(0, self.num_axis):
            str1 = str1 + ('%.2f, ' % (vec_mean[i]))
            str2 = str2 + ('%.2f, ' % (vec_std[i]))

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        self.ax.text(0.95, 0.95, 0.95, s=str1 + str2, fontsize=14,
                     verticalalignment='top', bbox=props)

        plot_coordinate_reference_frame(self.ax, length=self.axis_length)
        plot_vec3d(self.ax, linewidth=2, start=(0, 0, 0), stop=vec_curr, color='black')
        plot_vec3d(self.ax, linewidth=2, start=(0, 0, 0), stop=vec_mean, color='grey')
        self.ax.scatter(vec_arr[0], vec_arr[1], vec_arr[2], marker='o')

        self.ax.grid()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.ax.set_aspect('equal')
        scaling = np.array([getattr(self.ax, 'get_{}lim'.format(dim))() for dim in 'xyz']);
        self.ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]] * 3)
        #self.ax.set_xlim3d(0, max(self.axis_length, self.ax.get_xlim3d()[1])*1.1)
        #self.ax.set_ylim3d(0, max(self.axis_length, self.ax.get_ylim3d()[1])*1.1)
        #self.ax.set_zlim3d(0, max(self.axis_length, self.ax.get_zlim3d()[1])*1.1)

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
    format_str= '%f,%f'
    mock = MockSource(rate_ms=100, format_str=format_str)
    plotter1 = VectorPlot3D(max_samples=50, format_str=format_str, axis_length=0.1)
    plotter2 = VectorPlot3D(max_samples=200, format_str='%f')

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
