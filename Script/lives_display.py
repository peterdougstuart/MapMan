# coding: utf-8

from scene import *
import font

class LivesDisplay(object):
	
	INITIAL_LIVES = 3
	SCALE = 0.18
	
	def __init__(self, parent):
		
		self.lives = LivesDisplay.INITIAL_LIVES
		
		self.parent = parent
		
		self.add_lives()

	def hide(self):
		self.lives_label.scale = 0
		
	def show(self):
		self.lives_label.scale = 1
		
	def reset(self):
		self.lives = LivesDisplay.INITIAL_LIVES
		self.update()
		
	def blank_lives(self):
		self.lives_label.text = ''
		
	def update(self):
		
		if not self.parent.tutorial:
			self.lives_label.text = self.lives_text()
			self.heart.scale = LivesDisplay.SCALE
		else:
			self.lives_label.text = ''
			self.heart.scale = 0
		
	def add_lives(self):
		
		x = self.parent.size.w - 45
		y = self.parent.size.h - 30
		
		self.lives_label = LabelNode('', font=(font.LIVES_DISPLAY, 40), position=(x, y), parent=self.parent)
		self.lives_label.anchor_point=(1, 0.5)

		heart = Texture('heart.png')
		
		self.heart = SpriteNode(heart)
		self.heart.anchor_point = (0.5, 0.5)
		self.heart.position = (x + 18, y + 2)
		self.heart.scale = 0
		
		self.parent.add_child(self.heart)

	def lives_text(self):
		
		if not self.parent.tutorial:
			return "{0}".format(self.lives)
		else:
			return ''
	
