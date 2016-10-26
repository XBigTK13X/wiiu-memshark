from vendor.tcpgecko import tcpgecko

import time

class Memshark():
	def __init__(self, config):
		self.wii_u_ip = config.wii_u_ip
		self.tcp_gecko = None
		self.pokes = []

	def connect(self):
		if self.is_connected():
			self.tcp_gecko.s.close()
		try:
			self.tcp_gecko = tcpgecko.TCPGecko(self.wii_u_ip)
		except Exception:
			print("An error occurred when connecting to TCPGecko on the Wii U")
			print("Is TCPGecko not running on {}?".format(self.wii_u_ip))

	def disconnect(self):
		if self.is_connected():
			self.tcp_gecko.s.close()

	def poke(self, target):
		# print("--DEBUG Poking {}: {} -> {}".format(target.name, target.pretty_address, target.pretty_value))
		if not self.is_connected():
			return
		self.tcp_gecko.pokemem32(target.address,target.value)

	def is_connected(self):
		return self.tcp_gecko != None

	def handle_message(self, message):
		if isinstance(message, list):
			self.pokes = message
		elif isinstance(message, dict):
			self.poke(message['poke'])
		else:
			getattr(self, message)()

	def background(self):
		for poke in self.pokes:
			self.poke(poke)

	