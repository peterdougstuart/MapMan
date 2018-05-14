import os.path
import scene
from scene import SpriteNode

class Scaler (object):
	
	Resolution = None
	Bottom_bar = None
	Menu = None
	Timer = None
	Score = None
	DisplayShift = None
	Lives = None
	Size = None
	
	@staticmethod
	def initialize(game):
		
		if game.size.w >= 1024:
			
			#iPad
			Scaler.Size = 'Large'

			Scaler.Bottom_bar = 2
			Scaler.Timer = 2
			Scaler.Menu = 2
			Scaler.Score = 1
			Scaler.Lives = 1
			
			Scaler.Resolution = '2x'
			Scaler.DisplayShift = 15
			
		else:
			
			Scaler.DisplayShift = 0
			
			#iphone
			if scene.get_screen_scale() <= 1.0:
				Scaler.Resolution = '1x'
			elif scene.get_screen_scale() == 2.0:
				Scaler.Resolution = '2x'
			else:
				Scaler.Resolution = '3x'

			Scaler.Score = 1.0
			Scaler.Lives = 1.0
			Scaler.Bottom_bar = 1.0
			Scaler.Menu = 1.0
			Scaler.Timer = 1.0

			if game.size.w < 667:
				
				#iphone 4 and below
				
				if Scaler.Resolution == '1x':
					Scaler.Size = 'Tiny'
				else:
					Scaler.Size = 'Small'

			else:
				
				#iPhone 5, 6, 7
				Scaler.Size = 'Normal'

	@staticmethod
	def update_texture(node, texture):
		
		node.texture = texture
		
		node.size = Scaler.size_from_texture(texture)
		
	@staticmethod
	def size_from_texture(texture):

		if Scaler.Resolution == '1x':
			scale = 1.0
		elif Scaler.Resolution == '2x':
			scale = 2.0
		elif Scaler.Resolution == '3x':
			scale = 3.0
		else:
			raise Exception('Unkown resolution')
		
		x = int(texture.size[0] / scale)
		y = int(texture.size[1] / scale)
		
		return (x, y)

	@staticmethod
	def new_sprite(texture):
		
		#textures size is in pixels
		#convert to points and apply to sprite
		
		node = SpriteNode(texture)
		
		node.size = Scaler.size_from_texture(texture)
		
		return node

	@staticmethod
	def get_menu(tag):
		return os.path.join('Menu', Scaler.get_file('{0}.png'.format(tag)))
		
	@staticmethod
	def get_button_off(tag):
		return os.path.join('Buttons', Scaler.get_file('{0}.png'.format(tag)))

	@staticmethod
	def get_button_on(tag):
		return os.path.join('Buttons', Scaler.get_file('{0}_on.png'.format(tag)))
		
	@staticmethod
	def get_effect_path(file_name):
		return os.path.join('Effects', Scaler.get_file(file_name))

	@staticmethod
	def get_tile_path(file_name):
		return os.path.join('Tiles', Scaler.get_file(file_name))

	@staticmethod
	def get_man_frames_path(file_name):
		return os.path.join('Man', 'Frames', Scaler.get_file(file_name))

	@staticmethod
	def get_woman_frames_path(file_name):
		return os.path.join('Woman', 'Frames', Scaler.get_file(file_name))

	@staticmethod
	def get_vortex_frames_path(file_name):
		return os.path.join('Vortex', Scaler.get_file(file_name))

	@staticmethod
	def get_hearts_frames_path(file_name):
		return os.path.join('Hearts', Scaler.get_file(file_name))
		
	@staticmethod
	def get_death_path(file_name):
		return os.path.join('Man', 'Death', Scaler.get_file(file_name))

	@staticmethod
	def get_man_idle_path(file_name):
		return os.path.join('Man', 'Idle', Scaler.get_file(file_name))

	@staticmethod
	def get_woman_idle_path(file_name):
		return os.path.join('Woman', 'Idle', Scaler.get_file(file_name))
		
	@staticmethod
	def get_checkpoint_path(file_name):
		return os.path.join('CheckPoint', Scaler.get_file(file_name))

	@staticmethod
	def get_heart_path(file_name):
		return os.path.join('Heart', Scaler.get_file(file_name, force_normal=True))
	
	@staticmethod
	def get_star_path(file_name):
		return os.path.join('Star', Scaler.get_file(file_name))
		
	@staticmethod
	def get_file(file_name, force_normal=False):
		
		filter = Scaler.get_filter(force_normal)
		
		return '{0}_{1}'.format(filter, file_name)

	@staticmethod
	def get_filter(force_normal=False):
		
		if Scaler.Size not in ['Tiny','Large'] or force_normal:
			return Scaler.Resolution
		else:
			return Scaler.Size
