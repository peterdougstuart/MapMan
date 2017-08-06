# coding: utf-8

from scene import *
import clock
import game_levels as levels
import tutorial
import font
import sound
import datetime
from scaler import Scaler
import palette

class Timer (LabelNode):
	
	FONT_SIZE = 50
	
	def __init__(self, parent):
		
		self.countdown = clock.Countdown(parent, 20)
				
		LabelNode.__init__(self, '0', font=self.get_font(), position=(parent.size.w*0.5, parent.centre_height), parent=parent)
		
		self.anchor_point = (0.5, 0.5)
		
		self.player = sound.Player('game:Clock_1')
		self.player.number_of_loops = -1
		
		self.playing = False
		self.low_time = False
		self.dead = False
	
	def get_font(self, seconds=None):
		
		if seconds < 1:
			seconds = 1
			
		if (seconds is None) or seconds >= 4 or seconds < 0:
			multiplier = 1
		else:
			int_seconds = int(seconds)
			remainder_seconds = seconds - int_seconds
			multiplier = 1.1 + (3.0 - int_seconds + remainder_seconds*2) * 0.2
		
		#multiplier *= multiplier
		
		font_size = multiplier*Timer.FONT_SIZE*Scaler.get_scale()
		
		font_size = max([font_size, 1])
		
		return (font.TIMER, font_size)
		
	def hide(self):
		self.scale = 0
		
	def show(self):
		self.scale = 1
		
	def blank_timer(self):
		self.text = ''
		
	def update(self):
		
		if self.dead:
			return
			
		if not self.parent.parent.tutorial:
			
			seconds = self.countdown.seconds_remaining()
			
			self.font = self.get_font(seconds)
			
			if seconds > 0:
				
				int_seconds = int(seconds)
				self.text = str(int_seconds)
				
				if seconds < 4:
					
					self.player.play()
					self.playing = True
					
					if int_seconds > 0:
						self.color = palette.LOW_TIME
					else:
						self.color = palette.DEATH_BG
						
					self.low_time = True
					
				else:
					
					self.color = palette.NORMAL_TIME
					self.low_time = False
					
			else:
				
				self.text = ''
				self.low_time = False
				
				if self.playing:
					self.player.stop()
				
		else:
			
			self.text = ''
	
	def lose_life(self):
		
		self.dead = True
		
		if self.playing:
			self.player.stop()
			
	def complete_level(self):
		
		if self.playing:
			self.player.stop()
		
		self.low_time = False
		self.dead = False
			
	def advance_level(self):
		self.reset()
	
	def reset(self, reset_initial_seconds=False):
		self.countdown.reset(reset_initial_seconds)
		self.dead = False
