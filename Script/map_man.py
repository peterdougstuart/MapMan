# coding: utf-8
import datetime
import os
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
import sys
import time
from timer import Timer

from game_menu import PauseMenu
from game_menu import CreditsMenu
from game_menu import MainMenu
from game_menu import EndGameMenu
from game_menu import EndLevelMenu
from game_menu import LoseLifeMenu
from game_menu import RestartMenu
from game_menu import PurchaseMenu
from game_menu import FirstPlayMenu
from game_menu import ConfirmProductMenu
from game_menu import MakePurchaseMenu
from game_menu import PurchaseToPlayMenu
from game_menu import PurchaseToCheckpointMenu

from score_tweet import ScoreTweet
from shake import ShakeAndTilt
from music import Music
from level_display import LevelDisplay
from lives_display import LivesDisplay
from points_display import PointsDisplay
from gradient import Gradient
from scaler import Scaler
from in_app import InApp
from products_controller import ProductsController

import palette

A = Action

class SimulatedTilt (object):
	
	def __init__(self, size, touch):
		
		x, y = touch.location
		threshold_3 = 0.11
		threshold_4 = 0.5
		
		if y < (size.h / 4):
			self.y = -threshold_4
		elif y < (size.h / 3):
			self.y = -threshold_3
		elif y > (3 * size.h / 4):
			self.y = threshold_4
		elif y > (2 * size.h / 3):
			self.y = threshold_3
		else:
			self.y = 0

		if x < (size.w / 4):
			self.x = threshold_4
		elif x < (size.w / 3):
			self.x = threshold_3
		elif x > (3 * size.w / 4):
			self.x = -threshold_4
		elif x > (2 * size.w / 3):
			self.x = -threshold_3
		else:
			self.x = 0
		
class CheckPointInfo (object):
	
	def __init__(self, level):
		self.level = level
		self.score = None
		self.complete = False
	
	def set_complete(self, score):
		
		self.complete = True
		
		if self.score is None:
			self.score = score
		elif score > self.score:
			self.score = score
		
