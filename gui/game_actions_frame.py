import tkinter as tk

from gui import table_widget

import time
import threading

class GameActionsFrame():
    
    KILL_THREAD = False

    def __init__(self, master, games, memshark):
        self.master = tk.Frame(master)

        self.games = games
        self.memshark = memshark
        self.poke_thread = None
        self.game_actions_frame = None

        self.game_options = [x.name for x in self.games.games]
        self.game_selected = tk.StringVar()
        self.game_selected.set("Choose a game...")
        self.game_selected.trace('w', self.change_game_selection)
        self.game_list = tk.OptionMenu(self.master, self.game_selected, *self.game_options)
        self.game_list.config(width=50, padx=10, pady=10)
        # Calling this before the app is drawn causes it to crash
        # self.game_selected.set(self.game_options[0])
        self.game_list.grid()

        self.game_version = tk.Label(self.master, text='')
        self.game_version.grid()

    def change_game_selection(self, name, index, mode):
        if self.game_actions_frame != None:
            self.game_actions_frame.destroy()
        self.game_actions_frame = tk.Frame(self.master)
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
        self.poke_table = table_widget.TableWidget(self.game_actions_frame)
        for poke in game.memory_pokes:
            name_label = tk.Label(self.poke_table, text=poke.name)
            address_label = tk.Label(self.poke_table, text=poke.address)
            value_label = tk.Label(self.poke_table, text=poke.value)
            poke_button = tk.Button(self.poke_table, text='Poke', command=lambda poke=poke: self.poke(poke))
            freeze = tk.IntVar()
            freeze.trace('w', self.change_frozen_values)
            freezeCheck = tk.Checkbutton(self.poke_table, variable=freeze)
            self.game_pokes.append((name_label, address_label, value_label, poke_button, freezeCheck, freeze, poke))
        self.poke_table.set_rows(self.game_pokes)
        # Kill any frozen values for the previous selection
        self.change_frozen_values(None, None, None)
        self.poke_table.grid()
        self.game_actions_frame.grid()

    def poke(self, poke):
        print("--DEBUG Poking {}: {} -> {}".format(poke.name, poke.address, poke.value))
        self.memshark.poke(poke.address, poke.value)

    def change_frozen_values(self, name, index, mode):
        pokes = []
        freeze_var_position = 5
        for tup in self.game_pokes:
            if len(tup) > freeze_var_position:
                if tup[freeze_var_position].get() == 1:
                    pokes.append(tup[len(tup)-1])
        if self.poke_thread != None:
            GameActionsFrame.KILL_THREAD = True
            self.poke_thread.join()
        if len(pokes) > 0:
            GameActionsFrame.KILL_THREAD = False
            self.poke_thread = threading.Thread(target=self.freeze_pokes, args=(pokes, self.config.freeze_poke_interval_seconds, self.memshark))
            self.poke_thread.start()

    def freeze_pokes(self, pokes, interval_seconds, memshark):
        while True and not GameActionsFrame.KILL_THREAD:
            for poke in pokes:
                print("--DEBUG Poking {}: {} -> {}".format(poke.name, poke.address, poke.value))
                memshark.poke(poke.address, poke.value)
            time.sleep(interval_seconds)