import os

from scene import Texture
from scene import SpriteNode

class Gradient:

	GRADIENTS_FOLDER = 'Gradients'
	
	def __init__(self, parent, bottom_bar_height=0):
		
		background_texture = Texture(os.path.join(Gradient.GRADIENTS_FOLDER, 'MapMan-background-TRANSPARENCY.png'))
		
		self.background_gradient = SpriteNode(position=(0, bottom_bar_height), parent=parent)
		self.background_gradient.anchor_point=(0,0)
		
		self.background_gradient.texture = background_texture
		self.background_gradient.size=(parent.size.w, parent.size.h - bottom_bar_height)
