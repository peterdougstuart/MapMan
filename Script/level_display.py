# coding: utf-8

from scene import LabelNode
import game_levels as levels
import tutorial
import font
from scaler import Scaler

class LevelDisplay(object):
	
	def __init__(self, parent):
		self.reset()
		self.parent = parent
		self.add_level()
		self.level_count = len(levels.levels)

	def hide(self):
		self.level_label.scale = 0
		
	def show(self):
		self.level_label.scale = 1
		
	def reset(self):
		self.level = levels.START_LEVEL
		
	def update(self):
		
		if not self.parent.tutorial:
			self.level_label.text = self.level_text()
		else:
			self.level_label.text = ''
		
	def add_level(self):
		
		self.level_label = LabelNode('', font=(font.LEVEL_DISPLAY, 40), position=(10, self.parent.size.h-30-Scaler.DisplayShift), parent=self.parent)
		
		self.level_label.anchor_point = (0, 0.5)

	def level_text(self):
		
		if not self.parent.tutorial:
			return "L{0}/{1}".format(self.level, self.level_count)
		else:
			return ''
	
	def advance_level(self):
		
		self.level += 1
		self.update()
