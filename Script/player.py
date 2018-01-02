# coding: utf-8
from scene import Texture
from scaler import Scaler

class Player (object):
	
	FRAMES = 14
	DEATH_FRAMES = 21
	
	def __init__(self, parent):
		
		self.up_idle = [self.create_texture(Scaler.get_man_idle_path('back.png'))]
		
		self.down_idle = [self.create_texture(Scaler.get_man_idle_path('front.png'))]
		
		self.side_idle = [self.create_texture(Scaler.get_man_idle_path('side.png'))]
		
		self.idle = self.side_idle
		
		self.up = self.load_frames('back')
		self.down =  self.load_frames('forward')
		self.side = self.load_frames('side')
		
		self.death = self.load_death()
		
		self.node = Scaler.new_sprite(self.idle[0])
		self.node.z_position = 1001.0

		self.base_scale = self.node.scale
		self.base_size = self.node.size
		
		self.hide()
		
		self.node.anchor_point = (0.5, -0.05)

		self.x_scale = self.base_scale
		self.y_scale = self.base_scale
		
		self.parent = parent
		self.parent.add_child(self.node)
		
		self.frame = 0
		self.frames = self.idle
	
	def hide(self):
		self.vanish()
	
	def load_death(self):
		
		frames = []
		
		for index in range(Player.DEATH_FRAMES):
			frame = index
			image = "death{0:02d}.png".format(frame)
			texture = self.create_texture(Scaler.get_death_path(image))
			frames.append(texture)
			frames.append(texture)
			
		return frames
		
	def load_frames(self, tag):
		
		frames = []
		
		for index in range(Player.FRAMES):
			frame = index + 1
			image = "{0}{1:02d}.png".format(tag, frame)
			texture = self.create_texture(Scaler.get_man_frames_path(image))
			frames.append(texture)
			
		return frames

	def create_texture(self, image):
		try:
			return Texture(image)
		except:
			raise Exception('Image not found: {0}'.format(image))
			
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
		self.face(self.death, self.base_scale, self.base_scale)
		
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
		self.node.size = self.base_size
			
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
		
			

