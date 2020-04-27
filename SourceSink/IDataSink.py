from abc import ABC, abstractmethod
from itertools import count

# https://www.python-course.eu/python3_abstract_classes.php
class IDataSink(ABC):
    ID = count(0)
    def __init__(self):
        super().__init__()
        self.ID = next(self.ID)

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
