# (Another)SerialDataVisualization

(Another)SerialDataVisualization is a  tool to plot and save data steamed over a serial interface. 
But what is the difference to existing ones? Well, the primary goal was flexibility without being forced to change major 
parts of the code in order to get it working with your custom problem. 

Most solutions struggle when the data is not streamed as excatly three column separated values. 
- What if your device is sending data from different senors, e.g. in my case an accelerometer and gyroscope? 
- How to differentiate between those values in the data stream?
- What happens if on value is a timestamp?

A generic solution is to parse a **C** like [scanf](http://www.cplusplus.com/reference/cstdio/scanf/?kw=scanf) format string, e.g. `acc:%f,%f,%f` or `timestamp=%d,triple:%f;%f;%f`.
Each data logger or data plotter instance will be provided by a **format string** (Format) and process the received data if it matches the 
specified format.
 

## Requirements

[TK - Ubuntu and Python 3](https://tkdocs.com/tutorial/install.html): `sudo apt-get install python3-tk`

 
 ## SerialCOMViewer
 
![SerialCOMViewer](doc/SerialCOMViewer.png "SerialCOMViewer")


Open a detected serial configuration with some predefined baud rate (can be modified, just change a value).
Once it is opened successfully, you should see data arriving in the `RxDataView` where you can `Pause`, `Continue` and `Clear` the 
preview.
In the `LoggerConfig` you can create any number of `PlotterWindow` or `LoggerWindow`. 
Once everything is set up, you can save the current configuration in `File->Save as` as `*.ini` file to be loaded the next 
time. 

 
 ## PlotterWindow
 
 ![PlotterWindow](doc/PlotterWindow.png "PlotterWindow")
 
 Create a dynamic figure using matplot lib. 
 Data for the plot is received from a IDataSource (e.g. a SerialDataSource).
 Specify a format_str how each line received from the IDataSource should be interpreted.
 It is C++ <scanf> like: %f for float, %d for integer. Example: <mag:%f,%f,%f> would expect
 a line containing <mag> followed by three comma separated float values. It it fits it will be added
 to the buffer in the IDataSink, which is our DataPlotter, creating the figure.
 
- format_str: scanf string to parsed
- usetimestamp: specifies if the first element in <format_str> is a timestamp (x-axis)
- title: title of the figure
- legend: how the axis should be labeled
- max_sample: reduces the number of samples in the figure, dropping oldest ones
- pause/resume: pauses/resumes the refreshing of the plot - time to save figures!
- create/close: creates a new or destroys a plot.

## LoggerWindow

![LoggerWindow](doc/LoggerWindow.png "LoggerWindow")
 
Store the content received from a IDataSource in a CSV file.

The <data/msg/line> is received from a IDataSource(e.g. a SerialDataSource).
Specify a format_str how each line received from the
IDataSource should be interpreted. It is C <scanf> like:
%f for float, %d for integer. Example: <mag:%f,%f,%f> would expect
a line containing <mag> followed by three comma separated
float values. It it fits it will be added to the buffer in the IDataSink,
which is our DataLogger, writing lines in a specified file.
Options:
+ format_str: <scanf> string to parsed
+ header: header of the file: e.g. <x,y,z>
+ filename: name of the desired csv <file>
+ create/close: creates a new or destroys a file.
+ flush: refreshes file on drive (slower)


