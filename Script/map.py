# coding: utf-8
from scene import *
import game_levels as levels
import os
import datetime

A = Action

def get_vanish(tile_type):
	if tile_type.isdigit():
		return int(tile_type)
	elif tile_type == 'v':
		return 5
	elif tile_type == 'x':
		return 25
	else:
		return 0
			
class Tile:
	
	def __init__(self, map, brick_type, x, y):
		
		self.key = (x, y)
		
		self.position = Point(map.min_x + x * map.tile_w, map.min_y + y * map.tile_h)
		
		self.brick_type = brick_type
		self.size = (map.tile_w, map.tile_h)
		
		if brick_type != ' ' and brick_type != '-':
			self.node = SpriteNode(self.get_path(brick_type), parent=map.game.game_node, position=self.position)		
			self.node.anchor_point = (0.5, 0.5)
			self.node.size = self.size
			self.node.scale = 0
			self.node.alpha = 0.8
			self.blank = False
		else:
			self.node = None
			self.blank = True
	
	def normalise(self):
		self.node.texture = Texture(self.get_path('c'))
		self.node.size = self.size
	
	def denormalise(self):
		self.node.texture = Texture(self.get_path(self.brick_type))
		self.node.size = self.size
			
	def get_path(self, tile_type):
		
		folder = 'Tiles'
		vanish = get_vanish(tile_type)
		
		if vanish > 0:
			return os.path.join(folder, "tile_vanish.png")
		elif tile_type.lower() == "s":
			return os.path.join(folder, "south.png")
		elif tile_type.lower() == "e":
			return os.path.join(folder, "east.png")
		elif tile_type.lower() == "w":
			return os.path.join(folder, "west.png")
		elif tile_type.lower() == "n":
			return os.path.join(folder, "north.png")
		elif tile_type == "p":
			return os.path.join(folder, "points.png")
		elif tile_type == "d":
			return os.path.join(folder, "death.png")
		elif tile_type == "l":
			return os.path.join(folder, "life.png")
		elif tile_type == "m":
			return os.path.join(folder, "more_time.png")
		elif tile_type == "t":
			return os.path.join(folder, "less_time.png")
		elif tile_type == "y":
			return os.path.join(folder, "sticky.png")
		if tile_type == "r":
			return os.path.join(folder, "tile_reverse.png")
		elif tile_type == 'c':
			return os.path.join(folder, "circle_tile_big.png")
		elif tile_type == 'z':
			return os.path.join(folder, "circle_tile_small.png")
		else:
			return os.path.join(folder, "circle_tile_big.png")
			
	def appear(self, wait):
		
		if self.node != None:
			self.node.run_action(A.sequence(A.wait(wait), A.scale_to(1, 0.25, 4)))
		
class Map:
	
	def __init__(self, game):
		
		self.game = game
		self.start_position = None
		self.end_position = None
		self.position = None
		self.show_position = None
		self.start = None
		self.target = None
		self.moving = False
		self.load_end = None
		
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
		
		if self.game.size.w > 760:
			#iPad
			self.tile_w, self.tile_h = 64, 64
		else:
			#iPhone
			self.tile_w, self.tile_h = 32, 32
		
		self.load_end = None
		
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
		return (self.position == self.end_position)

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
	
	def vanish_duration(self):
		return self.vanish_durations[self.position]

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
			
	def load_level(self, level_str, loading_str=None):
		
		for tile in self.tiles.values():
			if tile.node != None:
				tile.node.run_action(A.remove())
			
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
		self.loadings = {}
		
		lines = level_str.splitlines()
		
		if loading_str is not None:
			loading_lines = loading_str.splitlines()
		else:
			loading_lines = None
		
		self.min_x = self.game.size.w/2 - 4.5 * self.tile_w
		
		self.min_y = self.game.size.h/2 - len(lines) * self.tile_h/2 + 50
		
		max_columns = 0
		
		for line in lines:
			max_columns = max([max_columns, len(line)])
		
		self.min_x = self.game.size.w/2 - (max_columns / 2) * self.tile_w
		
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
				tiles.append(self.loadings[key])
		else:
			tiles = []
			for tile in self.tiles.values():
				tiles.append([tile])
		
		delay = 0.05
		
		for tile_array in tiles:
			
			if not tile_array[0].blank:
				count += 1
			
			for tile in tile_array:
				if not tile.blank:
					tile.appear(count*delay)
				
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
			
	def is_start_end(self, tile):
		
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
	
	def is_start(self, tile):
		
		if self.is_start_end(tile):
			if tile.lower() == tile:
				return True
				
		return False

	def is_end(self, tile):
		
		if self.is_start_end(tile):
			if tile.upper() == tile:
				return True
				
		return False
		
	def add_tile(self, tile_type, x, y, loading=None):
		
		tile = Tile(self, tile_type, x, y)
		self.tiles[tile.key] = tile
		
		if loading is not None:
			
			if not loading in self.loadings:
				self.loadings[loading] = []
				
			self.loadings[loading].append(tile)
		
		vanish = get_vanish(tile_type)
		
		if vanish > 0:
			self.vanishes[tile.key] = True
			self.vanish_durations[tile.key] = vanish
		elif self.is_start(tile_type):
				self.start_position = tile.key
		elif self.is_end(tile_type):
				self.end_position = tile.key
		elif tile_type == 'r':
			self.reverses[tile.key] = True
		elif tile_type == 'd':
			self.deaths[tile.key] = True
		elif tile_type == 'l':
			self.lives[tile.key] = True
		elif tile_type == 'y':
			self.stickies[tile.key] = True
		elif tile_type == 'm':
			self.more_times[tile.key] = True
		elif tile_type == 't':
			self.less_times[tile.key] = True
		elif tile_type == 'p':
			self.points[tile.key] = True
