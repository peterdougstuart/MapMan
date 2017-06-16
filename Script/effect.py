# coding: utf-8
from scene import *
import os.path

class Effect(object):
	
	SCALE = 0.5
	FOLDER = 'Effects'
	
	def __init__(self, parent):
		
		self.off_texture = self.create_texture('off.png')
		self.reverse_texture = self.create_texture('reverse.png')
		self.vanish_texture = self.create_texture('vanish.png')
		self.sticky_texture = self.create_texture('sticky.png')
		self.points_texture = self.create_texture('points.png')
		self.more_time_texture = self.create_texture('more_time.png')
		self.less_time_texture = self.create_texture('less_time.png')
		self.life_texture = self.create_texture('life.png')
		
		self.node = SpriteNode(self.off_texture)
		self.hide()
		
		self.node.anchor_point = (0, 0)
		
		self.node.position = (5,5)
		
		self.parent = parent
		self.parent.add_child(self.node)
	
	def create_texture(self,image):
		return Texture(os.path.join(Effect.FOLDER, image))
		
	def vanish(self):
		self.show()
		self.node.texture = self.vanish_texture

	def reverse(self):
		self.show()
		self.node.texture = self.reverse_texture
	
	def sticky(self):
		self.show()
		self.node.texture = self.sticky_texture

	def points(self):
		self.show()
		self.node.texture = self.points_texture

	def life(self):
		self.show()
		self.node.texture = self.life_texture
		
	def more_time(self):
		self.show()
		self.node.texture = self.more_time_texture
	
	def less_time(self):
		self.show()
		self.node.texture = self.less_time_texture
		
	def clear(self):
		self.hide()
		self.node.texture = self.off_texture
		
	def show(self):
		self.node.scale = Effect.SCALE
	
	def hide(self):
		self.node.scale = 0
