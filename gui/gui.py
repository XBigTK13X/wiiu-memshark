import tkinter as tk
import tkinter.ttk as ttk

from gui import exploit_server_frame
from gui import tcp_gecko_frame
from gui import game_actions_frame

class MainApp:

    def __init__(self, config, games, memshark, exploit_server):
        self.root = tk.Tk()
        self.mainWindow = MainWindow(self.root, config, games, memshark, exploit_server)

    def start(self):
        self.root.mainloop()


class MainWindow:

    def __init__(self, master, config, games, memshark, exploit_server):
        self.master = master
        
        
        self.master.title("Memshark")

        self.container = tk.Frame(self.master)
        self.container.grid(padx=(20,20), pady=(20,20))

        self.label = tk.Label(self.container, text="Wii U IP Address: {}".format(config.wii_u_ip))

        self.notebook = ttk.Notebook(self.container)
        self.server_frame = exploit_server_frame.ExploitServerFrame(self.notebook, exploit_server)
        self.tcp_gecko_frame = tcp_gecko_frame.TcpGeckoFrame(self.notebook, memshark)
        self.game_actions_frame = game_actions_frame.GameActionsFrame(self.notebook, games, memshark, config)
        self.notebook.add(self.server_frame.master, text='Exploit Server', padding=[10,10])
        self.notebook.add(self.tcp_gecko_frame.master, text='PyGecko', padding=[10,10])
        self.notebook.add(self.game_actions_frame.master, text='Game Actions', padding=[10,10])           
        self.notebook.grid()
