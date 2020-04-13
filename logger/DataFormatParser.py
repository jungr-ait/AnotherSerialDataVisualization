import scanf

class DataFormatParser:
    def __init__(self, format_str="%f,%f,%f"):
        self.format_str = format_str

    def stop(self):
        print("stop handle")

    def append_data(self, arr):
        print("append:" + str(arr))

    def parse_line(self, str):
        # https://pypi.org/project/scanf/
        arr = scanf.scanf(self.format_str, str)

        # https://stackoverflow.com/a/7816439
        if arr is not None:
            self.append_data(arr)
