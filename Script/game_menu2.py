# coding: utf-8
# This module implements the menu that is used by all game examples. It doesn't do much by itself.

from scene import *
import ui
import sound
import os
from gradient import Gradient
import palette
import font
from scaler import Scaler
from products_controller import ProductsController
from wrapping import WrappingLabelNode
from random import random
from random import randint

def get_checkpoint_level(action):
	data = action.lower().replace('l','')
	level = int(data)
	return level
	
def is_checkpoint(action):
	action = action.lower()
	if len(action) == 3 and action[0] == 'l':
		return True
	else:
		return False
		
def offer_active():
	
	return ProductsController.get().offer_active()

def star_text(points):
	if points < 1:
		return ''
	if points <= 12:
		return font.STAR * points
	else:
		return '{0}{1}'.format(points, font.STAR)

def extract_stars(text):
	if len(text) > 1 and text.count(font.STAR)==1:
		return int(text.replace(font.STAR, ''))
	else:
		return len(text)
		
class ScoreLabelNode(LabelNode):
	
	def __init__(self, menu, score, base_text='score'):
		
		self.base_text = base_text
		
		button_font = (font.BUTTON, int(20*Scaler.Menu))
		
		LabelNode.__init__(self, text='', font=button_font, color='#ffffff', parent =menu.menu_bg)

		self.anchor_point = (0.5,1)
		
		self.position=(0, menu.bottom()-menu.space_y)
		
		self.set_score(score)
	
	def add_score(self):
		self.set_score(self.score + 1)
		
	def set_score(self, score):
		self.score = score
		self.text = self.make_score_text(score)
	
	def make_score_text(self, score):
		return '{0} {1} {2} {1}'.format(self.base_text, font.STAR, score)

		
class EmphasiseText:
	
	def __init__(self, nodes, index):
		
		if isinstance(nodes, list):
			self.nodes = nodes
		else:
			self.nodes = [nodes]
		
		self.on = False
		
		self.base_colors = []
		self.base_fonts = []
		
		for i in range(len(self.nodes)):
			node = self.nodes[i]
			self.base_colors.append(node.color)
			self.base_fonts.append(node.font)
		
		self.index = index
		
	def __call__(self):
		
		if not self.on:
			
			sound.play_effect('arcade:Powerup_3', 0.2, (1 + 1.0/8.0 * self.index))
			
			for i in range(len(self.nodes)):
				node = self.nodes[i]
				#node.color = '#e28c9b'
				node.font = (node.font[0], int(30*Scaler.Menu))
			
			self.on = True
			
		else:
			
			for i in range(len(self.nodes)):
				node = self.nodes[i]
				node.color = self.base_colors[i]
				node.font = self.base_fonts[i]
				
			self.on = False
		
class StartFade:
	
	def __init__(self, node):
		self.node = node

	def __call__(self):
		sound.play_effect('arcade:Powerup_2')
		self.node.run_action(Action.fade_to(1))
		
class Star:
	
	def __init__(self, node, score_node):
		self.node = node
		self.score_node = score_node
		
	def __call__(self):
		
		text = self.node.info_label.text
		
		if len(text) < 1:
			return
		
		sound.play_effect('game:Ding_3', 0.2)
		
		points = extract_stars(text)
		
		if points > 50:
			step = 5
		else:
			step = 1
			
		self.node.info_label.text = star_text(points-step)
		
		self.score_node.add_score()
		
class InfoNode (SpriteNode):
	
	def __init__(self, info, parent):
		
		SpriteNode.__init__(self, parent=parent)
		
		button_font = (font.BUTTON, int(20*Scaler.Menu))
		
		self.heading_label = LabelNode(info[0], font=button_font, color='#71c0e2', position=(0, 5), parent=self)
		
		self.info_label = self.new_info_label(info[1], font=button_font, color='#000000', position=(0, -20*Scaler.Menu), parent=self)
		
		if len(info) >= 3:
			self.heading_label.font = (button_font[0], info[2]*Scaler.Menu)

		if len(info) >= 4:
			self.info_label.font = (button_font[0], info[3]*Scaler.Menu)
			
		self.size = (self.parent.size.w * 0.8, self.heading_label.size.h + self.info_label.size.h)

	def new_info_label(self, text, font, color, position, parent):
		return LabelNode(text, font=font, color=color, position=position, parent=parent)

class WrappingInfoNode(InfoNode):

	def new_info_label(self, text, font, color, position, parent):
		
		fraction_of_parent_width = 0.9
		
		node = WrappingLabelNode(parent=parent, anchor_point=(0.5, 0.5), position=position,
		target_width=parent.parent.size.w*fraction_of_parent_width,
		font_type=font[0],
		color=color)
		
		node.set_text(text, font[1])
		
		return node

class Button(object):
	
	def __init__(self, action, tag):
		self.action = action
		self.tag = tag
		
