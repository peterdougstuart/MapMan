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
		self.hide_texture = self.create_texture('hide.png')
		
		self.node = SpriteNode(self.off_texture)
		self.node_top = SpriteNode(self.off_texture)
		self.node_bottom = SpriteNode(self.off_texture)
				
		self.hide_effect()
		
		self.node.anchor_point = (0, 0)
		self.node_top.anchor_point = (0, 0)
		self.node_bottom.anchor_point = (0, 0)
		
		self.node.position = (5, 5)
		self.node_top.position = (25, 45)
		self.node_bottom.position = (25, 5)
		
		self.parent = parent
		self.parent.add_child(self.node)
		self.parent.add_child(self.node_top)
		self.parent.add_child(self.node_bottom)
	
	def create_texture(self,image):
		return Texture(os.path.join(Effect.FOLDER, image))

	def reverse_and_vanish(self):
		self.show_double()
		self.node_top.texture = self.reverse_texture
		self.node_bottom.texture = self.vanish_texture

	def hide(self):
		self.show_effect()
		self.node.texture = self.hide_texture
		
	def vanish(self):
		self.show_effect()
		self.node.texture = self.vanish_texture

	def reverse(self):
		self.show_effect()
		self.node.texture = self.reverse_texture
	
	def sticky(self):
		self.show_effect()
		self.node.texture = self.sticky_texture

	def points(self):
		self.show_effect()
		self.node.texture = self.points_texture

	def life(self):
		self.show_effect()
		self.node.texture = self.life_texture
		
	def more_time(self):
		self.show_effect()
		self.node.texture = self.more_time_texture
	
	def less_time(self):
		self.show_effect()
		self.node.texture = self.less_time_texture
		
	def clear(self):
		self.hide_effect()
		self.node.texture = self.off_texture
		
	def show_effect(self):
		self.node_top.scale = 0
		self.node_bottom.scale = 0
		self.node.scale = Effect.SCALE

	def show_double(self):
		self.node_top.scale = 0.5 * Effect.SCALE
		self.node_bottom.scale = 0.5 * Effect.SCALE
		self.node.scale = 0
		
	def hide_effect(self):
		self.node_top.scale = 0
		self.node_bottom.scale = 0
		self.node.scale = 0
