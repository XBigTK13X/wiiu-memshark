import tkinter as tk

class TcpGeckoFrame():
    def __init__(self, master, memshark):
        self.master = tk.Frame(master)
        self.memshark = memshark

        self.connection_status_label = tk.Label(self.master, text='Connection Status: [disconnected]')
        self.connect_button = tk.Button(self.master, text="Connect to TCPGecko", command=self.connect)
        self.disconnect_button = tk.Button(self.master, text="Disconnect from TCPGecko", command=self.disconnect)
        self.connection_status_label.grid()
        self.connect_button.grid()
        self.disconnect_button.grid()    

    def connect(self):
        self.memshark.connect()
        self.connection_status_label.config(text='Connected')

    def disconnect(self):
        self.memshark.disconnect()
        self.connection_status_label.config(text='Disconnected')