class ButtonNode (SpriteNode):
	
	def __init__(self, button, parent, position=None):
		
		self.action = button.action
		
		SpriteNode.__init__(self, parent=parent)
		
		self.update_tag(button.tag)
		self.anchor_point = (0.5, 1)
		self.enabled = True
		
		if not position is None:
			self.position = position
	
	def update_tag(self, tag):
		
		self.untouch_texture = Texture(Scaler.get_button_off(tag))
		self.touch_texture = Texture(Scaler.get_button_on(tag))
		self.disabled_texture = self.untouch_texture
		
		self.texture = self.untouch_texture
					
	def set_action(self, action):
		self.action = action
		
	def disable(self):
		self.enabled = False
		self.texture = self.disabled_texture
		
	def touch(self):
		self.texture = self.touch_texture

	def untouch(self):
		self.texture = self.untouch_texture
		
class MenuScene (Scene):
	
	def __init__(self, tag, main_menu_button=True):
		
		Scene.__init__(self)
		
		self.space_x = 13.5 * Scaler.Menu
		self.space_y = 13.5 * Scaler.Menu
		
		self.main_menu_button = main_menu_button
		
		self.buttons = []
		self.tag = tag
	
	def get_menu_bg_texture(self):
		return Texture(Scaler.get_menu(self.tag))
		
	def update(self):
		# overloaded by menus with animated bits
		pass
	
	def below_height(self):
		return 0
	
	def total_height(self):
		
		height = self.menu_bg.size.h
		height += self.below_height()
		
		return height
		
	def center_y(self):
		
		total_height = self.total_height()
		space = 0.5 * (self.size.h - total_height)
		
		x = self.menu_bg.position[0]
		y = space + self.below_height() + self.menu_bg.size.h * 0.5
		
		new_position = (x, y)
		
		self.menu_bg.position = new_position
	
	def get_width(self):
		return self.menu_bg.size.w

	def bottom(self):
		return -self.menu_bg.size.h*0.35
		
	def setup(self):
		
		self.add_bg()
		self.add_menu_bg()
		
		self.add_buttons()
		
		self.center_y()
		
		self.fade_bg()
	
	def fade_bg(self):
		self.bg.alpha = 0
		self.bg.run_action(Action.fade_to(1))
		
	def add_buttons(self):
		
		if self.main_menu_button:
			
			self.main_menu = ButtonNode(button=Button('main menu','main_menu'), parent=self.menu_bg)

			y = self.bottom()-self.space_y/2
		
			self.main_menu.anchor_point = (0.5, 1.0)
			self.main_menu.position = (0, y)
			
			self.buttons.append(self.main_menu)
		
	def add_bg(self):
		
		self.bg = SpriteNode(color=palette.BASE_BG, parent=self)
		
		self.bg.size = self.size + (2*Scaler.Menu, 2*Scaler.Menu)
		
		self.bg.position = self.size/2
		
		#self.background_gradient = Gradient(self)
		#self.background_gradient.size=(self.size.w, self.size.h)
		
	def add_menu_bg(self):
		
		self.menu_bg = SpriteNode(texture=self.get_menu_bg_texture(), position=(self.size.w/2,self.size.h/2), parent=self)
		
		self.menu_bg.anchor_point = (0.5, 0.5)
		
	def touch_began(self, touch):
		
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			if touch_loc in btn.frame and btn.enabled:
				btn.touch()
	
	def should_action(self, action):
		return True
		
	def touch_ended(self, touch):
	
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			
			if btn.enabled:
				
				btn.untouch()
							
				if self.presenting_scene and touch_loc in btn.frame:
					
					if self.should_action(btn.action):
						self.show_menu(btn.action)
						return True
		
		return False
					
	def show_menu(self, menu):
		self.presenting_scene.menu_button_selected(menu)

class NoButtonMenu(MenuScene):

	def __init__(self, tag, main_menu_button=True):
	
		MenuScene.__init__(self, tag=tag,main_menu_button=main_menu_button)


class OneButtonMenu(MenuScene):

	def __init__(self, tag, button,main_menu_button=True):
	
		MenuScene.__init__(self, tag=tag,main_menu_button=main_menu_button)
			
		self.button = button
		
	def get_y(self):
		return self.bottom()+self.space_y
		
	def add_buttons(self):
		
		MenuScene.add_buttons(self)
		
		button = ButtonNode(button=self.button, parent=self.menu_bg)

		y = self.get_y()
		
		button.anchor_point = (0.5, 0.0)
		button.position = (0, y)
		
		self.buttons.append(button)
		
