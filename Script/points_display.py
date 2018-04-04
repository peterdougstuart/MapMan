# coding: utf-8

from scene import LabelNode
from scene import Texture
import font
from scaler import Scaler

class PointsDisplay(object):
	
	def __init__(self, parent):
		
		self.score = 0
		self.parent = parent
		
		self.add_score()
		self.update()
		
	def hide(self):
		self.score_label.scale = 0
		self.star.size = (0, 0)
		
	def show(self):
		self.score_label.scale = 1
		self.star.size = self.base_size
		self.update()
		
	def reset(self):
		self.score = 0
		self.update()
		
	def update(self):
		
		if not self.parent.tutorial:
			self.score_label.text = self.score_text()
			self.position()
		else:
			self.hide()
		
	def add_score(self):
		
		self.score_label = LabelNode(text='', font=(font.SCORE_DISPLAY, 40*Scaler.Score), parent=self.parent)
		
		self.score_label.anchor_point = (0.5, 0.5)
		
		self.star = Scaler.new_sprite(Texture(Scaler.get_star_path('star_white_transparent.png')))
		
		self.star.anchor_point = (0.5, 0.5)
		
		self.base_size = self.star.size
		
		self.parent.add_child(self.star)
		
		self.position()
		
	def position(self):
		
		x = self.parent.size.w/2
		y = self.parent.size.h-30-Scaler.DisplayShift
		
		self.star.position = (x+self.star.size.w*0.5, y+self.star.size.h*0.1)
		
		self.score_label.position = (x-self.score_label.size.w*0.5, y)
		
	def score_text(self):
		
		return "{0}".format(self.score)
