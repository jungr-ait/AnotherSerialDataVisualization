import time
from SourceSink.SerialDataSource import SerialDataSource
from SourceSink.OrientationPlot import OrientationPlot
from SourceSink.VectorPlot3D import VectorPlot3D

if __name__ == '__main__':
    ser = SerialDataSource(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    plot = OrientationPlot(format_str='q_wxyz:%f,%f,%f,%f', title="BNO080 - game orientation vector")
    acc = VectorPlot3D(format_str='acc:%f,%f,%f', title='BNO080 - acceleration', max_samples=50, axis_length=1)
    ser.add_sink(plot)
    ser.add_sink(acc)
    ser.start()
    print('Lets visualize')
    while True:
        plot.plot_figure()
        acc.plot_figure()
        time.sleep(0.05)

    print('stop')
    ser.stop()