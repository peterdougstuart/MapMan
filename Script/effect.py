# coding: utf-8
from scene import Texture
import os.path
from scaler import Scaler


class Effect(object):
	
	def __init__(self, parent):
		
		self.off_texture = self.create_texture(Scaler.get_effect_path('off.png'))
		self.reverse_texture = self.create_texture(Scaler.get_effect_path('reverse.png'))
		self.vanish_texture = self.create_texture(Scaler.get_effect_path('vanish.png'))
		self.sticky_texture = self.create_texture(Scaler.get_effect_path('sticky.png'))
		self.points_texture = self.create_texture(Scaler.get_effect_path('points.png'))
		self.more_time_texture = self.create_texture(Scaler.get_effect_path('more_time.png'))
		self.less_time_texture = self.create_texture(Scaler.get_effect_path('less_time.png'))
		self.life_texture = self.create_texture(Scaler.get_effect_path('life.png'))
		self.hide_texture = self.create_texture(Scaler.get_effect_path('hide.png'))
		self.unhide_texture = self.create_texture(Scaler.get_effect_path('unhide.png'))
				
		self.node = Scaler.new_sprite(self.off_texture)		
		self.node_top = Scaler.new_sprite(self.off_texture)
		self.node_bottom = Scaler.new_sprite(self.off_texture)

		self.base_size = Scaler.size_from_texture(self.points_texture)

		self.hide_effect()
		
		self.node.anchor_point = (0, 0)
		self.node_top.anchor_point = (0, 0)
		self.node_bottom.anchor_point = (0, 0)
		
		self.node.position = (5 * Scaler.Bottom_bar, 2 * Scaler.Bottom_bar)
		self.node_top.position = (25 * Scaler.Bottom_bar, 42 * Scaler.Bottom_bar)
		self.node_bottom.position = (25 * Scaler.Bottom_bar, 2 * Scaler.Bottom_bar) 
		
		self.parent = parent
		self.parent.add_child(self.node)
		self.parent.add_child(self.node_top)
		self.parent.add_child(self.node_bottom)
	
	def create_texture(self, image):
		try:
			return Texture(image)
		except:
			raise Exception('Cannot load image: {0}'.format(image))

	def reverse_and_vanish(self):
		self.node_top.texture = self.reverse_texture
		self.node_bottom.texture = self.vanish_texture
		self.show_double()

	def reverse_and_hidden(self):
		self.node_top.texture = self.reverse_texture
		self.node_bottom.texture = self.hide_texture
		self.show_double()

	def reverse_and_stuck(self):
		self.node_top.texture = self.reverse_texture
		self.node_bottom.texture = self.sticky_texture
		self.show_double()
		
	def unhide(self):
		self.node.texture = self.unhide_texture
		self.show_effect()
		
	def hide(self):
		self.node.texture = self.hide_texture
		self.show_effect()
		
	def vanish(self):
		self.node.texture = self.vanish_texture
		self.show_effect()

	def reverse(self):
		self.node.texture = self.reverse_texture
		self.show_effect()
	
	def sticky(self):
		self.node.texture = self.sticky_texture
		self.show_effect()

	def points(self):
		self.node.texture = self.points_texture
		self.show_effect()

	def life(self):
		self.node.texture = self.life_texture
		self.show_effect()
		
	def more_time(self):
		self.node.texture = self.more_time_texture
		self.show_effect()
	
	def less_time(self):
		self.node.texture = self.less_time_texture
		self.show_effect()
		
	def clear(self):
		self.node.texture = self.off_texture
		self.hide_effect()
		
	def show_effect(self):
		self.node_top.size = (0, 0)
		self.node_bottom.size = (0, 0)
		self.node.size = self.base_size

	def show_double(self):
		self.node_top.size = 0.5 * self.base_size
		self.node_bottom.size = 0.5 * self.base_size
		self.node.size = (0, 0)
		
	def hide_effect(self):
		self.node_top.size = (0, 0)
		self.node_bottom.size = (0, 0)
		self.node.size = (0, 0)
