# coding: utf-8
from scene import *
import game_levels as levels
import os
import datetime
from scaler import Scaler
from random import randint
from check_point import CheckPoint

A = Action

def get_vanish(tile_type, x_hides):
	if tile_type.isdigit():
		return int(tile_type)
	elif tile_type == 'v':
		return 5
	elif tile_type == 'x':
		return x_hides
	else:
		return 0
			
class Tile:
	
	def __init__(self, map, brick_type, x, y):
		
		self.x_hides = map.x_hides
		self.key = (x, y)
		
		self.position = Point(map.min_x + x * map.tile_w, map.min_y + (y-1) * map.tile_h)
		
		self.brick_type = brick_type
		self.size = (map.tile_w, map.tile_h)
		
		if brick_type != ' ' and brick_type != '-':
			
			self.node = SpriteNode(parent=map.game.game_node, position=self.position)
			self.node.texture = self.get_texture(brick_type)
			self.node.anchor_point = (0.5, 0.5)
			self.node.size = self.size
			self.node.scale = 0
			self.node.alpha = 0.8
			self.blank = False
			
			if brick_type.lower() in ['i', '@', '!']:
				self.can_hide = True
			else:
				self.can_hide = False
				
		else:
			self.node = None
			self.blank = True
			self.can_hide = False
			
		self.start_hidden = False
	
	def set_start_hidden(self):
		self.start_hidden = True
		self.hide()
		
	def hide(self):
		if self.can_hide:
			self.node.scale = 0
	
	def unhide(self):
			
		if self.node is not None:
			if self.node.scale == 0:
				self.node.scale = 1
			
	def normalise(self):
		self.node.texture = Texture(self.get_blank(1))
		self.node.size = self.size
	
	def denormalise(self):
		
		if self.node is None:
			return
			
		self.node.texture = Texture(self.get_path(self.brick_type))
		self.node.size = self.size
	
	def get_texture(self, tile_type):
		
		path = self.get_path(tile_type)
		
		if not os.path.isfile(path):
			raise Exception('File not found {0}'.format(path))
			
		return Texture(path)
			
	def get_path(self, tile_type):
		
		folder = 'Tiles'
		vanish = get_vanish(tile_type, self.x_hides)
		
		if vanish > 0:
			return self.get_tile_path("vanish.png")
		elif tile_type.lower() == 'b':
			return self.get_tile_path("start.png")
		elif tile_type.lower() == 'h':
			return self.get_tile_path("hide.png")
		elif tile_type.lower() == 'u':
			return self.get_tile_path("unhide.png")
		elif tile_type.lower() == "s":
			return self.get_tile_path("south.png")
		elif tile_type.lower() == "e":
			return self.get_tile_path("east.png")
		elif tile_type.lower() == "w":
			return self.get_tile_path("west.png")
		elif tile_type.lower() == "n":
			return self.get_tile_path("north.png")
		elif tile_type in ["p", "@"]:
			return self.get_tile_path("points.png")
		elif tile_type in ["d", "!"]:
			return self.get_tile_path("death.png")
		elif tile_type == "l":
			return self.get_tile_path("life.png")
		elif tile_type == "m":
			return self.get_tile_path("more_time.png")
		elif tile_type == "t":
			return self.get_tile_path("less_time.png")
		elif tile_type == "y":
			return self.get_tile_path("sticky.png")
		if tile_type == "r":
			return self.get_tile_path("reverse.png")
		elif tile_type == 'c':
			return self.get_blank()
		elif tile_type == 'z':
			return self.get_blank()
		else:
			return self.get_blank()
	
	def get_blank(self, index=None):
		
		if index is None:
			index = randint(1, 4)
		
		return self.get_tile_path("blank{0}.png".format(index))
		
	def get_tile_path(self, file_name):
		return Scaler.get_tile_path(file_name)
		
	def appear(self, wait):
		
		if self.node != None:
			self.node.run_action(A.sequence(A.wait(wait), A.scale_to(1, 0.25, 4)))
		
