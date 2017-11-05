import os.path
import scene
from scene import SpriteNode

class Scaler (object):
	
	Resolution = None
	Bottom_bar = None
	Menu = None
	Timer = None
	Score = None
	
	@staticmethod
	def initialize(game):
		
		if game.size.w >= 1024:
			
			#iPad
			Scaler.Size = 'Large'

			Scaler.Bottom_bar = 2
			Scaler.Timer = 2
			Scaler.Menu = 2
			Scaler.Score = 1
			
			Scaler.Resolution = '2x'
			
		else:
			
			#iphone
			if scene.get_screen_scale() == 1.0:
				Scaler.Resolution = '1x'
			elif scene.get_screen_scale() == 2.0:
				Scaler.Resolution = '2x'
			elif scene.get_screen_scale() >= 3.0:
				Scaler.Resolution = '3x'
			else:
				Scaler.Resolution = '3x'
		
			if game.size.w < 667:
				
				if Scaler.Resolution == '1x':
					Scaler.Size = 'Tiny'
				else:
					Scaler.Size = 'Small'
				
				#iphone 4 and below
				Scaler.Bottom_bar = 1
				Scaler.Timer = 1
				Scaler.Menu = 0.8
				Scaler.Score = 1			

			else:
				
				#iPhone 5, 6, 7
				Scaler.Size = 'Normal'
			
				Scaler.Bottom_bar = 1
				Scaler.Timer = 1
				Scaler.Menu = 1
				Scaler.Score = 1
	
	@staticmethod
	def new_sprite(texture):
		
		#textures size is in pixels
		#convert to points and apply to sprite
		
		node = SpriteNode(texture)
		
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
		
		node.size = (x, y)
		
		return node
		
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
	def get_death_path(file_name):
		return os.path.join('Man', 'Death', Scaler.get_file(file_name))

	@staticmethod
	def get_idle_path(file_name):
		return os.path.join('Man', 'Idle', Scaler.get_file(file_name))

	@staticmethod
	def get_checkpoint_path(file_name):
		return os.path.join('CheckPoint', Scaler.get_file(file_name))

	@staticmethod
	def get_heart_path(file_name):
		return os.path.join('Heart', Scaler.get_file(file_name, force_normal=True))
		
	@staticmethod
	def get_file(file_name, force_normal=False):
		
		if Scaler.Size not in ['Tiny','Large'] or force_normal:
			return '{0}_{1}'.format(Scaler.Resolution, file_name)
		else:
			return '{0}_{1}'.format(Scaler.Size, file_name)
			
			
