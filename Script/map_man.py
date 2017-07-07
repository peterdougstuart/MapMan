# coding: utf-8
import datetime
import os.path
from scene import *
import sound
import random
import math
import game_levels as levels
import tutorial
import map
import bottom_bar
import player
import controls
from game_menu import MenuScene
from score_tweet import ScoreTweet
from shake import ShakeAndTilt
from music import Music
from level_display import LevelDisplay
from lives_display import LivesDisplay

A = Action

class Game (Scene):
	
	GRADIENTS_FOLDER = 'Gradients'
	POINTS_PER_LEVEL = 10
	BONUS_POINTS = 5
	
	BASE_BG = '#71c0e2'
	REVERSE_BG = '#e28c9b'
	VANISH_BG = '#d593e2'
	STUCK_BG = '#7ce2c0'
	DEATH_BG = '#aeaeae'
	HIDDEN_BG = '#b1aaea'
	
	def setup(self):
		
		self.game_active = False
		
		self.music = Music()
		self.shake = ShakeAndTilt()
		
		self.tutorial = False
		self.started = False
		
		self.last_points_time = None
		self.last_less_time_time = None
		self.last_more_time_time = None
		self.last_life_time = None
		self.last_hide_time = None
		self.wait_until = None
		
		self.stuck = False
		self.reverse = False
		self.vanish = 0
		self.sound = 0
		
		self.background_color = Game.BASE_BG
		
		background_texture = Texture(os.path.join(Game.GRADIENTS_FOLDER, 'MapMan-background-TRANSPARENCY.png'))
		
		self.background_gradient = SpriteNode(size=self.size, position=self.size/2, parent=self)
		
		self.background_gradient.texture = background_texture

		self.level_display = LevelDisplay(parent=self)
		self.lives_display = LivesDisplay(parent=self)

		self.bottom_bar = bottom_bar.BottomBar(parent=self)
		
		self.tutorial_text = LabelNode('', font=('Avenir Next', 20), position=(self.size.w/2, self.size.h - 50), parent=self)

		self.map = map.Map(self)

		self.game_node = Node(parent=self)

		self.set_up_player()
		self.load_highscore()
		self.show_start_menu()
 	
 	def stop(self):
 		self.music.stop()
 		
	def set_background(self):
		
		if self.map.hidden:
			self.background_color = Game.HIDDEN_BG
		elif self.dead:
			self.background_color = Game.DEATH_BG
		elif self.reverse:
			self.background_color = Game.REVERSE_BG
		elif self.vanish > 0:
			self.background_color = Game.VANISH_BG
		elif self.stuck:
			self.background_color = Game.STUCK_BG
		else:
			self.background_color = Game.BASE_BG
	
	def set_controls_message(self):
		
		if self.stuck:
			self.bottom_bar.set_controls_message('Stuck, shake to release', 20)
			self.bottom_bar.effect.sticky()
		elif self.reverse and self.vanish > 0:
			self.bottom_bar.set_controls_message('Controls reversed &\nsee you again in {0} moves'.format(self.vanish), 18)
			self.bottom_bar.effect.reverse_and_vanish()
		elif self.reverse:
			self.bottom_bar.set_controls_message('Controls reversed', 20)
			self.bottom_bar.effect.reverse()
		elif self.vanish > 0:
			self.bottom_bar.set_controls_message('See you again in {0} moves'.format(self.vanish), 18)
			self.bottom_bar.effect.vanish()
		elif not self.last_points_time is None:
			self.bottom_bar.effect.points()
			self.bottom_bar.set_controls_message('Bonus Points', 20)
		elif not self.last_more_time_time is None:
			self.bottom_bar.effect.more_time()
			self.bottom_bar.set_controls_message('Extra Time', 20)
		elif not self.last_less_time_time is None:
			self.bottom_bar.effect.less_time()
			self.bottom_bar.set_controls_message('Time Lost', 20)
		elif not self.last_life_time is None:
			self.bottom_bar.effect.life()
			self.bottom_bar.set_controls_message('Extra Life', 20)
		elif not self.last_hide_time is None:
			self.bottom_bar.effect.hide()
			if self.map.hidden:
				self.bottom_bar.set_controls_message('Tiles hidden', 20)
			else:
				self.bottom_bar.set_controls_message('Tiles unhidden', 20)
		else:
			self.bottom_bar.set_controls_message('')
			self.bottom_bar.effect.clear()

	def loaded(self):
		
		if self.started:
			return
		
		self.started = True
		self.bottom_bar.timer.countdown.reset(True)
		
	def load_level(self):
		
		self.player.hide()
		
		level = self.level_display.level
		delay = 0.05
		
		if not self.tutorial:
			
			selected_levels = levels.levels
			tutorial_text = ''
			
			if level in levels.loadings:
				loading = levels.loadings[level]
			else:
				loading = None
			
			if level in levels.delays:
				delay = levels.delays[level]
				
			self.bottom_bar.timer.blank_timer()
			self.bottom_bar.set_time_message('Get Ready!!!')
						
		else:
			
			selected_levels = tutorial.levels
			tutorial_text = tutorial.descriptions[level]
			loading = None	
		self.map.load_level(selected_levels[level], loading, delay)
		
		self.tutorial_text.text = tutorial_text
		
	def update(self):
		
		if not self.game_active:
			return
		
		if self.menu is not None:
			return

		if self.started:
			
			self.move_player()
			self.update_player()
		
			self.bottom_bar.timer.update()
			self.level_display.update()
			
			time_left = self.bottom_bar.timer.countdown.seconds_remaining()
			
			self.set_time_message(time_left)
			
			if time_left < 1 and not (self.dead):
				self.lose_life()
				
			if self.dead:
				if self.player.on_last_frame():
					self.finish_lose_life()
			
		else:
			
			if self.map.loaded():
				self.loaded()

	def move_player(self):
		
		if self.dead:
			return
			
		move_time = datetime.datetime.now()
				
		show_delta = datetime.timedelta(seconds=2)
		
		if not self.last_hide_time is None:
			if (move_time - self.last_hide_time)  > show_delta:
				self.last_hide_time = None
				
		if not self.last_points_time is None:
			if (move_time - self.last_points_time)  > show_delta:
				self.last_points_time = None

		if not self.last_more_time_time is None:
			if (move_time - self.last_more_time_time)  > show_delta:
				self.last_more_time_time = None

		if not self.last_less_time_time is None:
			if (move_time - self.last_less_time_time)  > show_delta:
				self.last_less_time_time = None

		if not self.last_life_time is None:
			if (move_time - self.last_life_time)  > show_delta:
				self.last_life_time = None
			
		self.shake.update()
					
		if self.stuck:
			if self.shake.shook:
				self.stuck = False

		x_threshold = 0.1
		y_threshold = 0.1
		y_offset = 0.6
		
		stop_time = 1.0 / 60.0 * 14.0 #0.15
		wait_time = 1.0
				
		if self.map.moving:
			self.map.update_move()
			return
		else:
			can_move = self.started and (not self.stuck) 
				
		x = self.shake.g[1]
		
		if abs(x) > (2 * x_threshold):
			x_stop_time = 0.5 * stop_time
			self.wait_until = None
		elif abs(x) > (1.5 * x_threshold):
			x_stop_time = stop_time
			self.wait_until = None
		else:
			x_stop_time = stop_time
		
		y = self.shake.g[0] + y_offset
		
		if abs(y) > (2 * y_threshold):
			y_stop_time = 0.5 * stop_time
			self.wait_until = None
		elif abs(y) > (1.25 * y_threshold):
			y_stop_time = stop_time
			self.wait_until = None
		else:
			y_stop_time = stop_time

		if not self.wait_until is None:
			if move_time < self.wait_until:
				waiting = True
			else:
				waiting = False
				self.wait_until = None
		else:
			waiting = False
			
		#if waiting:
		#	return
			
		face = self.player.face_idle
		
		if x > x_threshold:
			
			if can_move:
				self.move(-1, 0, x_stop_time)
				
			if self.map.moving:
				if not self.reverse:
					self.player.face_left()
				else:
					self.player.face_right()
				self.wait_until = self.map.start_move + datetime.timedelta(seconds=(x_stop_time + wait_time))
				return
			else:
				if not self.reverse:
					face = self.player.face_left_idle
				else:
					face = self.player.face_right_idle
				
		elif x < -x_threshold:
			
			if can_move:
				self.move(1, 0, x_stop_time)
			
			if self.map.moving:
				if not self.reverse:
					self.player.face_right()
				else:
					self.player.face_left()
				self.wait_until = self.map.start_move + datetime.timedelta(seconds=(x_stop_time + wait_time))
				return
			else:
				if not self.reverse:
					face = self.player.face_right_idle
				else:
					face = self.player.face_left_idle
			
		if y > y_threshold:
			
			if can_move:
				self.move(0, 1, y_stop_time)
			
			if self.map.moving:
				if not self.reverse:
					self.player.face_up()
				else:
					self.player.face_down()
				self.wait_until = self.map.start_move + datetime.timedelta(seconds=(y_stop_time + wait_time))
				return
			else:
				if not self.reverse:
					face = self.player.face_up_idle
				else:
					face = self.player.face_down_idle
				
		elif y < -y_threshold:
			
			if can_move:
				self.move(0, -1, y_stop_time)
			
			if self.map.moving:
				if not self.reverse:
					self.player.face_down()
				else:
					self.player.face_up()
				self.wait_until = self.map.start_move + datetime.timedelta(seconds=(y_stop_time + wait_time))
				return
			else:
				if not self.reverse:
					face = self.player.face_down_idle
				else:
					face = self.player.face_up_idle
					
		face()
			
	def set_time_message(self, time_left):
		
		if self.tutorial:
			self.bottom_bar.set_time_message('')
		elif time_left > 18:
			self.bottom_bar.set_time_message('Go!!!')
		elif time_left < 5:
			self.bottom_bar.set_time_message('Hurry Up!!!')
			self.background_gradient.texture = None
		elif time_left < 0:
			self.bottom_bar.set_time_message('Time Up!!!')
		else:
			self.bottom_bar.set_time_message('')
				
	def reset_all(self):
		
			self.map.reset()
			self.dead = False
			self.reverse = False
			self.stuck = False
			self.map.clear_reverse()
			self.map.clear_hide()
			self.map.unhide()
			self.bottom_bar.effect.clear()
			self.bottom_bar.set_controls_message('')
			self.vanish = 0
			self.started = False
			self.set_background()
			self.bottom_bar.timer.update()
			self.level_display.update()
		
	def update_player(self):
			
			self.update_player_location()
			
			if self.map.moving:
				return
				
			if self.map.at_end():
				self.advance_level()
				return
			
			if self.map.on_reverse():
				sound.play_effect('game:Boing_1')
				self.reverse = not self.reverse
				self.map.clear_reverse()
				
			if self.vanish > 0:
				self.player.vanish()
			else:
				self.player.show()
				
			if self.map.on_vanish():
				sound.play_effect('game:Spaceship')
				self.vanish = self.map.vanish_duration()
				self.map.clear_vanish()
				self.player.vanish()

			if self.map.on_hide():
				sound.play_effect('game:Spaceship')
				self.map.clear_hide()
				self.map.toggle_hide()
				self.last_points_time = None
				self.last_more_time_time = None
				self.last_less_time_time = None
				self.last_life_time = None
				self.last_hide_time = datetime.datetime.now()
				
			if self.map.on_points():
				sound.play_effect('rpg:HandleCoins')
				self.map.clear_points()
				if not self.tutorial:
					self.level_display.score += Game.BONUS_POINTS
				self.last_points_time = datetime.datetime.now()
				self.last_more_time_time = None
				self.last_less_time_time = None
				self.last_life_time = None
				self.last_hide_time = None
				
			if self.map.on_death() and not self.dead:
				self.map.clear_death()
				self.lose_life()

			if self.map.on_life():
				
				sound.play_effect('game:Bleep')
				self.map.clear_life()
				
				if not self.tutorial:
					self.lives_display.lives += 1

				self.last_hide_time = None
				self.last_points_time = None
				self.last_less_time_time = None
				self.last_more_time_time = None
				self.last_life_time = datetime.datetime.now()
				self.lives_display.update()

			if self.map.on_sticky():
				sound.play_effect('game:Error')
				self.map.clear_sticky()
				self.stuck = True
				
			if self.map.on_more_time():
				self.map.clear_more_time()
				self.bottom_bar.timer.countdown.add_time(5)

				self.last_hide_time = None
				self.last_more_time_time = datetime.datetime.now()
				self.last_points_time = None
				self.last_less_time_time = None
				self.last_life_time = None
				
			if self.map.on_less_time():
				self.map.clear_less_time()
				self.bottom_bar.timer.countdown.add_time(-5)
				self.last_hide_time = None
				self.last_less_time_time = datetime.datetime.now()
				self.last_more_time_time = None
				self.last_points_time = None
				self.last_life_time = None
			
			self.set_background()
			self.set_controls_message()
	
	def update_player_location(self):
		self.player.update(self.map.get_position())

	def advance_level(self):
		
		sound.play_effect('rpg:DoorClose_1')
		self.show_level_complete()
	
	def next_level(self):
		
		if not self.tutorial:
			self.level_display.score += self.end_of_level_points
		
		self.level_display.advance_level()
		self.bottom_bar.timer.advance_level()
		self.lives_display.update() #to ensure lives display when entering game from turorial
		
		self.load_level()
		self.reset_all()
				
	def move(self, step_x, step_y, move_seconds):
		
		if self.map.moving:
			raise Exception('Player already moving')
			
		if not self.reverse:
			self.map.move(step_x, step_y, move_seconds)
		else:
			self.map.move(-step_x, -step_y, move_seconds)
		
		if self.map.moving:
			
			if self.sound == 0:
				self.sound = 1
			else:
				self.sound = 0
			
			sound.play_effect('rpg:Footstep00', 0.4, 1.0 + 0.5 * self.sound)
				
			if self.vanish > 0:
				self.vanish -= 1

	def set_up_player(self):
		self.player = player.Player(self)
		
	def show_start_menu(self):
		
		self.music.play_menu()
		
		self.menu = MenuScene('Map Man', 'Your Personal Best: {0}'.format(self.highscore), ['Play', 'Tutorial', 'Credits'])
		self.present_modal_scene(self.menu)
		
	def load_highscore(self):
		try:
			with open('.map_man_highscore', 'r') as f:
				self.highscore = int(f.read())
		except:
			self.highscore = 0

	def menu_button_selected(self, title):
		
		if title in ['Play','New Game']:
			self.dismiss_modal_scene()
			self.menu = None
			self.new_game()
		elif title == 'Tutorial':
			self.dismiss_modal_scene()
			self.menu = None
			self.new_tutorial()
		elif title == 'Credits':
			self.show_credits()
		elif title == 'Tweet PB':
			ScoreTweet(self.highscore)
			self.dismiss_modal_scene()
			self.show_start_menu()
		elif title == 'Main Menu':
			self.dismiss_modal_scene()
			self.show_start_menu()
		elif title == 'Next Level':
			self.next_level()
			self.menu = None
			self.dismiss_modal_scene()
				
	def show_credits(self):
		
		self.menu = MenuScene('Map Man','Coding by Peter Stuart\nGraphics by Fred Mangan\nMusic by David Sedgwick\n', ['Main Menu'], 12)
		self.present_modal_scene(self.menu)

	def show_level_complete(self):
		
		self.started = False
		
		if not self.tutorial:
			
			time_bonus = self.bottom_bar.timer.countdown.seconds_remaining()
		
			self.end_of_level_points = Game.POINTS_PER_LEVEL + time_bonus
		
			self.menu = MenuScene('Complete','Level Bonus {0}\nTime Bonus {1}\n '.format(Game.POINTS_PER_LEVEL, time_bonus), ['Next Level'])
			self.present_modal_scene(self.menu)
		
		else:
			
			self.next_level()
		
	def new_game(self, tutorial=False):
		
		self.music.play_game()
		
		self.shake.start()
		self.game_active = True
		
		self.tutorial = tutorial
		self.level_display.reset()
		self.load_level()
		self.reset_all()
		self.lives_display.reset()
	
	def new_tutorial(self):
		self.new_game(True)
		
	def save_highscore(self):
		
		with open('.map_man_highscore', 'w') as f:
			f.write(str(self.highscore))

	def lose_life(self):
		sound.play_effect('arcade:Explosion_2')
		self.player.face_death()
		self.dead = True
	
	def finish_lose_life(self):
		
		if not self.tutorial:
			self.lives_display.lives -= 1
		
		if self.lives_display.lives < 1:
			self.game_over()
		else:
			self.reset_all()
			
		self.lives_display.update()
			
	def game_over(self):
		
		self.music.play_end()
		self.game_active = True
		self.shake.stop()
		
		options = ['New Game','Main Menu']
		
		if self.level_display.score > self.highscore:
			self.highscore = self.level_display.score
			self.save_highscore()
			options.append('Tweet PB')
			text = 'New Personal Best: {0}'.format(self.highscore)
		else:
			text = 'Score: {0}'.format(self.level_display.score)
			
		self.menu = MenuScene('Game Over', text, options)
		self.present_modal_scene(self.menu)
	
if __name__ == '__main__':
	run(Game(), LANDSCAPE, show_fps=False)
