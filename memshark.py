from py_gecko import tcpgecko

class Memshark():
	def __init__(self, wii_u_ip):
		self.wii_u_ip = wii_u_ip
		self.tcp_gecko = None

	def connect(self):
		if self.tcp_gecko != None:
			self.tcp_gecko.s.close()
		self.tcp_gecko = TCPGecko(self.wii_u_ip)

	def disconnect():
		if self.tcp_gecko != None:
			self.tcp_gecko.s.close()

	def poke(self, address, value):
		if self.tcp_gecko == None:
			return
		self.tcp_gecko.pokemem32(address,value)

	