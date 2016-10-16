import tkinter as gui
import tkinter.ttk as gui_plus
import threading
import time

# This is fine for a single background thread, but a semaphore would be better
KILL_THREAD = False

class MainApp:    
    def __init__(self, config, games):
        self.root = gui.Tk()
        self.root.geometry('{}x{}'.format(800, 600))
        self.mainWindow = MainWindow(config, games, self.root)
    
    def start(self):
        self.root.mainloop()

class MainWindow:    
    def __init__(self, config, games, master):
        self.master = master
        self.config = config
        self.games = games
        self.poke_thread = None
        self.game_actions_frame = None
        master.title("Memshark")

        self.label = gui.Label(master, text="Wii U IP Address: {}".format(config.wii_u_ip))        
        self.close_button = gui.Button(master, text="Close", command=master.quit)
        
        self.game_options = [x.name for x in games.games]
        self.game_selected = gui.StringVar()        
        self.game_selected.trace('w', self.change_game_selection)
        self.game_list = gui.OptionMenu(master, self.game_selected, *self.game_options)
        self.game_list.config(width=50)
        # Calling this before the app is drawn causes it to crash
        # self.game_selected.set(self.game_options[0])

        self.label.grid()
        self.game_list.grid()

    def change_game_selection(self, name, index, mode):
        if self.game_actions_frame != None:
            self.game_actions_frame.destroy()
        self.game_actions_frame = gui.Frame(self.master)
        game_name = self.game_selected.get()
        game = self.games.game_lookup[game_name]                
        self.game_pokes = []
        for poke in game.memory_pokes:
            row = gui.Frame(self.game_actions_frame)
            name_label = gui.Label(row, text=poke.name)
            address_label = gui.Label(row, text=poke.address)
            value_label = gui.Label(row, text=poke.value)
            freeze = gui.IntVar()
            freeze.trace('w', self.change_frozen_values)
            freezeCheck = gui.Checkbutton(row, variable=freeze)            
            self.game_pokes.append((row,name_label,address_label,value_label,freeze, poke))
            row.grid()
            name_label.grid()
            address_label.grid()
            value_label.grid()
            freezeCheck.grid()
        self.game_actions_frame.grid()

    def change_frozen_values(self, name, index, mode):
        global KILL_THREAD
        pokes = []
        for tup in self.game_pokes:
            print("Tup[4] = {}".format(tup[4].get()))
            if tup[4].get() == 1:
                pokes.append(tup[5])
        if self.poke_thread != None:
            KILL_THREAD=True
            self.poke_thread.join()
        if len(pokes) > 0:
            KILL_THREAD=False
            self.poke_thread = threading.Thread(target=freeze_pokes, args=(pokes, self.config.freeze_poke_interval_seconds))
            self.poke_thread.start()

def freeze_pokes(pokes, interval_seconds):
    global KILL_THREAD
    while True and not KILL_THREAD:
        print("Running thread")
        for poke in pokes:
            print("Poking {}: {} -> {}".format(poke.name, poke.address, poke.value))
        time.sleep(interval_seconds)
    print("The thread is now dead")