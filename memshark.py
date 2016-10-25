from vendor.tcpgecko import tcpgecko

class Memshark():
	def __init__(self, config):
		self.wii_u_ip = config.wii_u_ip
		self.tcp_gecko = None

	def connect(self):
		if self.is_connected():
			self.tcp_gecko.s.close()
		self.tcp_gecko = tcpgecko.TCPGecko(self.wii_u_ip)

	def disconnect(self):
		if self.is_connected():
			self.tcp_gecko.s.close()

	def poke(self, address, value):
		if not self.is_connected():
			return
		self.tcp_gecko.pokemem32(address,value)

	def is_connected(self):
		return self.tcp_gecko != None

	