class TwoButtonMenu(MenuScene):

	def __init__(self, tag, button_lhs, button_rhs,main_menu_button=True):
	
		MenuScene.__init__(self, tag=tag,main_menu_button=main_menu_button)
			
		self.button_lhs = button_lhs
		self.button_rhs = button_rhs
	
	def get_y(self):
		return self.bottom()+self.space_y
		
	def add_buttons(self):
		
		MenuScene.add_buttons(self)
		
		self.lhs = ButtonNode(button=self.button_lhs, parent=self.menu_bg)
		
		self.rhs = ButtonNode(button=self.button_rhs, parent=self.menu_bg)

		y = self.get_y()
		
		self.lhs.anchor_point = (0.5, 0.0)
		self.lhs.position = (-self.lhs.size.w/2-self.space_x/2, y)
		
		self.rhs.anchor_point = (0.5, 0.0)
		self.rhs.position = (self.rhs.size.w/2+self.space_x/2, y)

		self.buttons.append(self.lhs)
		self.buttons.append(self.rhs)

class ThreeButtonMenu(MenuScene):

	def __init__(self, tag, button_lhs, button_middle, button_rhs,main_menu_button=True):
	
		MenuScene.__init__(self, tag=tag,main_menu_button=main_menu_button)
			
		self.button_lhs = button_lhs
		self.button_middle = button_middle
		self.button_rhs = button_rhs

	def get_y(self):
		return self.bottom()+self.space_y
		
	def add_buttons(self):
		
		MenuScene.add_buttons(self)
		
		self.lhs = ButtonNode(button=self.button_lhs, parent=self.menu_bg)
		
		self.middle = ButtonNode(button=self.button_middle, parent=self.menu_bg)
		
		self.rhs = ButtonNode(button=self.button_rhs, parent=self.menu_bg)

		y = self.get_y()
		
		self.lhs.anchor_point = (1.0, 0.0)
		self.lhs.position = (-self.middle.size.w/2-self.space_x, y)

		self.middle.anchor_point = (0.5, 0.0)
		self.middle.position = (0.0, y)
		
		self.rhs.anchor_point = (0.0, 0.0)
		self.rhs.position = (self.middle.size.w/2+self.space_x, y)

		self.buttons.append(self.lhs)
		self.buttons.append(self.middle)
		self.buttons.append(self.rhs)


class RestartMenu(MenuScene):

	def __init__(self, check_points):

		self.enables = []
		
		for level in check_points:
			
			check_point = check_points[level]
			
			if check_point.complete:
				self.enables.append(check_point.level)
		
		MenuScene.__init__(self, tag='restart_from_checkpoint',main_menu_button=True)

	def add_buttons(self):
		
		MenuScene.add_buttons(self)
		
		rows = []
		
		rows.append([80, 85, 90, 95])
		rows.append([50, 60, 70, 75])
		rows.append([10, 20, 30, 40])
		
		y = self.bottom()+self.space_y
		dict = {}
		width = 0
		
		for row in rows:
			
			for item in row:
				
				if item in self.enables:
					tag = 'Checkpoint_{0}'.format(item)
				else:
					tag = 'Checkpoint_{0}_locked'.format(item)
					
				button = Button(tag=tag,action='L{0}'.format(item))
				
				button_node = ButtonNode(button=button, parent=self.menu_bg)
					 
				button_node.anchor_point = (0.0, 0.0)
				
				self.buttons.append(button_node)
				dict[item] = button_node
				
				width += button_node.size.w
				
		y = self.bottom()+self.space_y
		width /= len(rows)
		width += 3*self.space_x
		
		for row in rows:
			
			x = -0.5 * width
			
			for item in row:
				
				button_node = dict[item]
				
				button_node.position = (x, y)
				
				x += button_node.size.w + self.space_x
				
			y += button_node.size.h + self.space_y

	def should_action(self, action):
		
		if is_checkpoint(action):
			level = get_checkpoint_level(action)
			if level in self.enables:
				return True
			else:
				return False
		else:
			return True
			
class CopyFailMenu(MenuScene):
	
	def __init__(self):
		
		buttons = []
		infos = []
		
		infos.append(('could not', 'expand files'))
		infos.append(('try freeing', 'up space'))
		infos.append(('on your', 'device'))
		
		MenuScene.__init__(self,'Failed', buttons, infos=infos)

	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		self.info_nodes[1].heading_label.color = '#000000'
		self.info_nodes[2].heading_label.color = '#000000'
		
class CreditsMenu(ThreeButtonMenu):
	
	def __init__(self):
		ThreeButtonMenu.__init__(self,tag='credits',button_lhs=Button(tag='credits_peter', action='peter'),
		button_middle=Button(tag='credits_fred', action='fred'),
		button_rhs=Button(tag='credits_david', action='david'))

	def get_y(self):
		return self.bottom()+self.space_y*3.5
		
class CheckpointsPurchaseRequiredMenu(OneButtonMenu):
	
	def __init__(self):
		OneButtonMenu.__init__(self,tag='purchase_required',button=Button(tag='purchase_required',action='purchase menu'))

		
