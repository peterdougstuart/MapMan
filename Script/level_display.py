# coding: utf-8

from scene import *
import game_levels as levels
import tutorial
import font

class LevelDisplay(object):
	
	def __init__(self, parent):
		
		self.reset()
		
		self.parent = parent
		
		self.add_score()
	
	def reset(self):
		self.level = levels.START_LEVEL
		self.score = 0
		
	def blank_score(self):
		self.score_label.text = ''
		
	def update(self):
		
		if not self.parent.tutorial:
			self.score_label.text = self.score_text()
		else:
			self.score_label.text = ''
		
	def add_score(self):
		
		self.score_label = LabelNode('', font=(font.LEVEL_DISPLAY, 40), position=(10, self.parent.size.h-30), parent=self.parent)
		
		self.score_label.anchor_point = (0, 0.5)

	def score_text(self):
		
		if not self.parent.tutorial:
			return "L{0}-{1}".format(self.level, self.score)
		else:
			return ''
	
	def advance_level(self):
		
		self.level += 1
		
		if not self.parent.tutorial:
			number_of_levels = len(levels.levels)
		else:
			number_of_levels = len(tutorial.levels)
			
		if self.level > number_of_levels:
			
			if self.parent.tutorial:
				self.parent.tutorial = False
				self.level = 1
			else:
				self.level = 1
