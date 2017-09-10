# coding: utf-8

from scene import *
import font

class PointsDisplay(object):
	
	def __init__(self, parent):
		
		self.reset()
		self.parent = parent
		self.add_score()

	def hide(self):
		self.score_label.scale = 0
		
	def show(self):
		self.score_label.scale = 1
		
	def reset(self):
		self.score = 0
		
	def blank_score(self):
		self.score_label.text = ''
		
	def update(self):
		
		if not self.parent.tutorial:
			self.score_label.text = self.score_text()
		else:
			self.score_label.text = ''
		
	def add_score(self):
		
		self.score_label = LabelNode('', font=(font.SCORE_DISPLAY, 40), position=(self.parent.size.w/2, self.parent.size.h-30), parent=self.parent)
		
		self.score_label.anchor_point = (0.5, 0.5)

	def score_text(self):
		
		if not self.parent.tutorial:
			return "{0}{1}".format(self.score, font.STAR)
		else:
			return ''
	