class OptionsMenu(MenuScene):
	
	def __init__(self, playing_position, music, fx):
		
		MenuScene.__init__(self, tag='options',main_menu_button=True)
		
		self.space_y *= 0.5
		
		self.playing_position = playing_position
		self.music = music
		self.fx = fx
	
	def music_off_tag(self):
		if not self.music:
			return 'options_musicoff_active'
		else:
			return 'options_musicoff'

	def music_on_tag(self):
		if self.music:
			return 'options_musicon_active'
		else:
			return 'options_musicon'

	def fx_off_tag(self):
		if not self.fx:
			return 'options_fxoff_active'
		else:
			return 'options_fxoff'

	def fx_on_tag(self):
		if self.fx:
			return 'options_fxon_active'
		else:
			return 'options_fxon'

	def standing_tag(self):
		if self.playing_position.lower() == 'standing':
			return 'options_standing_active'
		else:
			return 'options_standing'

	def sitting_tag(self):
		if self.playing_position.lower() == 'sitting':
			return 'options_sitting_active'
		else:
			return 'options_sitting'
	
	def update_options(self, music, fx, playing_position):
		
		self.music = music
		self.fx = fx
		self.playing_position = playing_position
		self.music_off_node.update_tag(self.music_off_tag())
		self.music_on_node.update_tag(self.music_on_tag())
		self.fx_off_node.update_tag(self.fx_off_tag())
		self.fx_on_node.update_tag(self.fx_on_tag())
		self.sitting_node.update_tag(self.sitting_tag())
		self.standing_node.update_tag(self.standing_tag())
	
	def add_buttons(self):
		
		MenuScene.add_buttons(self)
		width = 4 * self.space_x
		
		#music off
		music_off = Button(tag=self.music_off_tag(),action='music off')
				
		self.music_off_node = ButtonNode(button=music_off, parent=self.menu_bg)
					 
		self.music_off_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.music_off_node)
		
		width += self.music_off_node.size.w
		
		#music on
		music_on = Button(tag=self.music_on_tag(),action='music on')
				
		self.music_on_node = ButtonNode(button=music_on, parent=self.menu_bg)
					 
		self.music_on_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.music_on_node)
		
		#fx off
		fx_off = Button(tag=self.fx_off_tag(),action='fx off')
				
		self.fx_off_node = ButtonNode(button=fx_off, parent=self.menu_bg)
					 
		self.fx_off_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.fx_off_node)
		
		width += self.fx_off_node.size.w
		
		#fx on
		fx_on = Button(tag=self.fx_on_tag(),action='fx on')
				
		self.fx_on_node = ButtonNode(button=fx_on, parent=self.menu_bg)
					 
		self.fx_on_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.fx_on_node)

		#credits
		credits = Button(tag='options_credits',action='credits')
				
		self.credits_node = ButtonNode(button=credits, parent=self.menu_bg)
					 
		self.credits_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.credits_node)
		
		width += self.credits_node.size.w
		
		#standing
		standing = Button(tag=self.standing_tag(),action='standing')
				
		self.standing_node = ButtonNode(button=standing, parent=self.menu_bg)
					 
		self.standing_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.standing_node)

		#sitting
		sitting = Button(tag=self.sitting_tag(),action='sitting')
				
		self.sitting_node = ButtonNode(button=sitting, parent=self.menu_bg)
					 
		self.sitting_node.anchor_point = (0.0, 0.0)
		self.buttons.append(self.sitting_node)

		#positioning
		x = -0.5 * width + self.space_x
		y = self.bottom() + self.space_y*2
		self.music_off_node.position = (x, y)
		y += self.music_off_node.size.h + self.space_y
		self.music_on_node.position = (x, y)
		y += self.music_on_node.size.h + self.space_y*2
		self.standing_node.position = (x, y)

		x += self.music_off_node.size.w + self.space_x
		y = self.bottom() + self.space_y*2
		self.fx_off_node.position = (x, y)
		y += self.fx_off_node.size.h + self.space_y
		self.fx_on_node.position = (x, y)

		x += self.fx_off_node.size.w + self.space_x
		y = self.bottom() + self.space_y*2
		self.credits_node.position = (x, y)

		x += self.credits_node.size.w - self.sitting_node.size.w
		y += self.credits_node.size.h + self.space_y*2
		self.sitting_node.position = (x, y)

	def update_playing_position(self, playing_position):
		self.buttons[0].set_title(playing_position)
		
class FirstPlayMenu(TwoButtonMenu):
	
	def __init__(self):
		
		TwoButtonMenu.__init__(self,
		tag='newbie',
		button_lhs=Button(tag='take_tutorial', action='take tutorial'),
		button_rhs=Button(tag='play_game', action='play game'))

