# coding: utf-8

from scene import *
import clock
import game_levels as levels
import tutorial
import font
import sound
import datetime
from scaler import Scaler

class Timer (LabelNode):
	
	def __init__(self, parent):
		
		LabelNode.__init__(self, '0', font=(font.TIMER, int(50*Scaler.get_scale())), position=(parent.size.w/2, parent.size.h/2), parent=parent)
		
		self.player = sound.Player('game:Clock_1')
		self.player.number_of_loops = -1
		
		self.countdown = clock.Countdown(parent, 20)
		
		self.playing = False
		
	def blank_timer(self):
		self.text = ''
		
	def update(self):
		
		if not self.parent.parent.tutorial:
			
			seconds = self.countdown.seconds_remaining()
			
			if seconds > 0:
				self.text = str(seconds)
				if seconds <= 3:
					self.player.play()
					self.playing = True
			else:
				self.text = ''
				if self.playing:
					self.player.stop()
				
		else:
			
			self.text = ''
	
	def advance_level(self):
		
		self.countdown.reset()
		
		if self.playing:
			self.player.stop()
