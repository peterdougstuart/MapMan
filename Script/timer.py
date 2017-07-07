# coding: utf-8

from scene import *
import clock
import game_levels as levels
import tutorial

class Timer (object):
	
	def __init__(self, parent):
		
		self.level = 1
		
		self.parent = parent
		
		self.countdown = clock.Countdown(parent, 20)
		
		self.add_countdown()
		
	def blank_timer(self):
		self.timer_label.text = ''
		
	def add_countdown(self):
		
		self.timer_label = LabelNode('0', font=('Avenir Next', 50), position=(self.parent.size.w/2, 42.5), parent=self.parent)
		
	def update(self):
		
		if not self.parent.tutorial:
			
			seconds = self.countdown.seconds_remaining()
			
			if seconds > 0:
				self.timer_label.text = str(seconds)
			else:
				self.timer_label.text = ''
			
		else:
			self.timer_label.text = ''
	
	def advance_level(self):
		self.countdown.reset()