class ConfirmQuitMenu(TwoButtonMenu):
	
	def __init__(self):
		
		TwoButtonMenu.__init__(self,
		tag='confirm_quit',
		button_lhs=Button(tag='confirm_quit_yes', action='end game'),
		button_rhs=Button(tag='confirm_quit_no', action='unpause'),
		main_menu_button=False)

class MainMenu(MenuScene):
	
	def __init__(self, highscore):
	
		MenuScene.__init__(self, tag='welcome')
		
		self.high_score = highscore
		self.space_y *= 0.75
		
	def add_buttons(self):
		
		self.purchase = ButtonNode(button=Button(tag='purchase', action='purchase'), parent=self.menu_bg)
		self.purchase.z_position = 1001
		
		if offer_active():
			star_texture = Texture(Scaler.get_button_off('sale_star'))
			star = SpriteNode(parent=self.purchase, texture=star_texture)
			star.anchor_point = (0.5, 0.5)
			star.position = (-0.5*self.purchase.size.w, 0.5*self.purchase.size.h)
			
		self.options = ButtonNode(button=Button(tag='options', action='options'), parent=self.menu_bg)
		
		y = self.bottom()+self.space_y
		
		self.purchase.anchor_point = (0.5, 0.0)
		self.purchase.position = (-self.purchase.size.w/2-self.space_x/2, y)
		
		self.options.anchor_point = (0.5, 0.0)
		self.options.position = (self.options.size.w/2+self.space_x/2, y)

		self.buttons.append(self.purchase)
		self.buttons.append(self.options)
		
		y += self.options.size.h+self.space_y
		
		self.tutorial = ButtonNode(button=Button(tag='tutorial', action='tutorial'), parent=self.menu_bg)
		
		self.tutorial.anchor_point = (0.5, 0.0)
		self.tutorial.position = (0, y)
		
		self.buttons.append(self.tutorial)
		
		y += self.tutorial.size.h+self.space_y
		
		self.checkpoint = ButtonNode(button=Button(tag='restart_active', action='restart from checkpoint'), parent=self.menu_bg)
		
		self.checkpoint.anchor_point = (0.5, 0.0)
		self.checkpoint.position = (0, y)
		
		self.buttons.append(self.checkpoint)
		
		y += self.checkpoint.size.h+self.space_y
		
		self.play = ButtonNode(button=Button(tag='play_from_start', action='play from start'), parent=self.menu_bg)
		
		self.play.anchor_point = (0.5, 0.0)
		self.play.position = (0, y)

		self.buttons.append(self.play)

	def setup(self):
		
		MenuScene.setup(self)
		
		self.score_label = ScoreLabelNode(menu=self, score=self.high_score, base_text='best score')
		
		if offer_active():
			pass
		

class PurchaseMenuBase(MenuScene):
	
	def get_width(self):
		return 400
		
	def new_info_node(self, info, parent):
		return WrappingInfoNode(info, parent=parent)
		
class ConfirmProductMenu(TwoButtonMenu):
	
	def __init__(self, product):
		
		self.product = product
		
		if product.can_purchase:
			buttons = ['okay','cancel']
		else:
			buttons = ['purchase menu']
		
		infos = []
		
		if product.can_purchase:
			info1 = 'Buy'
			info2 = product.title
			header = 'Confirm'
		else:
			header = 'Cannot'
			info1 = product.title
			info2 = product.why_cant_purchase
						
		infos.append((info1, info2))
		
		TwoButtonMenu.__init__(self, tag='purchase_confirm',button_lhs=Button(tag='purchase_ok',action='okay'),button_rhs=Button(tag='purchase_cancel',action='cancel'))

	def show_menu(self, menu):
	 	
		if 'okay' in menu.lower():
			self.presenting_scene.purchase_product(self.product)
		elif 'cancel' in menu.lower():
			self.presenting_scene.menu_button_selected('purchase menu')
		else:
			self.presenting_scene.menu_button_selected(menu)
		
class MakePurchaseMenu(NoButtonMenu):
	
	def __init__(self, product):
		
		self.product = product
		self.enable_button = False
		self.text_size = int(24 * Scaler.Menu)
		
		self.message = '{0} processing'.format(product.title)
		
		MenuScene.__init__(self, 'purchase_thanks',main_menu_button=True)
		
		self.failed_texture = Texture(Scaler.get_menu('purchase_failed'))
	
	def show_menu(self, menu):
		
		if self.enable_button:
			NoButtonMenu.show_menu(self, menu)
		
	def setup(self):
		
		MenuScene.setup(self)
		
		self.message_label = WrappingLabelNode(parent=self.menu_bg, anchor_point=(0.5, 0.5),
		position=(0.0, 0.0),
		target_width=300.0,
		font_type=font.BUTTON,
		color='#000000')
		ProductsController.get().purchase(self.product, self)
	
	def purchase_successful(self, product_identifier):
		
		self.set_message('successful')
		self.enable_button = True

	def purchase_restored(self, product_identifier):
		
		self.set_message('restored')
		self.enable_button = True

	def purchase_failed(self, product_identifier):
		self.menu_bg.texture = self.failed_texture
		self.set_message('failed')
		self.enable_button = True
	
	def set_message(self, message):
		self.message_label.set_text(message, self.text_size)
		
