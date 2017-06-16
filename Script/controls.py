# coding: utf-8

from scene import *
import clock
import game_levels as levels

class Controls(object):
	
	
	def __init__(self, parent):
		
		self.parent = parent
		self.arrows = []
		self.deg_to_rad = 3.14 / 180.0
		
		self.add_arrow(50, self.parent.size.h/2, 0)
		self.add_arrow(self.parent.size.w - 50, self.parent.size.h/2, 180)
		self.add_arrow(self.parent.size.w/2, self.parent.size.h - 120, 270)
		self.add_arrow(self.parent.size.w/2, 60, 90)
		
		self.rotation = 0
		
	def add_arrow(self, x, y, rotation = 0):
		
		arrow = SpriteNode('arrow.png', parent=self.parent, position=(x, y))
		arrow.size = (40, 40)
		arrow.anchor_point = (0.5, 0.5)
		arrow.rotation = rotation * self.deg_to_rad
	
		self.arrows.append(arrow)
		
	def reverse(self):
		
		if self.rotation > 0:
			return 
			
		self.rotation = self.deg_to_rad * 180.0
		
		for arrow in self.arrows:
			arrow.rotation += self.rotation
			
	def clear_reverse(self):
		
		if self.rotation > 0:
			
			for arrow in self.arrows:
				arrow.rotation -= self.rotation
				
			self.rotation = 0.0
			