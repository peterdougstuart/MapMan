import sound
import os.path

class FX (object):
	
	def __init__(self, enabled):
		self.enabled = enabled
		self.sound = 0
		self.clock_player = sound.Player(os.path.join('SoundEffects','clock.caf'))
		self.clock_player.number_of_loops = -1
		self.playing_clock = False
	
	def play_clock(self):
		if self.enabled:
			self.playing_clock = True
			self.clock_player.play()
	
	def stop_clock(self):
		if self.playing_clock:
			self.clock_player.stop()
			
	def play_love(self):
		
		if self.enabled:
			sound.play_effect(os.path.join('SoundEffects','love.caf'))
	
	def play_reverse(self):
		
		if self.enabled:
			sound.play_effect('game:Boing_1')
	
	def play_vanish(self):
		
		if self.enabled:
			sound.play_effect('game:Spaceship')
	
	def play_hide(self):
		
		if self.enabled:
			sound.play_effect('game:Spaceship')
	
	def play_points(self):
		
		if self.enabled:
			sound.play_effect('rpg:HandleCoins')
	
	def play_life(self):
		
		if self.enabled:
			sound.play_effect('game:Bleep')
	
	def play_sticky(self):
		
		if self.enabled:
			sound.play_effect('game:Error')
	
	def play_lose_life(self):
		
		if self.enabled:
			sound.play_effect(os.path.join('SoundEffects','pop.caf'))
	
	def play_end_level(self):
		
		if self.enabled:
			
			sound.play_effect('rpg:DoorClose_1')
	
	def play_check_point(self):
		
		if self.enabled:
			sound.play_effect(os.path.join('SoundEffects','checkpoint.caf'))
	
	def play_step(self):
		
		if self.enabled:

			if self.sound == 0:
				self.sound = 1
			else:
				self.sound = 0

			sound.play_effect('rpg:Footstep00', 0.4, 1.0 + 0.5 * self.sound)
	
	def play_star(self):
		
		if self.enabled:
			sound.play_effect('game:Ding_3', 0.2)
			
	def enable(self):
		self.enabled = True
	
	def disable(self):
		self.enabled = False
