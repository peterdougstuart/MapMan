# coding: utf-8

from scene import *
from effect import Effect
from timer import Timer

class BottomBar (object):
	
	FONT = 'Avenir Next'
	
	def __init__(self, parent):
		
		self.parent = parent
		self.add_background()
		self.add_controls_message()
		self.add_time_message()
		self.timer = Timer(parent)
		self.effect = Effect(parent)

	def add_background(self):
		self.height = 90
		self.top_bg = SpriteNode(parent=self.parent, position=(0, self.height))
		self.top_bg.color = '#1c1c1c'
		self.top_bg.size = self.parent.size.w, self.height
		self.top_bg.anchor_point = (0, 1)
		
	def set_time_message(self,text,size=30):
		self.set_controls([self.time_message_label_bottom], text, size)
	
	def set_controls_message(self,text,size=30):
		self.set_controls([self.controls_message_label_bottom], text, size)
		
	def add_controls_message(self):
		
		self.controls_message_label_bottom = LabelNode(parent=self.parent)
		self.controls_message_label_bottom.anchor_point = (0, 0.5)
		self.controls_message_label_bottom.position = (90, 50)
		
	def add_time_message(self):
	
		self.time_message_label_bottom = LabelNode(position=(self.parent.size.w-100, 45), parent=self.parent)
	
	def set_controls(self, controls, text, size):
		
		for control in controls:
			control.text = text
			control.font = (BottomBar.FONT, size)
