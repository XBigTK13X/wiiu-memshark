from memshark import Memshark
from memshark_config import MemsharkConfig
from games import Games
import gui

config = MemsharkConfig('config.json')
games = Games('games')
memshark = Memshark(config)

app = gui.MainApp(config, games, memshark)
app.start()
