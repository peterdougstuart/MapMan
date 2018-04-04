class Messenger (object):
	
	Instance = None
	
	def __init__(self, game):
		self.game = game

	@classmethod
	def get(cls):
		return cls.Instance

	@classmethod
	def initialize(cls, game):
		cls.Instance = Messenger(game)

	@classmethod
	def initialize_dummy(cls):
		cls.Instance = DummyMessenger()

	def show_message(self, message):
		self.game.show_message(message)
		
class DummyMessenger (object):
	
	def show_message(self, message):
		print message
