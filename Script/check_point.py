from scene import SpriteNode
from scene import Texture
from scene import Action
import os.path
from scaler import Scaler

class CheckPoint(object):
	
	SCALE = 0.2
	FRAMES = 117
	
	def __init__(self, tile):

		self.frame = 0
		self.frames = self.load_frames()
		
		self.node = SpriteNode(self.frames[0])
		self.node.scale = 0
		
		self.node.anchor_point = (0.1, 0.05)
		self.node.position = (tile.node.position[0], tile.node.position[1] + tile.node.size.h/2)
		
		self.node.z_position = 1000.0
		
		self.parent = tile.node.parent
		self.parent.add_child(self.node)
		
	def load_frames(self):
		
		frames = []
		
		for index in range(CheckPoint.FRAMES):
			
			frame = index + 1
			
			image = "checkpoint{0:03d}.png".format(frame)
			
			path = Scaler.get_checkpoint_path(image)
			
			texture = self.create_texture(path)
			
			frames.append(texture)
			
		return frames

	def create_texture(self, image):
		try:
			return Texture(image)
		except:
			raise Exception('Cannot load image: {0}'.format(image))
			
	def __call__(self):
		self.advance_frame()
		
	def advance_frame(self):
		
		self.frame += 1
		
		if self.frame >= len(self.frames):
			self.frame = 0
		
		self.node.texture = self.frames[self.frame]

	def appear(self, wait):
		
		if self.node != None:
			
				change_frame = Action.call(self)
				wait_fame = Action.wait(1.0/60.0)
				frame = Action.sequence(change_frame, wait_fame)
				
				animate = Action.repeat(frame, 0)
				self.node.run_action(Action.sequence(Action.wait(wait), Action.scale_to(CheckPoint.SCALE, 0.25, 4), animate))
		
			
