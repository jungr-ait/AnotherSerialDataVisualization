from abc import ABC, abstractmethod
import time
import threading

# https://www.python-course.eu/python3_abstract_classes.php
class ICyclic(threading.Thread, ABC):
    do_run = True
    do_continue = False
    def __init__(self, period_ms = 1000):
        self.period_ms = period_ms
        threading.Thread.__init__(self, target=self.run)
        ABC.__init__(self)

    def __del__(self):
        if  self.do_run:
            self.stop()

    @abstractmethod
    def periodic_call(self):
        pass


    def run(self):
        while self.do_run:

            if self.do_continue:
                self.periodic_call()
            time.sleep(self.period_ms / 1000)

    def set_continue(self, val=True):
        self.do_continue = val


    def stop(self):
        self.do_run = False
        self.join()



class TestICyclic(ICyclic):
    def __init__(self):
        super().__init__(500)
        self.start()

    ## ICyclic - abstract method
    def periodic_call(self):
        print('periodic_call - being called!')



if __name__ == '__main__':
    i = TestICyclic()

    print('main thread - rest a bit...')
    i.set_continue()
    time.sleep(5)

    print('cyclic should also stop working!')
    i.set_continue(False)
    time.sleep(2)
    print('main thread - time to proceed...')

    print('main thread - stop cyclic..')
    i.stop()

    time.sleep(0.5)

