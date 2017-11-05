# coding: utf-8
from scene import LabelNode
import clock
import game_levels as levels
import tutorial
import font
import sound
import datetime
from scaler import Scaler
import palette
import os.path

class Timer (LabelNode):
	
	FONT_SIZE = 50
	INITIAL_SECONDS = 20
	
	def __init__(self, parent):
		
		self.countdown = clock.Countdown(parent, Timer.INITIAL_SECONDS)
				
		LabelNode.__init__(self, '0', font=self.get_font(), position=(parent.size.w*0.5, parent.centre_height), parent=parent)
		
		self.anchor_point = (0.5, 0.5)
		
		self.player = sound.Player(os.path.join('SoundEffects','clock.caf'))
		self.player.number_of_loops = -1
		
		self.playing = False
		self.low_time = False
	
	def active(self):
		return self.countdown.started
		
	def get_font(self):
		
		if self.active():
			seconds = self.countdown.seconds_remaining(True)
		else:
			seconds = Timer.INITIAL_SECONDS
			
		if (seconds is None) or seconds > 3 or seconds < 0:
			multiplier = 1
		else:
			int_seconds = int(seconds)
			remainder_seconds = seconds - int_seconds
			multiplier = 1.0 + (3.0 - int_seconds + remainder_seconds*2) * 0.2
		
		font_size = multiplier*Timer.FONT_SIZE*Scaler.Timer
		
		font_size = max([font_size, 1])
		
		return (font.TIMER, font_size)
		
	def hide(self):
		self.scale = 0
		
	def show(self):
		self.scale = 1
		
	def blank(self):
		self.text = ''
		
	def update(self):
		
		if self.parent.parent.tutorial:
			self.blank()
			
		if not self.active():
			return
		
		seconds = self.countdown.seconds_remaining()
			
		self.font = self.get_font()
		self.text = str(seconds)
		
		if seconds > 0:
				
			if seconds <= 3:
					
				self.player.play()
				self.playing = True
				self.color = palette.LOW_TIME
				self.low_time = True
					
			else:
					
				self.stop_player()
				self.color = palette.NORMAL_TIME
				self.low_time = False
					
		else:
			
			self.stop_player()
			self.color = palette.DEATH_BG
			self.low_time = False
		
	def seconds_remaining(self):
		return self.countdown.seconds_remaining()
		
	def stop_player(self):
		if self.playing:
			self.player.stop()
			
	def stop(self):
		self.countdown.stop()
		self.stop_player()
			
	def start(self):
		self.countdown.start()
	
	def reset(self):
		self.countdown.reset()
		self.low_time = False
