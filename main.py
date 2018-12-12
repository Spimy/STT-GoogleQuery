import tkinter as tk
from tkinter import *
import speech_recognition as sr
import webbrowser
import threading
import queue
import time

RECONGISER = sr.Recognizer()
URL = "https://www.google.com/search?q="
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300


class App(Tk):

    def __init__(self, *args,**kwargs):
        Tk.__init__(self, *args, **kwargs)

        x_coord = (self.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y_coord = (self.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        
        self.iconbitmap('icon.ico')
        self.configure(cursor='@arrow.cur')
        self.title('Speech to Text Google Query - by Spimy')
        self.geometry('{0}x{1}+{2}+{3}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, x_coord, y_coord))

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = Main(container, self)
        self.frames[Main] = frame
        frame.grid(row=0, column=0, sticky=NSEW)

        self.show_frame(Main)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.config(background='#030303')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text = Text(self)
        self.text.config(state='normal', background='#030303', foreground="#f1f1f1")
        
        self.text.insert(tk.INSERT, 'Click the "Record" Button to Start Recording a\nQuery for Google Search!')
        self.text.config(state='disabled', background='#030303', width=50, height=15)

        record = Button(self, text='Click To Record', font=('Consolas', 10),
                        relief=FLAT, bg='#07049e', fg='#f1f1f1', activebackground='#0400d3', 
                        activeforeground='#f1f1f1', height=3, command=self.threader)

        self.text.grid(row=0, column=0, sticky=NSEW)
        record.grid(row=1, column=0, sticky=NSEW)

    def record(self):

        self.text.config(state='normal', background='#030303', foreground="#f1f1f1")
        self.text.delete('1.0', END)
        self.text.insert(tk.INSERT, "Recording...")
        self.text.config(state='disabled', background='#030303', foreground="#f1f1f1")

        with sr.Microphone() as source:
            audio = RECONGISER.listen(source)

            try:
                text = RECONGISER.recognize_google(audio)
                keyword = text.replace(' ', '+')
                search = URL + keyword

                webbrowser.open(search, new=2)

                self.text.config(state='normal', background='#030303', foreground="#f1f1f1")
                self.text.delete('1.0', END)
                self.text.insert(tk.INSERT, text)
                self.text.config(state='disabled', background='#030303', foreground="#f1f1f1")
            except:
                self.text.config(state='normal', background='#030303', foreground="#f1f1f1")
                self.text.delete('1.0', END)
                self.text.insert(tk.INSERT, "Could not recognise voice...")
                self.text.config(state='disabled', background='#030303', foreground="#f1f1f1")
    
    def threader(self):
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.record)
        self.new_thread.start()
        self.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.thread_queue.get(0)
        except queue.Empty:
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        time.sleep(5)
        self.queue.put("Task finished")


def loadapp():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    loadapp()