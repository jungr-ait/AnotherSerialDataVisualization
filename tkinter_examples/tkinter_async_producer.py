# classical producer consumer example
import tkinter as tk
import tkinter.ttk as ttk
import queue
import threading
import random
import time


class Producer(threading.Thread):
    cycle_period_ms  = 10  # periode [ms] of the run method
    do_run = True  # TODO: is do_run atomic? Or should it be locked?
    def __init__(self, data_queue, period_ms =  10):
        super().__init__(target=self.run)  # important: init Thread
        self.cycle_period_ms = period_ms
        self.data_queue = data_queue

    def __del__(self):
        if  self.do_run:
            self.stop()
        print('Producer is dying...')

    def run(self):
        while self.do_run:
            self.data_queue.put(random.random())
            time.sleep(self.cycle_period_ms / 1000.0)

    def stop(self):
        self.do_run = False  # does the rest...
        self.join()



class ConsumerGUI(tk.Tk):  # a tk.Toplevel
    producer = None  # we are a factory that produces producers :D
    periodic_rate_ms = 1000

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('MainGUI')
        self.root = self   # here is your root, when you are looking for it!


        self.content = ttk.Frame(self, padding=10)
        self.btn1 = ttk.Button(self, text='create consumer', command=self.on_btn1)
        self.btn1.pack()
        self.btn2 = ttk.Button(self, text='stop', command=self.on_btn2)
        self.btn2.pack()
        self.btn_quit = ttk.Button(self, text='quit', command=self.on_btn_quit)
        self.btn_quit.pack()
        # data field
        self.frame_DataView = ttk.Frame(self, padding=10, height=100 )
        self.lst_DataView = tk.Listbox(self.frame_DataView)
        self.scrl_DataView = ttk.Scrollbar(self.frame_DataView, orient=tk.VERTICAL, command=self.lst_DataView.yview)
        self.lst_DataView['yscrollcommand'] = self.scrl_DataView.set
        self.lst_DataView.insert('end', 'empty...')
        self.lst_DataView.size()
        self.lst_DataView_buffersize  = 50 # max buffersize in listbox.
        self.scrl_DataView.pack(side=tk.RIGHT, fill=tk.Y)
        self.lst_DataView.pack()
        self.frame_DataView.pack()

        self.producer_queue = queue.Queue(100)
        self.periodicCall()

    def __del__(self):
        print('kill object....')

    ## WIDGED callbacks:
    def on_btn1(self):
        print('btn1 pressed - create consumer')
        self.create_producer()

    def on_btn2(self):
        print('btn2 pressed - stop consumer')
        self.kill_producer()

    def on_btn_quit(self):
        print('quit')
        self.kill_producer()
        self.quit()

    ## PRODUCER:
    def create_producer(self):
        if self.producer is None:
            self.producer = Producer(self.producer_queue, 500)
            self.producer.start()
        else:
            print('--- producer already created!')

    def kill_producer(self):
        if self.producer is not None:
            self.producer.stop()
            del(self.producer)
        else:
            print('--- no producer to destroy!')

    ## PERIODIC CALLS:
    def periodicCall(self):
        # here: all polling activities should be places:
        self.poll_producer_queue()

        # call this method every N ms
        self.after(self.periodic_rate_ms, self.periodicCall)

    def poll_producer_queue(self):
        print('periodic call...')
        while self.producer_queue.qsize():
            msg = self.producer_queue.get(0)
            print('we got: ' + str(msg))
            self.add_line_to_lst_DataView(str(msg))

    def add_line_to_lst_DataView(self, line):
        print('add line to lst_DataView...')
        self.lst_DataView.insert('end', line)

        # truncate DataView list if too long:
        if self.lst_DataView.size() > self.lst_DataView_buffersize:
            self.lst_DataView.delete(0, int(self.lst_DataView_buffersize/10))
            print('delete items from lst_DataView...')


if __name__ == '__main__':
    app = ConsumerGUI()
    app.geometry('300x600')
    app.mainloop()



