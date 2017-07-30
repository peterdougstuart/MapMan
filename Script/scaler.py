import os.path

class Scaler (object):
	
	Scale = None
	
	@staticmethod
	def initialize(game):
		
		if game.size.w > 760:
			#iPad
			Scaler.scale = 2
		else:
			#iPhone
			Scaler.scale = 1
			
	@staticmethod
	def get_scale():
		
		if Scaler.scale is None:
			raise Exception('Not initialised.')
			
		return Scaler.scale
	
	@staticmethod
	def get_effect_path(file_name):
		
		return os.path.join('Effects', Scaler.get_scale_folder(), file_name)

	@staticmethod
	def get_tile_path(file_name):
		
		return os.path.join('Tiles', '{0}{1}'.format(Scaler.get_scale_prefix(), file_name))

	@staticmethod
	def get_man_frames_path(file_name):
		
		return os.path.join('Man', 'Frames', Scaler.get_scale_folder(), file_name)

	@staticmethod
	def get_man_death_path(file_name):
		
		return os.path.join('Man', 'Death', Scaler.get_scale_folder(), file_name)

	@staticmethod
	def get_man_idle_path(file_name):
		
		return os.path.join('Man', 'Idle', Scalere.get_scale_folder(), file_name)

	@staticmethod
	def get_scale_prefix():
		return '{0}_'.format(Scaler.get_scale_folder())
		
	@staticmethod
	def get_scale_folder():
		
		if Scaler.scale == 1.0:
			return '1x'
		elif Scaler.scale == 2.0:
			return '2x'
		else:
			raise Exception('Cannot locate folder for scale: {0}'.format(Scaler.scale))