class Game (Scene):
	
	POINTS_PER_LEVEL = 10
	SIMULATE_TILT = 'simulate_tilt.txt'
	
	def __init__(self):
		self.set_up_complete = False
		Scene.__init__(self)
		
	def load_simulated(self):
		
		if not os.path.isfile(Game.SIMULATE_TILT):
			self.simulate_tilt = False
			return
			
		try:
			with open(Game.SIMULATE_TILT, 'r') as f:
				text = f.read().lower().strip()
				if text == 'simulate':
					self.simulate_tilt = True
					Timer.INITIAL_SECONDS = 99
				else:
					self.simulate_tilt = False
		except:
			self.simulate_tilt = False
		
	def setup(self):

		self.purchase_to_play = False
		self.purchase_to_continue = False
		self.game_active = False
		self.paused = False
		
		self.set_background()
		self.load_first_play()
		
		self.simulated_tilt = None
		self.load_simulated()

		Scaler.initialize(self)
		
		self.music = Music()
		self.shake = ShakeAndTilt()
		
		self.tutorial = False
		
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
		self.stars = 0
		
		self.bottom_bar = bottom_bar.BottomBar(parent=self)
		self.bottom_bar.hide()
		
		self.level_display = LevelDisplay(parent=self)
		self.lives_display = LivesDisplay(parent=self)
		self.points_display = PointsDisplay(parent=self)
		
		#self.game_node = Node(parent=self)
		self.map = map.Map(self)
		
		self.set_up_player()
		self.load_highscore()
		self.load_continues()
		self.load_check_points()
		self.show_start_menu()
		
		self.set_up_complete = True
		
	def stop(self):
		self.music.stop()

	def set_background(self):
		
		if not self.game_active:
			self.background_color = palette.BASE_BG
		elif self.map.hidden:
			self.background_color = palette.HIDDEN_BG
		elif self.dead:
			self.background_color = palette.DEATH_BG
		elif self.reverse:
			self.background_color = palette.REVERSE_BG
		elif self.vanish > 0:
			self.background_color = palette.VANISH_BG
		elif self.stuck:
			self.background_color = palette.STUCK_BG
		else:
			self.background_color = palette.BASE_BG
	
	def set_controls_message(self):
		
		if not self.last_points_time is None:
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
		elif self.stuck:
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
			
		elif not self.last_hide_time is None:
			
			if self.map.hidden:
				self.bottom_bar.effect.hide()
				self.bottom_bar.set_controls_message('Tiles hidden', 20)
			else:
				self.bottom_bar.effect.unhide()
				self.bottom_bar.set_controls_message('Tiles unhidden', 20)
				
		else:
			self.bottom_bar.set_controls_message('')
			self.bottom_bar.effect.clear()

	def loaded(self):
		
		if self.started():
			return
		
		self.update_player_location()
		self.player.show()
		
		if not self.tutorial:
			self.bottom_bar.timer.start()
	
	def started(self):
		
		if self.tutorial:
			return self.map.loaded()
		else:
			return self.bottom_bar.timer.active()
		
	def load_level(self):
		
		self.bottom_bar.timer.stop()
		self.bottom_bar.timer.reset()
		self.bottom_bar.timer.show()
		
		self.player.hide()
		
		level = self.level_display.level
		delay = levels.DEFAULT_DELAY
		
		if not self.tutorial:
			
			selected_levels = levels.levels
			
			if level in levels.loadings:
				loading = levels.loadings[level]
			else:
				loading = None
			
			if level in levels.delays:
				delay = levels.delays[level]
			
			if level in levels.check_points:
				check_point = True
			else:
				check_point = False
			
			self.bottom_bar.timer.blank()
			self.bottom_bar.set_time_message('get ready...')
			
			self.bottom_bar.set_tutorial_text('')
			
			if level in levels.x_hides:
				x_hides = levels.x_hides[level]
			else:
				x_hides = levels.DEFAULT_X_HIDES
				
		else:
			
			selected_levels = tutorial.levels
			loading = None
			check_point = False
			self.bottom_bar.set_tutorial_text(tutorial.descriptions[level])
			
			x_hides = levels.DEFAULT_X_HIDES
		self.map.load_level(selected_levels[level], loading, delay, check_point, x_hides)
		
	def update(self):
			
		if not self.set_up_complete:
			return
			
		self.bottom_bar.timer.update()
		self.music.restart()
		
		if not self.game_active:
			return
		
		if self.menu is not None:
			return

		if self.dead:
			
			self.update_player()
			
			if self.player.on_last_frame():
				self.finish_lose_life()
				
		elif self.started():
			
			self.move_player()
			self.update_player()
		
			self.level_display.update()
			self.points_display.update()
			
			time_left = self.bottom_bar.timer.seconds_remaining()
			
			self.set_time_message(time_left)
			
			if time_left < 1 and not (self.dead):
				self.lose_life()
			
		else:
			
			if self.map.loaded():
				self.loaded()

	def touch_began(self, touch):
		
		if not self.simulate_tilt:
				return
		else:
			self.simulated_tilt = SimulatedTilt(self.size, touch)

	def touch_ended(self, touch):

		if not self.simulate_tilt: 
			if self.paused:
				return
			else:
				if (not self.dead) and (self.bottom_bar.timer.seconds_remaining() <= 19 or self.tutorial):
					self.show_pause_menu()
		else:
			self.simulated_tilt = None 
		
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
			if not self.simulate_tilt:
				if self.shake.shook:
					self.stuck = False
			else:
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
			can_move = self.started() and (not self.stuck) 
		
		if self.simulate_tilt:
			if self.simulated_tilt is None:
				x = 0
				y = 0
			else:
				x = self.simulated_tilt.x
				y = self.simulated_tilt.y
		else:
			y = self.shake.g[0] + y_offset
			x = self.shake.g[1]
			
		if abs(x) > (2 * x_threshold):
			x_stop_time = 0.5 * stop_time
			self.wait_until = None
		elif abs(x) > (1.5 * x_threshold):
			x_stop_time = stop_time
			self.wait_until = None
		else:
			x_stop_time = stop_time

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
		elif time_left > 19:
			self.bottom_bar.set_time_message('go!')
		elif self.bottom_bar.timer.low_time:
			self.bottom_bar.set_time_message('hurry up!')
		elif time_left < 0:
			self.bottom_bar.set_time_message('time up!')
		elif time_left > 15 and self.level_display.level in levels.level_messages and not self.tutorial:
			message = levels.level_messages[self.level_display.level]
			self.bottom_bar.set_time_message(message)
		else:
			self.bottom_bar.set_time_message('')

	def use_continue(self):
		
		if self.continues < 1:
			return
			
		self.continues -= 1
		self.save_contiues()
		self.new_game(level=self.level_display.level)
		
	def reset_all(self, reset_stars=True):
			
			if reset_stars:
				self.stars = 0
			
			self.map.reset()
			self.dead = False
			self.reverse = False
			self.stuck = False
			self.map.clear_reverse()
			self.map.clear_hide()
			self.map.reset_hide()
			self.bottom_bar.timer.reset()
			self.bottom_bar.effect.clear()
			self.bottom_bar.set_controls_message('')
			self.vanish = 0

			self.set_background()
			self.bottom_bar.timer.update()
			self.level_display.update()
			self.points_display.update()
			
			self.simulated_tilt = None
		
	def update_player(self):
			
			self.update_player_location()
			
			if self.map.moving:
				return
				
			if self.map.at_end():
				self.advance_level(self.map.check_point)
				return
			
			if self.map.on_reverse():
				sound.play_effect('game:Boing_1')
				self.reverse = not self.reverse
				self.map.clear_reverse()
				
			if self.vanish > 0 and not self.dead:
				self.player.vanish()
			else:
				self.player.show()
				
			if self.map.on_vanish():
				sound.play_effect('game:Spaceship')
				self.vanish = self.map.vanish_duration()
				self.map.clear_vanish()
				self.player.vanish()

			if self.map.on_hide() or self.map.on_unhide():
				
				sound.play_effect('game:Spaceship')
				
				if self.map.on_hide():
					self.map.clear_hide()
					self.map.hide()
				elif self.map.on_unhide():
					self.map.clear_unhide()
					self.map.unhide()
					
				self.last_points_time = None
				self.last_more_time_time = None
				self.last_less_time_time = None
				self.last_life_time = None
				self.last_hide_time = datetime.datetime.now()
				
			if self.map.on_points():
				sound.play_effect('rpg:HandleCoins')
				self.map.clear_points()
				
				if not self.tutorial:
					self.stars += 1
					
				self.last_points_time = datetime.datetime.now()
				self.last_more_time_time = None
				self.last_less_time_time = None
				self.last_life_time = None
				self.last_hide_time = None
				
			if self.map.on_death() and not self.dead:
				self.map.tiles[self.map.position].unhide()
				
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

	def advance_level(self, check_point):
		
		self.bottom_bar.timer.stop()
		
		if not check_point:
			sound.play_effect('rpg:DoorClose_1')
		else:
			self.music.pause(datetime.timedelta(seconds=3))
			sound.play_effect(os.path.join('SoundEffects','checkpoint.caf'))
			
		self.show_level_complete(check_point)
	
	def next_level(self):
		
		if not self.tutorial:
			
			self.points_display.score += self.end_of_level_points

			if self.map.check_point:
				
				check_point = CheckPointInfo(self.level_display.level)
				check_point.set_complete(self.points_display.score)
				
				self.check_points[check_point.level] = check_point
				
				self.save_check_points()
		
		self.level_display.advance_level()
		
		if not self.can_play_level():
			self.show_purchase_to_play_menu()
		else:
			self.finish_advancing_level()

	def finish_advancing_level(self):
		
		if not self.tutorial:
			number_of_levels = len(levels.levels)
		else:
			number_of_levels = len(tutorial.levels)
			
		if self.level_display.level > number_of_levels:
			
			if self.tutorial:
				self.tutorial = False
				self.level_display.level = 1
				self.lives_display.update()
			else:
				self.level_display.level = 1
		
		self.bottom_bar.timer.stop()
		
		self.load_level()
		self.reset_all()
	
	def can_play_level(self):
		
		level = self.level_display.level
		pc = ProductsController.get()
		
		if level <= 25:
			return True
		elif level >= 26 and level <= 50 and pc.l26_l50.purchased:
			return True
		elif level >= 51 and level <= 75 and pc.l51_l75.purchased:
			return True
		elif level >= 76 and level <= 100 and pc.l76_l100.purchased:
			return True
		else:
			return False
		
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
	
	def show_purchase_to_play_menu(self):
		
		self.bottom_bar.hide()
		self.player.hide()
		self.map.unload()
		self.level_display.hide()
		self.points_display.hide()
		self.lives_display.hide()
		
		self.bottom_bar.timer.stop()
	
		self.purchase_to_play = True
		self.menu = PurchaseToPlayMenu()
		self.present_modal_scene(self.menu)

	def show_purchase_to_checkpoint_menu(self):
		self.menu = PurchaseToCheckpointMenu()
		self.present_modal_scene(self.menu)
	
	def can_use_checkpoints(self):
		return ProductsController.get().checkpoints.purchased

	def show_pause_menu(self):
		
		self.bottom_bar.timer.stop()
		self.paused = True
		self.menu = PauseMenu(self.tutorial)
		self.present_modal_scene(self.menu)
		
	def show_start_menu(self):
		
		self.music.play_menu()
		
		self.menu = MainMenu(self.highscore, self.continues)
		self.present_modal_scene(self.menu)
		
	def show_restart_menu(self):
		
		self.music.play_menu()
		self.menu = RestartMenu(self.check_points)
		self.present_modal_scene(self.menu)

	def load_first_play(self):
		try:
			with open('.map_man_first_play', 'r') as f:
				self.first_play = False
		except:
			self.first_play = True

	def save_first_play(self):
		
		if not self.first_play:
			return
			
		with open('.map_man_first_play', 'w') as f:
			f.write(str(datetime.datetime.now()))
			
		self.first_play = False
			
	def load_highscore(self):
		try:
			with open('.map_man_highscore', 'r') as f:
				self.highscore = int(f.read())
		except:
			self.highscore = 0

	def load_continues(self):
		try:
			with open('.continues', 'r') as f:
				self.continues = int(f.read())
		except:
			self.continues = 0
			
	def load_check_points(self):
		
		self.check_points = {}
			
		for level in levels.check_points:
			check_point = CheckPointInfo(level)
			self.check_points[level] = check_point
		
		try:
			
			with open('.map_man_check_point', 'r') as f:
				
				for line in f.readlines():
					
					data = line.split(',')
				
					level = int(data[0])
					score = int(data[1])
				
					if level in self.check_points:
						check_point = self.check_points[level]
						check_point.set_complete(score)
				
		except:
			
			pass
	
	def add_continue(self, number=1):
		self.continues += number
		self.save_contiues()
		
	def purchase_product(self, product):
		
		self.dismiss_modal_scene()
		
		self.menu = MakePurchaseMenu(product, purchase_to_play=self.purchase_to_play, purchase_to_continue=self.purchase_to_continue,
		add_continue=self.add_continue)
		
		self.present_modal_scene(self.menu)
		
	def product_selected(self, product):
		
		self.dismiss_modal_scene()
		self.menu = ConfirmProductMenu(product)
		self.present_modal_scene(self.menu)
	
	def menu_button_selected(self, title):
		
		title = title.lower()
		
		
		if title in ['play','new game', 'play game','play from start']:
			
			self.dismiss_modal_scene()
			
			if self.first_play and title != 'play game':
				self.show_first_play()
			else:
				self.menu = None
				self.new_game()
				
		elif title in ['resume', 'resume game']:
			
			if self.can_play_level():
				self.dismiss_modal_scene()
				self.menu = None
				self.purchase_to_play = False
				self.purchase_to_continue = False
				self.bottom_bar.show()
				self.lives_display.show()
				self.points_display.show()
				self.level_display.show()
				self.bottom_bar.timer.start()
				self.finish_advancing_level()
			else:
				self.dismiss_modal_scene()
				self.show_purchase_to_play_menu()
			
		elif title == 'restart from checkpoint':
			self.dismiss_modal_scene()
			self.show_restart_menu()
		elif len(title) == 3 and title[0] == 'l':
			
			if self.can_use_checkpoints():
				
				self.dismiss_modal_scene()
				self.menu = None
				data = title.replace('l','')
				level = int(data)
				self.new_game(level=level)
				
			else:
				self.show_purchase_to_checkpoint_menu()
				
		elif title in ['tutorial', 'take tutorial']:
			self.dismiss_modal_scene()
			self.menu = None
			self.new_tutorial()
		elif title == 'credits':
			self.show_credits()
		elif title in ['purchase', 'purchase menu', 'okay']:
			self.show_purchase()
		elif title == 'tweet pb':
			ScoreTweet(self.highscore)
			self.menu.remove_tweet_pb()
		elif title in ['main menu', 'main menu (end game)']:
			self.purchase_to_play = False
			self.purchase_to_continue = False
			self.dismiss_modal_scene()
			self.show_start_menu()
		elif title in ['end game','end tutorial']:
			self.purchase_to_play = False
			self.purchase_to_continue = False
			self.paused = False
			self.game_over(False)
			self.dismiss_modal_scene()
			self.show_start_menu()
		elif title in ['next level','play next level']:
			self.menu = None
			self.dismiss_modal_scene()
			self.next_level()
		elif title == 'try again':
			self.reset_all(False)
			self.menu = None
			self.dismiss_modal_scene()
		elif title == 'use continue':
			self.purchase_to_continue = False
			self.use_continue()
			self.menu = None
			self.dismiss_modal_scene()
		elif title == 'purchase continue':
			self.show_purchase_to_continue()
		elif title == 'unpause':
			self.bottom_bar.timer.start()
			self.menu = None
			self.paused = False
			self.dismiss_modal_scene()
		
	def show_first_play(self):
		
		self.menu = FirstPlayMenu()
		self.present_modal_scene(self.menu)
		
	def show_credits(self):
		
		self.menu = CreditsMenu()
		self.present_modal_scene(self.menu)

	def show_purchase(self):
		
		self.menu = PurchaseMenu(purchase_to_play=self.purchase_to_play, purchase_to_continue=self.purchase_to_continue)
		self.present_modal_scene(self.menu)
		
	def show_purchase_to_continue(self):
		
		self.purchase_to_continue = True
		self.show_purchase()
		
	def show_level_complete(self, check_point):
		
		self.bottom_bar.timer.stop()
		
		if not self.tutorial:
			
			time_bonus = int(round(self.bottom_bar.timer.seconds_remaining() / 2, 0))
		
			self.end_of_level_points = Game.POINTS_PER_LEVEL + time_bonus + self.stars

			self.menu = EndLevelMenu(self.level_display.level, self.points_display.score, Game.POINTS_PER_LEVEL, time_bonus, self.stars, check_point)
			
			self.present_modal_scene(self.menu)
		
		else:
			
			self.next_level()
		
	def new_game(self, level=None, tutorial=False):
		
		self.save_first_play()
		
		if level is None:
			level = levels.START_LEVEL
			
		self.music.play_game()
		
		self.shake.start()
		
		self.tutorial = tutorial
		self.points_display.reset()
		self.level_display.reset()
		self.level_display.level = level
		self.load_level()
		self.reset_all()
		self.lives_display.reset()
		self.game_active = True

		self.level_display.show()
		self.points_display.show()
		self.lives_display.show()
		
		self.bottom_bar.show()
		
		if self.tutorial:
			self.bottom_bar.timer.hide()
		else:
			self.bottom_bar.timer.show()
	
	def new_tutorial(self):
		self.new_game(tutorial=True)
		
	def save_highscore(self):
		
		with open('.map_man_highscore', 'w') as f:
			f.write(str(self.highscore))

	def save_contiues(self):
		
		with open('.continues', 'w') as f:
			f.write(str(self.continues))
			
	def save_check_points(self):
		
		with open('.map_man_check_point', 'w') as f:
			
			for level in sorted(self.check_points):
				
				check_point = self.check_points[level]
				
				if check_point.complete:
					f.write('{0},{1}\n'.format(check_point.level, check_point.score))
			
	def lose_life(self):
		self.bottom_bar.timer.stop()
		sound.play_effect(os.path.join('SoundEffects','pop.caf'))
		self.player.show()
		self.player.face_death()
		self.dead = True
	
	def finish_lose_life(self):

		if not self.tutorial:
			self.lives_display.lives -= 1
		
		self.lives_display.update()
				
		if self.lives_display.lives < 1:
			self.game_over()
		else:
			if not self.tutorial:
				self.menu = LoseLifeMenu(self.lives_display.lives)
				self.present_modal_scene(self.menu)
			else:
				self.reset_all()
				
	def game_over(self, score=True):
		
		self.bottom_bar.hide()
		self.map.unload()
		self.player.hide()
		
		self.music.play_end()
		self.game_active = False
		self.set_background()
		self.shake.stop()
		
		self.level_display.hide()
		self.points_display.hide()
		self.lives_display.hide()
		
		if score:
			
			if self.points_display.score > 	self.highscore:
				self.highscore = self.points_display.score
				self.save_highscore()
				pb = True
			else:
				pb = False
			
			self.menu = EndGameMenu(self.points_display.score, pb, self.continues)
			
			self.present_modal_scene(self.menu)
	
	def present_modal_scene(self, menu):
		Scene.present_modal_scene(self, menu)
		
if __name__ == '__main__':
	
	InApp.initialize_dummy()
	
	run(Game(), LANDSCAPE, show_fps=False)
