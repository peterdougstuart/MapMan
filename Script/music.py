import os
import os.path
import random
from sound import play_effect
from sound import stop_effect
from sound import Player
from time import sleep

#https://www.freefileconvert.com/mp3-caf

class Music:

	def __init__(self):
		pass
		
		self.player = None
	
	def play_menu(self):
		
		file = 'Brexit of Champions (opening).caf'
		
		if not self.player is None:
			self.player.stop()
		
		self.player = Player(file)
		self.player.play()

	def play_menu(self):
		self.play('Brexit of Champions (opening).caf')
		
	def play_end(self):
		self.play('Paris Breakup (end screen).caf')

	def play_game(self):
		
		if random.randint(1, 2) == 1:
			self.play('Tolerate Intolerance (mid game).caf')
		else:
			self.play('Worst of all Worlds (mid game).caf')
		
	def play(self, file):

		if not self.player is None:
			self.player.stop()
		
		file = os.path.join('GameMusic', file)
	
		self.player = MyPlayer(file)
		self.player.play()
	
	def stop(self):
		
		if not self.player is None:
			self.player.stop()
			
class MyPlayer:
	
	def __init__(self, file):
		self.effect_id = None
		self.file = file
		
	def play(self):
			
		self.stop()

		self.effect_id = play_effect(self.file)

	def stop(self):
		
		if self.effect_id is None:
			return
			
		stop_effect(self.effect_id)
