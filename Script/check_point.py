from scene import *
import os.path
from scaler import Scaler

A = Action

class CheckPoint(object):
	
	SCALE = 0.2
	FRAMES_FOLDER = 'CheckPoint'
	FRAMES = 100
	
	def __init__(self, tile):

		self.frame = 0
		self.frames = self.load_frames()
		
		self.node = SpriteNode(self.frames[0])
		self.node.scale = 0
		
		self.node.anchor_point = (0.1, 0.05)
		self.node.position = (tile.node.position[0], tile.node.position[1] + tile.node.size.h/2)
		
		self.parent = tile.node.parent
		self.parent.add_child(self.node)
		
	def load_frames(self):
		
		frames = []
		
		for index in range(CheckPoint.FRAMES):
			
			frame = index + 1
			
			image = "MapMan-checkpoint-animated{0:02d}.png".format(frame)
			
			path = os.path.join(CheckPoint.FRAMES_FOLDER, image)
			
			texture = Texture(path)
			
			frames.append(texture)
			
		return frames
	
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
				self.node.run_action(A.sequence(A.wait(wait), A.scale_to(CheckPoint.SCALE, 0.25, 4), animate))
		
			
