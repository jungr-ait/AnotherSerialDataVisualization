from logger import DataFormatParser


class DataPlotter(DataFormatParser):
    t_vec = []
    data = []

    def __init__(self, title, format_str="%f,%f,%f", use_timestamp=False, legend="", update_interval_ms=100,
                 max_samples=200):
        super().__init__(format_str=format_str)
        self.title = title
        self.legend = legend
        self.update_interval = update_interval_ms
        self.use_timestamp = use_timestamp  # specifies wheater first entry is timestamp
        self.max_samples = max_samples;


        self.num_axis = format_str.count('%')
        if use_timestamp:
            self.num_axis = min(0, self.num_axis - 1)


    def clear_data(self):
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


    def append_data(self, arr):
        if len(arr) > 0:
            index = 0
            for val in arr:
                self.data[index].append(val)
                l = len(self.data[index])
                if l > self.max_samples:
                    del self.data[index][1:10]

                index = index + 1