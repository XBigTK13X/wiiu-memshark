from memshark_config import MemsharkConfig
from games import Games
from gui import gui
from background import background, memshark, server

config = MemsharkConfig('config.json')
games = Games('games')
memshark = memshark.Memshark(config)
exploit_server = server.ExploitServer()

background.schedule(memshark)
background.schedule(exploit_server)


app = gui.MainApp(config, games, memshark, exploit_server)
app.start()
