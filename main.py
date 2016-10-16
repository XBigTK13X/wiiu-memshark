import tkinter as gui
from memshark import Memshark

class MemsharkUiMain:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = gui.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = gui.Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = gui.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

root = gui.Tk()
my_gui = MemsharkUiMain(root)
root.mainloop()