class PurchaseMenu(OneButtonMenu):
	
	NULL_ACTION = 'NULL ACTION'
	
	def __init__(self):
		
		products_controller = ProductsController.get()
		
		self.can_purchase = False
		self.price_text = ''
		self.font_size = 20
		
		action = PurchaseMenu.NULL_ACTION
		
		if not products_controller.enabled:
			
			self.price_text = 'purchases disabled'
			
		else:
			
			if products_controller.validated:
			
				self.checkpoints = products_controller.checkpoints
				
				if self.checkpoints.valid:
					
					if self.checkpoints.purchased:
							
						self.price_text = 'already purchased'
						
					else:
							
						self.price_text = str(self.checkpoints.price)
						self.font_size = 36
						self.can_purchase = True
						
						action = '{0}: {1}'.format(self.checkpoints.title, self.price_text)
						
				else:
				
					self.price_text = 'product invalid'
				
			else:
				
				self.price_text = 'could not validate'
		
		button = Button(tag='purchase_checkpoints',action=action)
		
		OneButtonMenu.__init__(self, tag='purchase', button=button)
	
	def setup(self):
		OneButtonMenu.setup(self)
		self.add_price_label()
	
	def add_price_label(self):

		label_font = (font.BUTTON, int(self.font_size*Scaler.Menu))
		
		self.price_label = LabelNode(parent=self.menu_bg, font=label_font,color='#ffffff')
		
		self.price_label.anchor_point = (0.5, 0.5)
		
		x = 0.0
		y = -80.0*Scaler.Menu
		
		self.price_label.position = (x, y)
		
		self.price_label.text = self.price_text

	def show_menu(self, menu):
	 	
	 	if menu.lower() == 'main menu':
	 		self.presenting_scene.menu_button_selected(menu)
	 	
	 	elif menu in PurchaseMenu.NULL_ACTION:
	 		
	 		return
	 		
	 	else:
			self.presenting_scene.product_selected(self.checkpoints)
	 	
class EndLevelMenu(MenuScene):
	
	def __init__(self, level, score, level_points, time_bonus, stars, check_point):
		
		self.complete = False
		self.score = score
		self.check_point = check_point
		self.stars = stars
		
		self.score_label = None
		self.next_level_button = None
		
		buttons = []
		
		infos = self.add_infos(level_points, time_bonus, stars, check_point)
			
		MenuScene.__init__(self, self.get_title(level), buttons, infos=infos, title_size=40)
	
	def get_title(self, level):
		return 'Level {0} Clear'.format(level)
		
	def add_infos(self, level_points, time_bonus, stars, check_point):
		
		infos = []
		
		infos, self.level_bonus_index = self.add_level_bonus(infos, level_points)
		
		infos, self.time_bonus_index = self.add_time_bonus(infos, time_bonus)
		
		if self.stars > 0:
			infos.append(('collected', star_text(stars)))
			self.stars_index = self.get_index(infos)
		else:
			self.stars_index = None
		
		if self.check_point:
			infos.append(('checkpoint', 'passed'))
			self.check_point_index = self.get_index(infos)
		else:
			self.check_point_index = None
		
		return infos
		
	def get_index(self, infos):
		return len(infos) - 1
		
	def add_level_bonus(self, infos, level_points):
		infos.append(('level bonus', star_text(level_points)))
		return infos, self.get_index(infos)
	
	def add_time_bonus(self, infos, time_bonus):
		infos.append(('time bonus', star_text(time_bonus)))
		return infos, self.get_index(infos)
		
	def below_height(self):
		
		height = 0
		
		if self.score_label is not None:
			height += self.score_label.size.h

		if self.next_level_button is not None:
			height += self.next_level_button.size.h
			
		return height
	
	def get_next_title(self):
		return 'play next level'
		
	def setup(self):
		
		MenuScene.setup(self)
		
		self.score_label = ScoreLabelNode(menu=self, score=self.score)
		
		btn = ButtonNode(self.get_next_title(), parent=self.menu_bg)
		
		btn.untouch_color='#ffffff'
		btn.touch_color='#000000'
		btn.untouch()
				
		btn.anchor_point = (0.5, 1)
		btn.position = (self.score_label.position[0], self.score_label.position[1] - btn.size.h)
			
		self.buttons.append(btn)
		
		actions = []
		
		self.next_level_button = self.buttons[0]
		
		self.next_level_button.alpha = 0
		
		actions.append(Action.wait(0.2))
		
		if not self.level_bonus_index is None:
			actions += self.add_star_action(self.level_bonus_index)

		if not self.time_bonus_index is None:
			actions += self.add_star_action(self.time_bonus_index)
		
		if not self.stars_index is None:
			actions += self.add_star_action(self.stars_index)
		
		if not self.check_point_index is None:
			self.info_nodes[self.check_point_index].info_label.color = '#71c0e2'
			
			items = [self.info_nodes[self.check_point_index].heading_label, self.info_nodes[self.check_point_index].info_label]
			
			emphasise = EmphasiseText(items, self.check_point_index)
			
			actions.append(Action.call(emphasise))
			actions.append(Action.wait(0.2))
			actions.append(Action.call(emphasise))
		actions.append(Action.call(StartFade(self.next_level_button)))

		actions.append(Action.call(self))
		self.info_nodes[0].run_action(Action.sequence(actions))
		
		self.did_change_size()
	
	def __call__(self):
		self.complete = True
		
	def add_star_action(self, index):
		
		actions = []
		
		actions.append(Action.wait(0.2))
		
		action = self.star_action(index)
		
		if action is not None:
			actions.append(action)
			
		return actions
		
	def star_action(self, index):
		
		node = self.info_nodes[index]
		count = extract_stars(node.info_label.text)
		
		if count < 1:
			return None
		
		score_node = self.score_label
		
		emphasise = EmphasiseText(node.heading_label, index)
		
		emphasise_action = Action.call(emphasise)
		
		star_action = Action.call(Star(node, score_node))
		wait_action = Action.wait(0.1)
		
		star_and_wait = Action.sequence([star_action, wait_action])

		stars_to_add = count
		stars_count = 0
		
		while stars_to_add > 0:
			
			stars_count += 1
			
			if stars_to_add > 50:
				stars_to_add -= 5
			else:
				stars_to_add -= 1
				
		stars = Action.repeat(star_and_wait, stars_count)
		
		unemphasise_action = Action.call(emphasise)
		
		return Action.sequence([emphasise_action, Action.wait(0.2), stars, unemphasise_action])

	def touch_ended(self, touch):
		if not MenuScene.touch_ended(self, touch):
			#if self.complete:
			self.show_menu('next level')

