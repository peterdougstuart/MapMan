import os
import os.path
import random
import datetime
import os.path

from sound import play_effect
from sound import stop_effect
from sound import Player
from time import sleep

class Music:

	def __init__(self):
		
		self.player = None
		self.menu = False
		self.restart_call = None
		self.duration = None
		
		self.paused = False
		self.start_pause = None
		self.pause_duration = None
		self.completion = 1
		
	def play_menu(self):
		
		if self.menu:
			return
			
		self.menu = True
		self.completion = 1
		
		self.play('Brexit of Champions (opening).caf')
		
		self.restart_call = self.play_menu
		
	def play_end(self):
		self.menu = False
		self.play('Paris Breakup (end screen).caf')
		self.restart_call = self.play_end

	def play_completion_scoring(self):
		
		self.menu = False
		self.completion = 1
		
		self.play('Calling it a day (completion scoring).caf')
			
		self.restart_call = self.play_completion_scoring
		
	def play_completion_menu(self):
		
		self.menu = False
		
		if self.completion == 1:
			self.play('Starry Starry Bye (completion menu).caf')
			self.completion = 2
		else:
			self.play('Fly away my old friend (completion menu).caf')
			self.completion = 1
			
		self.restart_call = self.play_completion_menu
		
	def play_game(self):
		
		self.menu = False
		self.completion = 1
		
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
		
		if self.paused:
			self.check_pause()
			if self.paused:
				return
				
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
			raise Exception('Music not found: {0}'.format(file))

		self.player = Player(file)
		self.player.play()
		
		self.duration = self.player.duration
		self.start_time = datetime.datetime.now()
		
		self.paused = False
		self.start_pause = None
		self.pause_duration = None
		
	def pause(self, pause_duration):
		
		self.start_pause = datetime.datetime.now()
		self.pause_duration = pause_duration
		
		self.paused = True
		self.stop()
	
	def check_pause(self):
		
		if self.start_pause is None:
			self.paused = False
			return
		
		if (datetime.datetime.now() -self.start_pause) > self.pause_duration:
			
			self.start_time += self.pause_duration
			
			self.paused = False
			self.pause_duration = None
			self.start_pause = None
			
			if not self.player is None:
				self.player.play()
		
	def stop(self):
		
		if not self.player is None:
			self.player.stop()
			
