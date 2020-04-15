from abc import ABC, abstractmethod
from itertools import count

# https://www.python-course.eu/python3_abstract_classes.php
class IDataSource(ABC):
    ID = count(0)
    def __init__(self):
        super().__init__()
        self.ID = next(self.ID)

    @abstractmethod
    def add_sink(self, sink):
        pass

    @abstractmethod
    def remove_sink(self, sink):
        pass

    @abstractmethod
    def remove_all_sinks(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass