# SerialDataVisualization

(Another) tool to display data steam over a serial interface. 


## Install

### TK

[Ubuntu and Python 3](https://tkdocs.com/tutorial/install.html): `sudo apt-get install python3-tk`


## Tutorials:

- [tkDocs - grid](https://tkdocs.com/tutorial/grid.html)
- [Model View Controller using Tkinter ](https://gist.github.com/ReddyKilowatt/5d0bfedbe9a92a8f50cd948ab51683ee)


## Basic concepts

Serial visualization is maintained from a `MainWindow` (root, toplevel window).
There, a `tk.menubar` is show, allowing to save and load a `SerialConfig`.
In the `MainWindow`, a `tk.Frame` to select a port, baudrate and to connect/disconnect via a toggling button is shown.
In another frame below a `tkk.Entry` as a text-field is shown, allowing to specify a string to be parsed, with a `ttk.Button` to create a `DataLogger` and to create a `DataPlotter`.
To create a `DataLogger` the user will be prompted to specify a csv-file to dump the data to.
Each `DataPlotter` will be created in a new `tk.Toplevel(MainWindow)` to display a matplotlib graph.
In the `DataPlotter`, two widgets are shown, one to specify the max number of samples and a canvas blow to show the graph


 
 ### PlotterWindow
 
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
