import scanf
from logger.IDataSink import  IDataSink


class DataFormatParser(IDataSink):
    def __init__(self, format_str="%f,%f,%f"):
        super().__init__()
        self.format_str = format_str

    def append_data(self, arr):
        print("append:" + str(arr))

    def parse_line(self, str):
        # https://pypi.org/project/scanf/
        arr = scanf.scanf(self.format_str, str)

        # https://stackoverflow.com/a/7816439
        if arr is not None:
            self.append_data(arr)

    ## IDataSink -- Interface:
    def sink(self, data):
        self.parse_line(str(data))

    def stop(self):
        print("stop handle")



if __name__ == '__main__':

    i = DataFormatParser(format_str='%d')

    i.sink('1')
    i.sink('2.23')
    i.sink('3')
    i.sink('foo')

    print("is instance of abstract basis class: " + str(isinstance(i, IDataSink)))

