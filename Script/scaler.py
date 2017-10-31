import os.path
import scene

class Scaler (object):
	
	Player = None
	Size = None
	Resolution = None
	Font = None
	Bottom_bar = None
	Menu = None
	Timer = None
	Effect = None
	Score = None
	
	@staticmethod
	def initialize(game):
		
		if game.size.w >= 1024:
			
			#iPad
			Scaler.Size = 'Large'
			Scaler.Tile_size_x = 64
			Scaler.Tile_size_y = 46
			
			Scaler.Player = 1
			Scaler.Bottom_bar = 2
			Scaler.Timer = 2
			Scaler.Effect = 1
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
				raise Exception('Unsupported resolution')
			
			#iPhone 5, 6, 7
			Scaler.Size = 'Small'
			Scaler.Tile_size_x = 32
			Scaler.Tile_size_y = 23
			
			Scaler.Player = 1
			Scaler.Bottom_bar = 1
			Scaler.Timer = 1
			Scaler.Effect = 1
			Scaler.Menu = 1
			Scaler.Score = 1
		
			if game.size.w < 667:
				
				#iphone 4 and below
				reduce = 0.8

				Scaler.Tile_size_x = 28
				Scaler.Tile_size_y = 20
			
				Scaler.Player *= reduce
				Scaler.Menu *= reduce
				
				#keep bottom bar same size
				#keep score the same size
	
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
		return os.path.join('Heart', Scaler.get_file(file_name))
		
	@staticmethod
	def get_file(file_name):
		
		if Scaler.Size == 'Large':
			return '{0}_{1}'.format(Scaler.Size, file_name)
		else:
			return '{0}_{1}'.format(Scaler.Resolution, file_name)
			
