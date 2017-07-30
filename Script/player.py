# coding: utf-8
from scene import *
import os.path
from scaler import Scaler

class Player (object):
	
	SCALE = 0.4
	FOLDER = 'Man'
	FRAMES_FOLDER = 'Frames'
	IDLE_FOLDER = 'Idle'
	FRAMES = 14
	
	def __init__(self, parent):
		
		self.base_scale = Player.SCALE * Scaler.get_scale()
		
		self.x_scale = self.base_scale
		self.y_scale = self.base_scale
		
		self.up_idle = [Texture(os.path.join(Player.FOLDER, Player.IDLE_FOLDER, 'MapMan-idle-BACK-2.png'))]
		
		self.down_idle = [Texture(os.path.join(Player.FOLDER, Player.IDLE_FOLDER, 'MapMan-idle-FRONT-2.png'))]
		
		self.side_idle = [Texture(os.path.join(Player.FOLDER, Player.IDLE_FOLDER, 'MapMan-idle-SIDE-2.png'))]
		
		self.idle = self.down_idle
		
		self.up = self.load_frames('BACK')
		self.down =  self.load_frames('FORWARD')
		self.side = self.load_frames('SIDE')
		
		self.death = self.load_death()
		
		self.node = SpriteNode(self.idle[0])
		
		self.hide()
		
		self.node.anchor_point = (0.5, -0.05)
		
		self.parent = parent
		self.parent.add_child(self.node)
		
		self.frame = 0
		self.frames = self.idle
	
	def hide(self):
		self.vanish()
	
	def load_death(self):
		
		frames = []
		
		for index in range(21):
			frame = index
			image = "MapMan-death-2x-FRONT-_000{0:02d}.png".format(frame)
			folder = os.path.join(Player.FOLDER, 'Death')
			texture = Texture(os.path.join(folder, image))
			frames.append(texture)
			frames.append(texture)
			
		return frames
		
	def load_frames(self, tag):
		
		frames = []
		
		for index in range(Player.FRAMES):
			frame = index + 1
			image = "MapMan-walkcycle-{0}-2{1:02d}.png".format(tag, frame)
			folder = os.path.join(Player.FOLDER, Player.FRAMES_FOLDER)
			texture = Texture(os.path.join(folder, image))
			frames.append(texture)
			
		return frames
		
	def face(self, frames, x_scale=None, y_scale=None):
		
		if x_scale is None:
			self.x_scale = self.base_scale
		else:
			self.x_scale = x_scale

		if y_scale is None:
			self.y_scale = self.base_scale
		else:
			self.y_scale = y_scale
			
		self.frames = frames
		self.frame = 0
		
		self.draw()

	def face_death(self):
		self.face(self.death, self.base_scale/2, self.base_scale/2)
		
	def face_up(self):
		self.face(self.up)

	def face_down(self):
		self.face(self.down)
	
	def face_left(self):
		self.face(self.side, -self.base_scale)
	
	def face_right(self):
		self.face(self.side)
	
	def face_up_idle(self):
		self.face(self.up_idle)

	def face_down_idle(self):
		self.face(self.down_idle)
	
	def face_left_idle(self):
		self.face(self.side_idle, -self.base_scale)
	
	def face_right_idle(self):
		self.face(self.side_idle)
		
	def face_idle(self):
		self.face(self.idle)
	
	def vanish(self):
		self.node.x_scale = 0
		self.node.y_scale = 0
		self.hidden = True
	
	def show(self):
		self.node.x_scale = self.x_scale
		self.node.y_scale = self.y_scale
		self.hidden = False
				
	def update(self, position):

		self.node.position = position
		self.advance_frame()
	
	def draw(self):
		
		if not self.hidden:
			self.node.x_scale = self.x_scale
			self.node.y_scale = self.y_scale
		
		self.node.texture = self.frames[self.frame]
			
	def advance_frame(self):
		
		self.frame += 1
		
		if self.frame >= len(self.frames):
			self.frame = 0
		
		self.draw()
		
	def on_last_frame(self):
		
		if self.frame == (len(self.frames)-1):
			return True
		else:
			return False
		
			