class PauseMenu(TwoButtonMenu):
	
	def __init__(self, tutorial):

		if tutorial:
			button_lhs=Button(tag='paused_tutorial_return', action='unpause')
			button_rhs=Button(tag='paused_tutorial_end', action='end tutorial')
			
			
			menu = 'paused_game'
			
		else:
			button_lhs=Button(tag='paused_game_return', action='unpause')
			button_rhs=Button(tag='paused_game_end', action='confirm quit')
			
			menu = 'paused_game'

		TwoButtonMenu.__init__(self, tag=menu,button_lhs=button_lhs,button_rhs=button_rhs, main_menu_button=False)
			
class LoseLifeMenu(OneButtonMenu):
	
	def __init__(self, lives):
		
		self.lives = lives
		infos = []
		infos.append(('life lost', '{0} lives remaining'.format(lives)))
						
		OneButtonMenu.__init__(self, tag='lose_life', button=Button(tag='try_again',action='try again'))

	def setup(self):
		
		OneButtonMenu.setup(self)
		
		label_font = (font.BUTTON, int(22*Scaler.Menu))
		
		self.lives_label = LabelNode(parent=self.menu_bg, font=label_font,color=palette.BASE_BG)
		
		self.lives_label.anchor_point = (0.5, 0)
		
		x = -22.0*Scaler.Menu
		y = 23.0*Scaler.Menu
		
		self.lives_label.position = (x, y)
		self.lives_label.text = str(self.lives)
					
class EndGameMenu(TwoButtonMenu):
	
	def __init__(self, score, pb):
		
		if pb:
			self.score_text = '{0} - new PB!'.format(score)
		else:
			self.score_text = '{0}'.format(score)
		
		lhs = Button(tag='game_over_restart',action='play from start')
		
		rhs = Button(tag='game_over_checkpoint',action='restart from checkpoint')
		
		TwoButtonMenu.__init__(self, tag='game_over',button_lhs=lhs,button_rhs=rhs,main_menu_button=True)

	def setup(self):
		
		TwoButtonMenu.setup(self)
		
		label_font = (font.BUTTON, int(30*Scaler.Menu))
		
		self.score_label = LabelNode(parent=self.menu_bg, font=label_font,color='#000000')
		
		self.score_label.anchor_point = (0.5, 0.5)
		
		y = 35 * Scaler.Menu
		
		self.score_label.position = (0, y)
		self.score_label.text = self.score_text
			
