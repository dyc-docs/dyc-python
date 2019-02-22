class Processor():
	"""Subclass process that runs complete lifecycle for DYC"""
	def start(self):
		self.setup()
		self.prompts()
		self.apply()
