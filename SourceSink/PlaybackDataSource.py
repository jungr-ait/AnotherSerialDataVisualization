import time
import csv
import os
import serial
import threaded_serial
import threading
import signal
import random
from SourceSink.IDataSource import IDataSource
from SourceSink.IDataSink import IDataSink
from SourceSink.ICyclic import ICyclic
from SourceSink.TSDataSource import TSDataSource
from SourceSink.DataPlotter import DataPlotter
from SourceSink.VectorPlot3D import VectorPlot3D
from SourceSink.OrientationPlot import OrientationPlot


class PlaybackDataSource(ICyclic, TSDataSource):
    def __init__(self, filename="", rate_ms = 500):
        ICyclic.__init__(self,rate_ms)
        TSDataSource.__init__(self)

        self.set_continue()
        self.file = open(filename, 'r')
        self.cur_line = 0

    ## override from IDataSource and ICyclic
    def stop(self):
        self.do_run = False
        self.join()
        self.remove_all_sinks()

    ## ICyclic -- Interface
    def periodic_call(self):
        line = self.file.readline()
        if line:
            self.distribute_data(line)
            self.cur_line = self.cur_line + 1
        else:
            self.do_run = False


if __name__ == '__main__':
    mock = PlaybackDataSource(rate_ms=10, filename="rec_orient.txt")

    plotter1 = DataPlotter(max_samples=1000, format_str="q_wxyz:%f,%f,%f,%f")
    plotter2 = DataPlotter(max_samples=1000, format_str="acc:%f,%f,%f")
    plotter3 = VectorPlot3D(format_str="acc:%f,%f,%f")
    plotter4 = OrientationPlot(format_str="q_wxyz:%f,%f,%f,%f")
    mock.add_sink(plotter1)
    mock.add_sink(plotter2)
    mock.add_sink(plotter3)
    mock.add_sink(plotter4)
    print('Lets play back')
    mock.start()
    while mock.do_run:
        #print('main thread rests a bit....')
        #time.sleep(0.1)
        #plotter1.plot_figure()
        #plotter2.plot_figure()
        #plotter3.plot_figure()
        plotter4.plot_figure()

    print('stop the Mock')
    mock.stop()