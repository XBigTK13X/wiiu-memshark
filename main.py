from memshark import Memshark
from memshark_config import MemsharkConfig
from games import Games
from gui import gui
from server import ExploitServer

config = MemsharkConfig('config.json')
games = Games('games')
memshark = Memshark(config)
exploit_server = ExploitServer()

app = gui.MainApp(config, games, memshark, exploit_server)
app.start()
