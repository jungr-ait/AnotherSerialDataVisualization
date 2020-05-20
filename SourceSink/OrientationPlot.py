import time
import threading
from SourceSink.DataFormatParser import DataFormatParser
from SourceSink.MockSource import MockSource
import matplotlib.pyplot as plt
import numpy as np
from SourceSink.drawing_utils import *

class OrientationPlot(DataFormatParser):
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
        assert(self.num_axis < 10)
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

        R = np.eye(3)
        if len(data[0]) > 0:
            if self.num_axis < 4:
                vec_mean = np.zeros(3)
                vec_curr = np.zeros(3)
                vec_std = np.zeros(3)
                vec_arr = np.zeros((3, len(data[0])))
                for i in range(0, self.num_axis):
                    xs = np.array(data[i])
                    array_length = len(xs)
                    vec_arr[i] = xs
                    vec_mean[i] = np.mean(xs)
                    vec_curr[i] = xs[array_length - 1]
                    vec_std[i] = np.std(xs)

                R = matrix_from_euler_xyz(vec_mean)
            if self.num_axis == 4:
                q = np.zeros(4)
                for i in range(0, self.num_axis):
                    q[i] = data[i][len(data[i])-1]


                R = matrix_from_quaternion(q)
            if self.num_axis == 9:
                v_R = np.zeros(9)
                for i in range(0, self.num_axis):
                    v_R[i] = data[i][len(data[i])-1]
                R = v_R.reshape((3,3))
        self.ax.clear()




        plot_coordinate_reference_frame(self.ax, length=self.axis_length/10)
        plot_coordinate_reference_frame(self.ax, length=self.axis_length, R=R)


        self.ax.grid()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

        self.ax.set_xlim3d(-1.1*self.axis_length, 1.1*self.axis_length)
        self.ax.set_ylim3d(-1.1*self.axis_length, 1.1*self.axis_length)
        self.ax.set_zlim3d(-1.1*self.axis_length, 1.1*self.axis_length)

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
    format_str= '%f,%f%f'
    mock = MockSource(rate_ms=100, format_str=format_str)
    plotter1 = OrientationPlot(max_samples=50, format_str=format_str, axis_length=0.1)
    plotter2 = OrientationPlot(max_samples=200, format_str='%f')
    plotter3 = OrientationPlot(max_samples=200, format_str='%f,%f')
    mock.add_sink(plotter1)
    mock.add_sink(plotter2)
    mock.add_sink(plotter3)
    print('Let the Mock produce')
    mock.start()

    for i in range(0,20):
        print('main thread rests a bit....')
        time.sleep(1)
        plotter1.plot_figure()
        time.sleep(1)
        plotter2.plot_figure()
        plotter3.plot_figure()

    print('stop the Mock')
    mock.stop()
