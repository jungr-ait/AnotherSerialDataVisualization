from logger.DataLogger import DataLogger


class LoggerModel():
    logger = None
    view = None
    def __init__(self, view):
        self.view = view

    def create_logger(self, filename, format_str, header, flush_data):
        self.logger = DataLogger(filename=filename, format_str=format_str,
                                 header=header,flush_data=flush_data);
        return self.logger

    def close_logger(self):
        self.logger.stop()

    def get_logger(self):
        return self.logger