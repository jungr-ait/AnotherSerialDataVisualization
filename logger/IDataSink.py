from abc import ABC, abstractmethod

# https://www.python-course.eu/python3_abstract_classes.php
class IDataSink(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def sink(self, data):
        pass

    @abstractmethod
    def stop(self):
        pass


if __name__ == '__main__':
    try:
        i = IDataSink()
    except:
        print('you got an expected error...')
