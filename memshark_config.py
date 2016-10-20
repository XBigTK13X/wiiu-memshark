import json

class MemsharkConfig():	
	def __init__(self, configPath):
		with open(configPath) as json_file:    
			self.get = json.load(json_file)
		self.wii_u_ip = self.get['wii_u_ip']
		self.freeze_poke_interval_seconds = self.get['freeze_poke_interval_seconds']
		self.window_width = self.get['window_width']
		self.window_height = self.get['window_height']