class Map:
	
	def __init__(self, game):
		
		self.game = game
		self.start_position = None
		self.end = None
		self.check_point = False
		self.check_point_flag = None
		self.position = None
		self.show_position = None
		self.start = None
		self.target = None
		self.moving = False
		self.load_end = None
		self.hidden = False
		
		self.tiles = {}
		self.reverses = {}
		self.vanishes = {}
		self.vanish_durations = {}
		
		self.deaths = {}
		self.lives = {}
		self.stickies = {}
		self.more_times = {}
		self.less_times = {}
		self.points = {}
		self.hides = {}
		self.unhides = {}
		
		self.tile_w = 32 * Scaler.get_scale()
		self.tile_h = 23 * Scaler.get_scale()
		
	def hide(self):
			
		for tile in self.tiles.values():
			tile.hide()
		
		self.hidden = True

	def unhide(self):

		for tile in self.tiles.values():
			tile.unhide()
		
		self.hidden = False

	def reset_hide(self):

		for tile in self.tiles.values():
			if tile.start_hidden:
				tile.hide()
			else:
				if self.hidden:
					tile.unhide()
		
		self.hidden = False
		
	def get_position(self):
		
		if self.moving:
			return self.show_position
		else:
			return   self.tiles[self.position].position
		
	def update_move(self):
		
		if not self.moving:
		 	return
		 
		seconds_past =(datetime.datetime.now() - self.start_move).total_seconds()
		
		if seconds_past >= self.move_seconds:
			self.moving = False
			self.position = self.target
			self.show_position = self.position
			return

		start_coord = self.tiles[self.start].position
			
		x = start_coord[0] + self.speed[0] * seconds_past
		
		y = start_coord[1] + self.speed[1] * seconds_past
		
		self.show_position = (x, y)

	def move(self, step_x, step_y, move_seconds):
		
		dx = self.tile_w * step_x
		dy = self.tile_h * step_y
		
		x = self.position[0] + step_x
		y = self.position[1] + step_y
		
		new_position = (x, y)
		
		if (self.tiles[new_position].node != None):
			
			self.start_move = datetime.datetime.now()
			self.moving = True
			self.move_seconds = move_seconds
		
			self.start = self.position
			self.target = new_position
			
			start_coord = self.tiles[self.position].position
			target_coord = self.tiles[self.target].position
			
			speed_x = (target_coord[0] - start_coord[0]) / move_seconds
			
			speed_y = (target_coord[1] - start_coord[1]) / move_seconds
		
			self.speed = (speed_x, speed_y)
			
			self.update_move()
			
		else:
			
			self.moving = False
	
	def reset(self):
		
		self.moving = False
		self.position = self.start_position
		self.show_position = self.position

		for position in self.unhides:
			self.unhides[position] = True
			self.tiles[position].denormalise()
			
		for position in self.hides:
			self.hides[position] = True
			self.tiles[position].denormalise()
			
		for position in self.reverses:
			self.reverses[position] = True
			self.tiles[position].denormalise()

		for position in self.vanishes:
			self.vanishes[position] = True
			self.tiles[position].denormalise()

		for position in self.stickies:
			self.stickies[position] = True
			self.tiles[position].denormalise()
			
		for position in self.deaths:
			self.deaths[position] = True
			self.tiles[position].denormalise()

		for position in self.more_times:
			self.more_times[position] = True
			self.tiles[position].denormalise()

		for position in self.less_times:
			self.less_times[position] = True
			self.tiles[position].denormalise()
			
	def on_map(self):
		return (self.tiles[self.position].node != None)
		
	def at_end(self):
		return (self.position == self.end.key)

	def on_points(self):
		if self.position in self.points:
			return self.points[self.position]
		else:
			return False

	def on_death(self):
		if self.position in self.deaths:
			return self.deaths[self.position]
		else:
			return False

	def on_life(self):
		if self.position in self.lives:
			return self.lives[self.position]
		else:
			return False
			
	def on_sticky(self):
		if self.position in self.stickies:
			return self.stickies[self.position]
		else:
			return False
			
	def on_more_time(self):
		if self.position in self.more_times:
			return self.more_times[self.position]
		else:
			return False

	def on_less_time(self):
		if self.position in self.less_times:
			return self.less_times[self.position]
		else:
			return False
			
	def on_reverse(self):
		if self.position in self.reverses:
			return self.reverses[self.position]
		else:
			return False

	def on_vanish(self):
		if self.position in self.vanishes:
			return self.vanishes[self.position]
		else:
			return False
	
	def on_hide(self):
		if self.position in self.hides:
			return self.hides[self.position]
		else:
			return False

	def on_unhide(self):
		if self.position in self.unhides:
			return self.unhides[self.position]
		else:
			return False
			
	def vanish_duration(self):
		return self.vanish_durations[self.position]

	def clear_hide(self):
		if self.position in self.hides:
			self.hides[self.position] = False
			self.tiles[self.position].normalise()
	
	def clear_unhide(self):
		if self.position in self.unhides:
			self.unhides[self.position] = False
			self.tiles[self.position].normalise()
			
	def clear_death(self):
		if self.position in self.deaths:
			self.deaths[self.position] = False
			self.tiles[self.position].normalise()

	def clear_life(self):
		if self.position in self.lives:
			self.lives[self.position] = False
			self.tiles[self.position].normalise()
			
	def clear_sticky(self):
		if self.position in self.stickies:
			self.stickies[self.position] = False
			self.tiles[self.position].normalise()
			
	def clear_points(self):
		if self.position in self.points:
			self.points[self.position] = False
			self.tiles[self.position].normalise()

	def clear_more_time(self):
		if self.position in self.more_times:
			self.more_times[self.position] = False
			self.tiles[self.position].normalise()
			
	def clear_less_time(self):
		if self.position in self.less_times:
			self.less_times[self.position] = False
			self.tiles[self.position].normalise()
			
	def clear_reverse(self):
		if self.position in self.reverses:
			self.reverses[self.position] = False
			self.tiles[self.position].normalise()
	
	def clear_vanish(self):
		if self.position in self.vanishes:
			self.vanishes[self.position] = False
			self.tiles[self.position].normalise()
			
	def load_level(self, level_str, loading_str, delay, check_point, x_hides):
		
		for tile in self.tiles.values():
			if tile.node != None:
				tile.node.run_action(A.remove())
		
		if self.check_point:
			self.check_point_flag.node.run_action(A.remove())

		self.check_point = check_point
		self.check_point_flag = None
		
		self.tiles = {}
		self.reverses = {}
		self.vanishes = {}
		self.vanish_durations = {}
		
		self.lives = {}
		self.deaths = {}
		self.stickies = {}
		self.more_times = {}
		self.less_times = {}
		self.points = {}
		self.hides = {}
		self.unhides = {}
		self.loadings = {}
		
		self.hidden = False
		self.x_hides = x_hides
		
		self.end = None
		
		lines = level_str.splitlines()[1:]
		
		if loading_str is not None:
			loading_lines = loading_str.splitlines()
		else:
			loading_lines = None
		
		self.min_y = self.game.size.h/2 - len(lines) * self.tile_h/2 + 50 * Scaler.get_scale()
		
		max_columns = 0
		
		for line in lines:
			max_columns = max([max_columns, len(line)])
			
		self.min_x = self.game.size.w * 0.5 - (max_columns * 0.5) * self.tile_w
		
		self.add_row(-1, "", max_columns)
		
		for y, line in enumerate(reversed(lines)):
			
			if loading_lines is not None:
				loading_line = loading_lines[len(loading_lines) - y - 1]
			else:
				loading_line = None
				
			self.add_row(y, line, max_columns, loading_line)
		
		self.add_row(y+1, "", max_columns)
		
		self.position = self.start_position
		
		count = 0
		
		if len(self.loadings) > 0:
			tiles = []
			for key in sorted(self.loadings):
				tile_array = self.loadings[key]
				if key != '*':
					tiles.append(tile_array)
				else:
					for tile in tile_array:
						tile.set_start_hidden()
		else:
			tiles = []
			for tile in self.tiles.values():
				tiles.append([tile])
		
		for tile_array in tiles:
			
			if not tile_array[0].blank:
				count += 1
			
			for tile in tile_array:
				if not tile.blank:
					tile.appear(count*delay)
		
		if self.check_point:
			count += 1
			self.check_point_flag.appear(count * delay)
			
		self.load_end = datetime.datetime.now() + datetime.timedelta(seconds = count * delay)
		
	def loaded(self):
		
		if datetime.datetime.now() > self.load_end:
			return True
		else:
			return False
	
	def add_row(self, y, line, max_columns, loading_line=None):
		
		x = -1
		
		self.add_tile(" ", x, y)
		
		for x, char in enumerate(line):
			
			if loading_line is not None:
				loading_char = loading_line[x]
			else:
				loading_char = None
				
			self.add_tile(char, x, y, loading_char)
		
		x += 1
		
		while x < (max_columns + 1):
			self.add_tile(" ", x, y)
			x += 1
			
	def is_start(self, tile):
		
		if tile.lower() == 'b':
			return True
		else:
			return False
			
	def is_end(self, tile):

		if tile.lower() == 's':
			return True
		elif tile.lower() == 'w':
			return True
		elif tile.lower() == 'e':
			return True
		elif tile.lower() == 'n':
			return True
		else:
			return False
		
	def add_tile(self, tile_type, x, y, loading=None):
		
		tile = Tile(self, tile_type, x, y)
		
		self.tiles[tile.key] = tile
		
		if loading is not None:
			
			if not loading in self.loadings:
				self.loadings[loading] = []
				
			self.loadings[loading].append(tile)
		
		vanish = get_vanish(tile_type, self.x_hides)
		
		if vanish > 0:
			self.vanishes[tile.key] = True
			self.vanish_durations[tile.key] = vanish
		elif self.is_start(tile_type):
				self.start_position = tile.key
		elif self.is_end(tile_type):
				self.end = tile
				if self.check_point:
					self.check_point_flag = CheckPoint(tile)
		elif tile_type == 'r':
			self.reverses[tile.key] = True
		elif tile_type in ['d','!']:
			self.deaths[tile.key] = True
		elif tile_type == 'l':
			self.lives[tile.key] = True
		elif tile_type == 'y':
			self.stickies[tile.key] = True
		elif tile_type == 'm':
			self.more_times[tile.key] = True
		elif tile_type == 't':
			self.less_times[tile.key] = True
		elif tile_type in ['p','@']:
			self.points[tile.key] = True
		elif tile_type == 'h':
			self.hides[tile.key] = True
		elif tile_type == 'u':
			self.unhides[tile.key] = True
