from logger.DataPlotter import DataPlotter

class PlotterModel():
    plotter = None
    view = None

    def __init__(self, view):
        self.view = view

    def create(self, title, format_str, use_timestamp, legend, max_samples):
        self.plotter = DataPlotter(title=title,
                                   format_str=format_str,
                                   use_timestamp=use_timestamp,
                                   legend=legend,
                                   max_samples=max_samples)
        return self.plotter

    def close(self):
        del self.plotter
        self.plotter = None
        pass

    def get(self):
        return self.plotter

    def periodic_call(self):
        if self.plotter is not None:
            self.plotter.plot_figure()