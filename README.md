# SerialDataVisualization

(Another) tool to display data steam over a serial interface. 


## Install

### TK

[Ubuntu and Python 3](https://tkdocs.com/tutorial/install.html): `sudo apt-get install python3-tk`


## Tutorials:

- [tkDocs - grid](https://tkdocs.com/tutorial/grid.html)
- [Model View Controller using Tkinter ](https://gist.github.com/ReddyKilowatt/5d0bfedbe9a92a8f50cd948ab51683ee)
- [as]()
- [as]()


## Basic concepts

Serial visualization is maintained from a `MainWindow` (root, toplevel window).
There, a `tk.menubar` is show, allowing to save and load a `SerialConfig`.
In the `MainWindow`, a `tk.Frame` to select a port, baudrate and to connect/disconnect via a toggling button is shown.
In another frame below a `tkk.Entry` as a text-field is shown, allowing to specify a string to be parsed, with a `ttk.Button` to create a `DataLogger` and to create a `DataPlotter`.
To create a `DataLogger` the user will be prompted to specify a csv-file to dump the data to.
Each `DataPlotter` will be created in a new `tk.Toplevel(MainWindow)` to display a matplotlib graph.
In the `DataPlotter`, two widgets are shown, one to specify the max number of samples and a canvas blow to show the graph


 Dta
