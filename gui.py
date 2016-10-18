import tkinter as gui
import tkinter.ttk as gui_plus
import threading
import time

# This is fine for a single background thread, but a semaphore would be better
KILL_THREAD = False

class MainApp:    
    def __init__(self, config, games, memshark):
        self.root = gui.Tk()
        self.root.geometry('{}x{}'.format(800, 600))
        self.mainWindow = MainWindow(self.root, config, games, memshark)
    
    def start(self):
        self.root.mainloop()

class MainWindow:    
    def __init__(self, master, config, games, memshark):
        self.master = master
        self.config = config
        self.games = games
        self.memshark = memshark

        self.poke_thread = None
        self.game_actions_frame = None
        master.title("Memshark")

        self.label = gui.Label(master, text="Wii U IP Address: {}".format(config.wii_u_ip))    
        self.label.grid()    
        
        self.connection_status_label = gui.Label(master, text='Connection Status: [disconnected]')
        self.connect_button = gui.Button(master, text="Connect", command = self.connect)
        self.disconnect_button = gui.Button(master, text="Disconnect", command = self.disconnect)
        self.connection_status_label.grid()
        self.connect_button.grid()
        self.disconnect_button.grid()

        self.close_button = gui.Button(master, text="Close", command=master.quit)
        
        self.game_options = [x.name for x in games.games]
        self.game_selected = gui.StringVar()        
        self.game_selected.trace('w', self.change_game_selection)
        self.game_list = gui.OptionMenu(master, self.game_selected, *self.game_options)
        self.game_list.config(width=50)
        # Calling this before the app is drawn causes it to crash
        # self.game_selected.set(self.game_options[0])
        self.game_list.grid()

        self.game_version = gui.Label(master, text='')
        self.game_version.grid()

    def connect(self):
        self.memshark.connect()
        self.connection_status_label.config(text='Connected')

    def disconnect(self):
        self.memshark.disconnect()
        self.connection_status_label.config(text='Disconnected')

    def change_game_selection(self, name, index, mode):
        if self.game_actions_frame != None:
            self.game_actions_frame.destroy()
        self.game_actions_frame = gui.Frame(self.master)
        game_name = self.game_selected.get()
        game = self.games.game_lookup[game_name]
        self.game_version.config(text='Game Version: {}'.format(game.version))                
        self.game_pokes = [(
            'Name',
            'Address',
            'Value',
            'Poke',
            'Frozen'
        )]
        self.poke_table = SimpleTable(self.game_actions_frame)
        for poke in game.memory_pokes:
            name_label = gui.Label(self.poke_table, text=poke.name)
            address_label = gui.Label(self.poke_table, text=poke.address)
            value_label = gui.Label(self.poke_table, text=poke.value)
            poke_button = gui.Button(self.poke_table, text='Poke', command = lambda poke=poke: self.poke(poke))
            freeze = gui.IntVar()
            freeze.trace('w', self.change_frozen_values)
            freezeCheck = gui.Checkbutton(self.poke_table, variable=freeze)            
            self.game_pokes.append((name_label,address_label,value_label,poke_button,freezeCheck, freeze, poke))
        self.poke_table.set_rows(self.game_pokes)
        # Kill any frozen values for the previous selection
        self.change_frozen_values(None, None, None)
        self.poke_table.grid()
        self.game_actions_frame.grid()

    def poke(self, poke):
        print("--DEBUG Poking {}: {} -> {}".format(poke.name, poke.address, poke.value))
        self.memshark.poke(poke.address, poke.value)

    def change_frozen_values(self, name, index, mode):
        global KILL_THREAD
        pokes = []
        freeze_var_position = 5
        for tup in self.game_pokes:
            if len(tup) > freeze_var_position:
                if tup[freeze_var_position].get() == 1:
                    pokes.append(tup[len(tup)-1])
        if self.poke_thread != None:
            KILL_THREAD=True
            self.poke_thread.join()
        if len(pokes) > 0:
            KILL_THREAD=False
            self.poke_thread = threading.Thread(target=freeze_pokes, args=(pokes, self.config.freeze_poke_interval_seconds, self.memshark))
            self.poke_thread.start()

def freeze_pokes(pokes, interval_seconds, memshark):
    global KILL_THREAD
    while True and not KILL_THREAD:
        for poke in pokes:
            print("--DEBUG Poking {}: {} -> {}".format(poke.name, poke.address, poke.value))
            memshark.poke(poke.address, poke.value)
        time.sleep(interval_seconds)

# http://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter
class SimpleTable(gui.Frame):
    def __init__(self, parent):
        # use black background so it "peeks through" to 
        # form grid lines
        gui.Frame.__init__(self, parent, background="black")    
    
    def set_rows(self, rows):
        non_widget_col = 5
        self._widgets = []
        ii = 0
        jj = 0
        for row in rows:
            current_row = []
            for column in row:                
                if jj < non_widget_col:
                    if ii > 0:
                        column.config(borderwidth=0)
                        column.grid(row=ii, column=jj, sticky="nsew", padx=1, pady=1)
                        current_row.append(column)
                    else:
                        label = gui.Label(self, text=column, borderwidth=0, width=10)
                        label.grid(row=ii, column=jj, sticky="nsew", padx=1, pady=1)
                        current_row.append(column)
                jj += 1
            jj = 0
            ii += 1
            self._widgets.append(current_row)

        for column in range(0,non_widget_col):
            self.grid_columnconfigure(column, weight=1)        


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)