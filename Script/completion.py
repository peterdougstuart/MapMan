# coding: utf-8
from scene import Texture
from scaler import Scaler


class MapWoman (object):
	
	FRAMES = 14
	
	def __init__(self, parent):
		
		self.up_idle = [self.create_texture(Scaler.get_woman_idle_path('back.png'))]
		
		self.down_idle = [self.create_texture(Scaler.get_woman_idle_path('front.png'))]
		
		self.side_idle = [self.create_texture(Scaler.get_woman_idle_path('side.png'))]
		
		self.idle = [self.create_texture(Scaler.get_woman_idle_path('neutral.png'))]
		
		self.up = self.load_frames('back')
		self.down =  self.load_frames('forward')
		self.side = self.load_frames('side')
		
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
		
	def load_frames(self, tag):
		
		frames = []
		
		for index in range(MapWoman.FRAMES):
			frame = index + 1
			image = "{0}{1:02d}.png".format(tag, frame)
			texture = self.create_texture(Scaler.get_woman_frames_path(image))
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
	
	def hide(self):
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


class AnimatedBase(object):
	
	def __init__(self, parent):
		
		self.frames = self.load_frames()
		
		self.node = Scaler.new_sprite(self.frames[0])
		self.node.z_position = 999.0

		self.base_scale = self.node.scale
		self.base_size = self.node.size
		
		self.hide()
		
		self.node.anchor_point = (0.5, 0.35)

		self.x_scale = self.base_scale
		self.y_scale = self.base_scale
		
		self.parent = parent
		self.parent.add_child(self.node)
		
		self.frame = 0

	def number_of_frames(self):
		pass
		
	def load_frames(self):
		pass
		
	def load_frames_base(self, tag, method):
		
		frames = []
		
		for index in range(self.number_of_frames()):
			frame = index
			image = "{0}{1:02d}.png".format(tag, frame)
			texture = self.create_texture(method(image))
			frames.append(texture)
			
		return frames

	def create_texture(self, image):
		try:
			return Texture(image)
		except:
			raise Exception('Image not found: {0}'.format(image))
	
	def hide(self):
		self.node.x_scale = 0
		self.node.y_scale = 0
		self.hidden = True
	
	def show(self):
		self.node.x_scale = self.x_scale
		self.node.y_scale = self.y_scale
		self.hidden = False
				
	def update(self, position=None):
		if not position is None:
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
			
class Vortex (AnimatedBase):
	
	FRAMES = 90

	def number_of_frames(self):
		return Vortex.FRAMES
		
	def load_frames(self):
		return self.load_frames_base('vortex', Scaler.get_vortex_frames_path)

class Hearts(AnimatedBase):
	
	FRAMES = 90

	def __init__(self, parent):
		AnimatedBase.__init__(self, parent)
		self.node.z_position = 3000
		
	def number_of_frames(self):
		return Hearts.FRAMES
		
	def load_frames(self):
		return self.load_frames_base('hearts', Scaler.get_hearts_frames_path)