class CompletionScoringMenu(EndLevelMenu):
	
	def __init__(self, score, completion_bonus, lives_remaining_bonus):
		
		self.completion_bonus = completion_bonus
		self.lives_remaining_bonus = lives_remaining_bonus
		
		EndLevelMenu.__init__(self, level=-1, score=score, level_points=0, time_bonus=0, stars=0, check_point=False)

	def get_width(self):
		return 400

	def add_level_bonus(self, infos, level_points):
		infos.append(('completion bonus', star_text(self.completion_bonus)))
		return infos, self.get_index(infos)
	
	def add_time_bonus(self, infos, time_bonus):
		infos.append(('remaining lives bonus', star_text(self.lives_remaining_bonus)))
		return infos, self.get_index(infos)
	
	def get_title(self, level):
		return 'Game Complete'

	def get_next_title(self):
		return 'tap to proceed'

	def touch_ended(self, touch):
		if not MenuScene.touch_ended(self, touch):
			self.show_menu('completion menu')

class CompletionSpriteNode(SpriteNode):
	
	def __init__(self, game, parent, texture, get_x, scale,rotation_range=3.14, z_position=None):
		
		SpriteNode.__init__(self, parent=parent, texture=texture)
		
		if not z_position is None:
			self.z_position = z_position
			
		self.base_scale = scale
		self.game = game
		
		self.anchor_point=(0.5,0.5)
		
		self.set_scale()
		
		self.position = (get_x(self.size.w), self.get_new_y() + self.game.size.h*random()*0.5)
		self.get_x = get_x
		self.rotation_range = rotation_range
		
		self.set_rotation()
		self.set_speed()
	
	def set_scale(self):
		self.scale = self.base_scale = 0.9 + 0.2*random()
		self.max_dimension = max([self.size.w, self.size.h])
		self.min_height = -self.game.size.h*0.5-self.max_dimension
		
	def set_rotation(self):
		self.rotation = self.rotation_range * (0.5-random())
	
	def set_speed(self):
		self.speed = 0.5 + 0.5 * random()
	
	def get_new_y(self):
		return self.game.size.h*0.5 + self.max_dimension
		
	def update(self):
		
		y = self.position[1]
		
		if y < self.min_height:
			self.set_rotation()
			self.set_speed()
			self.set_scale()
			self.position = (self.get_x(self.size.w), self.get_new_y())
		else:
			self.position = (self.position[0], self.position[1]-self.speed)
		
class CompletionMenu(EndGameMenu):
	
	def __init__(self, game, score, pb):
		
		self.game = game
		
		buttons = ['main menu']
		
		self.pb = pb
			
		if pb:
			score_text = '{0} - new PB!'.format(score)
		else:
			score_text = '{0}'.format(score)
			
		infos = [('MapMan', 'Completed'),('Your Score', score_text)]
		
		MenuScene.__init__(self, 'Congratulations', buttons, infos, title_size=40)

	def get_width(self):
		return 400
	
	def update(self):
		for item in self.scrollers:
			item.update()
			
	def setup(self):
		
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		
		self.edge = 0.5 * (self.game.size.w- self.get_width())
		
		self.scroller_scale = float(self.get_width()) / float(self.game.size.w)
		
		self.scrollers = []
		
		self.add_scroller(Scaler.get_man_idle_path('front.png'), self.get_lhs, 0.5 * 3.14, 3000)
	
		self.add_scroller(Scaler.get_woman_idle_path('front.png'), self.get_rhs, 0.5 * 3.14,3000)
		
		for i in range(10):
			
			self.add_scroller(self.get_tile(), self.get_lhs)
			self.add_scroller(self.get_tile(), self.get_rhs)
		
		
	def get_lhs(self, width):
		return -(0.5 * self.get_width() + random() * (self.edge-width))-0.5*width

	def get_rhs(self, width):
		return -self.get_lhs(width)
	
	def get_tile(self):
		
		key = randint(1, 8)
		
		if key == 1:
			return Scaler.get_tile_path('blank1.png')
		elif key == 2:
			return Scaler.get_tile_path('show.png')
		elif key == 3:
			return Scaler.get_tile_path('life.png')
		elif key == 4:
			return Scaler.get_tile_path('sticky.png')
		if key == 5:
			return Scaler.get_tile_path('points.png')
		elif key == 6:
			return Scaler.get_tile_path('reverse.png')
		elif key == 7:
			return Scaler.get_tile_path('hide.png')
		elif key == 8:
			return Scaler.get_tile_path('death.png')
		else:
			return Scaler.get_tile_path('blank1.png')
			
	def add_scroller(self, texture, get_x, rotation_range=3.14,z_position=None):
		
		item = CompletionSpriteNode(self.game, parent=self.menu_bg,texture=texture, get_x=get_x, scale=self.scroller_scale,
		rotation_range=rotation_range,
		z_position=z_position)
		
		self.scrollers.append(item)
