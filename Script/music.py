import os
import os.path
import random
import datetime
import os.path

from sound import play_effect
from sound import stop_effect
from sound import Player
from time import sleep

#https://www.freefileconvert.com/mp3-caf

class Music:

	def __init__(self):
		self.player = None
		self.menu = False
		self.restart_call = None
		self.duration = None
		
	def play_menu(self):
		
		if self.menu:
			return
			
		self.menu = True
		self.play('Brexit of Champions (opening).caf')
		
		self.restart_call = self.play_menu
		
	def play_end(self):
		self.menu = False
		self.play('Paris Breakup (end screen).caf')
		self.restart_call = self.play_end

	def play_game(self):
		
		self.menu = False
		number = random.randint(1, 5)
		
		if number == 1:
			self.play('A Boy named Crystal (mid game).caf')
		elif number == 2:
			self.play('A trace of empathy (mid game).caf')
		elif number == 3:
			self.play('Phishing for compliments (mid game).caf')
		elif number == 4:
			self.play('Questionable Thoughts (mid game).caf')
		else:
			self.play('TOlerate INtolerence (mid game).caf')
		
		self.restart_call = self.play_game
	
	def restart(self):
		
		if self.restart_call is None:
			return
		
		if (datetime.datetime.now() -self.start_time).total_seconds() > self.duration:
			self.restart_call()
			
	def play(self, file):
		
		if file is None:
			return
		
		if len(file) < 1:
			return
			
		if not self.player is None:
			self.player.stop()
		
		file = os.path.join('GameMusic', file)

		if not os.path.isfile(file):
			print "Music not found: {0}".format(file)
			return

		#self.player = MyPlayer(file)
		self.player = Player(file)
		self.player.play()
		
		self.duration = self.player.duration
		self.start_time = datetime.datetime.now()
	
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
