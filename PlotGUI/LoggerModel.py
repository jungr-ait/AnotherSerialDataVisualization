from logger.DataLogger import DataLogger


class LoggerModel():
    logger = None
    view = None
    def __init__(self, view):
        self.view = view

    def create(self, filename, format_str, header, flush_data):
        self.logger = DataLogger(filename=filename, format_str=format_str,
                                 header=header,flush_data=flush_data);
        return self.logger

    def close(self):
        if self.logger is not None:
            self.logger.stop()

    def get(self):
        return self.logger