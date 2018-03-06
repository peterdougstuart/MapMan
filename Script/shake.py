import math
from scene import gravity
import motion

class ShakeAndTilt:
	
	def __init__(self):
		
		self.g = None
		self.shook = False
		self.active = False
			
	def start(self):
		
		if self.active:
			raise Exception('Cant start, already started')
			
		motion.start_updates()
		self.active = True
		
	def stop(self):

		if not self.active:
			raise Exception('Cant stop, not started')
			
		motion.stop_updates()
		self.active = False
		
	def update(self):
		
		if not self.active:
			raise Exception('Cant update, not started')
			
		self.g = motion.get_gravity()
		
		ua = motion.get_user_acceleration()
		
		scale = 100
		ux = ua[0] * scale
		uy = ua[1] * scale
		uz = ua[2] * scale
		
		shake = math.sqrt(ux*ux+uy*uy+uz*uz)
				
		if shake > 40.0:
			self.shook = True
		else:
			self.shook = False

