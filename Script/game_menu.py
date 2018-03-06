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
	
	def __init__(self, parent, score, base_text='score'):
		
		self.base_text = base_text
		
		button_font = (font.BUTTON, int(20*Scaler.Menu))
		
		LabelNode.__init__(self, text='', font=button_font, color='#ffffff', parent =parent)

		self.anchor_point = (0.5,0.5)
		
		self.position=(0, -parent.size.h/2-self.size.h)
		
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
		
class ButtonNode (LabelNode):
	
	def __init__(self, title, parent):
		
		self.title = title
		
		self.untouch_color = '#71c0e2'
		self.touch_color = '#e28c9b'
		
		text = title
		button_font = self.make_font()
		
		LabelNode.__init__(self, text, font=button_font, color=self.untouch_color, position=(0, 0), parent=parent)
		
		self.anchor_point = (0.5, 1)
		self.enabled = True
		
		self.spacer = None
	
	def make_font(self, scale=1):

		self.untouch_font_size = 20*Scaler.Menu*scale
		self.touch_font_size = 25*Scaler.Menu*scale
		
		button_font = (font.BUTTON, self.untouch_font_size)
		
		return button_font
	
	def set_font_scale(self, scale):
		self.font = self.make_font(scale)
		
	def add_spacer(self):
		
		self.spacer = LabelNode('—----',font=self.font, color=self.untouch_color, position=(0, 0), parent=self.parent)
		self.spacer.anchor_point = (0.5, 1)
		
		self.set_position(self.position)
		
	def set_position(self, position):
		
		self.position = position
		
		if not self.spacer is None:
			self.spacer.position = (self.position.x, self.position.y + self.size.h)
		
	def set_title(self, title):
		self.title = title
		self.text = title
		
	def disable(self):
		self.enabled = False
		self.color = '#aaaaaa'
		
	def touch(self):
		
		self.color = self.touch_color
		self.font = (font.BUTTON_PRESSED, self.touch_font_size)

	def untouch(self):
		
		self.color = self.untouch_color
		self.font = (font.BUTTON, self.untouch_font_size)
		
class MenuScene (Scene):
	
	def __init__(self, title, button_titles, infos=[], title_size=60, button_delta=None, info_delta=60):
		
		if button_delta is None:
			button_delta = 40
			
		Scene.__init__(self)

		self.info_delta = info_delta*Scaler.Menu
		self.button_delta = button_delta*Scaler.Menu
		
		self.title = title
		self.button_titles = button_titles
		self.infos = infos
		self.title_size = title_size*Scaler.Menu
	
	def update(self):
		# overloaded by menus with animated bits
		pass
		
	def above_height(self):
		if len(self.title_label.text) > 0:
			return self.title_label.size.h * 0.6
		else:
			return 0
	
	def below_height(self):
		return 0
	
	def total_height(self):
		
		height = self.menu_bg.size.h
		height += self.below_height()
		height += self.above_height()
		
		return height
		
	def center(self):
		
		total_height = self.total_height()
		space = 0.5 * (self.size.h - total_height)
		
		x = self.menu_bg.position[0]
		y = space + self.below_height() + self.menu_bg.size.h * 0.5
		
		new_position = (x, y)
		
		self.menu_bg.position = new_position
	
	def get_width(self):
		return 240
		
	def setup(self):
		
		title_font = (font.TITLE, self.title_size)
		
		self.number_of_buttons = len(self.button_titles)
		self.number_of_infos = len(self.infos)
				
		self.bg = SpriteNode(color=palette.BASE_BG, parent=self)

		self.background_gradient = Gradient(self)
		
		bg_shape = ui.Path.rounded_rect(0, 0, self.get_width()*Scaler.Menu, self.get_height(), 16*Scaler.Menu)
		
		bg_shape.line_width = 0
		
		self.menu_bg = ShapeNode(bg_shape, position=(self.size.w/2,self.size.h/2), color='#ffffff', parent=self)
		
		self.menu_bg.anchor_point = (0.5, 0.5)
		
		self.title_label = LabelNode(self.title, font=title_font, color='#ffffff', parent=self)
		
		self.title_label.anchor_point = (0.5, 0)
		
		self.buttons = []
		self.info_nodes = []
		
		for i, info in enumerate(self.infos):
			
			node = self.new_info_node(info, self.menu_bg)
			
			node.anchor_point = (0.5, 1)
			
			node.position = 0, self.menu_bg.size.h/2 - (i+0.5) * self.info_delta
			
			self.info_nodes.append(node)
		
		self.info_space = self.number_of_infos * self.info_delta
		
		for i, title in enumerate(self.button_titles):
			
			btn = self.new_button_node(self.menu_bg, title)
			
			btn.anchor_point = (0.5, 1)
			btn.set_position(self.button_position(i))
			
			self.buttons.append(btn)
			
		self.did_change_size()

		self.bg.alpha = 0
		self.bg.run_action(Action.fade_to(1))
	
	def get_height(self):
		return self.number_of_buttons * self.button_delta + self.number_of_infos * self.info_delta+10*Scaler.Menu

	def button_position(self, index):
		return (0, self.menu_bg.size.h/2 - (index+0.5) * self.button_delta - self.info_space)
		
	def new_button_node(self, parent, title):
		return ButtonNode(title, parent=parent)
		
	def new_info_node(self, info, parent):

		return InfoNode(info, parent=parent)

	def did_change_size(self):
		
		self.bg.size = self.size + (2*Scaler.Menu, 2*Scaler.Menu)
		self.bg.position = self.size/2
		
		self.center()
				
		self.title_label.position=(self.menu_bg.position[0], self.menu_bg.position[1]+self.menu_bg.size.h/2-self.title_label.size.h * 0.2)
		self.background_gradient.size=(self.size.w, self.size.h)
		
	def touch_began(self, touch):
		
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			if touch_loc in btn.frame and btn.enabled:
				btn.touch()
	
	def touch_ended(self, touch):
	
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			
			if btn.enabled:
				
				btn.untouch()
							
				if self.presenting_scene and touch_loc in btn.frame:
				
					self.show_menu(btn.title)
					return True
		
		return False
					
	def show_menu(self, menu):
		self.presenting_scene.menu_button_selected(menu)
	 	
class RestartMenu(MenuScene):
	
	def __init__(self, check_points):
		
		buttons = []
		self.enables = []
		
		sorted_check_points = sorted(check_points)
		
		for level in sorted(check_points):
			
			check_point = check_points[level]
			buttons.append('L{0}'.format(check_point.level))
			self.enables.append(check_point.complete)
			
		buttons.append('main menu')
		infos = []
		
		infos.append(('select checkpoint', 'to restart game'))
		
		MenuScene.__init__(self, 'Restart', buttons, infos=infos, button_delta=65)

	def get_height(self):
		return MenuScene.get_height(self) * 0.31
	
	def get_width(self):
		return 400
		
	def button_position(self, index):
		
		if index < 12:
			if index < 4:
				x = -100
			elif index < 8:
				x = 0
				index -= 4
			else:
				x = 100
				index -= 8
			extra = 0.0
		else:
			x = 0
			index = 4
			extra = -0.0
			
		return (x, self.menu_bg.size.h/2 - (index+0.5) * self.button_delta * (0.70+extra) - self.info_space*0.85)
		
	def setup(self):
			
		MenuScene.setup(self)
		
		self.info_nodes[0].heading_label.color = self.info_nodes[0].info_label.color
		
		for i in range(len(self.enables)):
			if not self.enables[i]:
				self.buttons[i].disable()
		
		for i in range(len(self.buttons)-1):
			self.buttons[i].set_font_scale(1.5)

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
		
class CreditsMenu(MenuScene):
	
	def __init__(self):
		
		buttons = ['main menu']
		infos = []
		
		infos.append(('creator', 'Peter Stuart'))
		infos.append(('art', 'Fred Mangan'))
		infos.append(('music', 'David Sedgwick'))
		infos.append(('info', 'www.mapmangame.com'))
		
		MenuScene.__init__(self,'Credits', buttons, infos=infos)

class CheckpointsPurchaseRequiredMenu(MenuScene):
	
	def __init__(self):
		
		buttons = ['purchase menu', 'main menu']
		infos = []
		
		infos.append(('purchase required', 'to enable checkpoints'))
		
		MenuScene.__init__(self,'Puchase Required', buttons, infos=infos, button_delta=50, title_size=40)

	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		self.buttons[0].set_font_scale(1.7)
		self.buttons[1].set_font_scale(1.1)

	def get_width(self):
		return 400
		
class OptionsMenu(MenuScene):
	
	def __init__(self, playing_position):
		
		buttons = [playing_position, 'main menu']
		infos = []
		
		infos.append(('playing position', 'click to toggle'))
		
		MenuScene.__init__(self,'Options', buttons, infos=infos)

	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		
	def update_playing_position(self, playing_position):
		self.buttons[0].set_title(playing_position)
		
class FirstPlayMenu(MenuScene):
	
	def __init__(self):
		
		buttons = ['take tutorial', 'play game']
		infos = []
		
		infos.append(('first time,', 'take tutorial?'))
		
		MenuScene.__init__(self,'Newbie', buttons, infos=infos)
	
	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		
class MainMenu(MenuScene):
	
	def __init__(self, high_score):
		
		self.high_score = high_score
		
		buttons = ['play from start', 'restart from checkpoint', 'tutorial']
		
		if offer_active():
			buttons.append('purchase - price reduction')
		else:
			buttons.append('purchase')
		
		buttons += ['credits', 'options']
		
		self.button_count = len(buttons)
		
		infos = []
		
		self.man = None
		self.score_label = None
		
		MenuScene.__init__(self, '', buttons, infos)

	def button_position(self, index):
		
		if index < (self.button_count - 2):
			return MenuScene.button_position(self, index)
			
		else:
			
			position = MenuScene.button_position(self, self.button_count - 2)
			
			width = self.get_width()
			
			if index == (self.button_count - 2):
				return (position[0]-60*Scaler.Menu, position[1])
			else:
				return (position[0]+60*Scaler.Menu, position[1])

	def get_height(self):
		
		height = MenuScene.get_height(self)
		
		return height - self.button_delta
			
	def get_width(self):
		return 400
		
	def above_height(self):

		if self.man is not None:
			return (self.man.size.h * self.man.scale) * 0.8
		else:
			return 0
		
	def below_height(self):

		if self.score_label is not None:
			return self.score_label.size.h
		else:
			return 0
		
	def setup(self):
		
		MenuScene.setup(self)
		
		self.score_label = ScoreLabelNode(parent=self.menu_bg, score=self.high_score, base_text='best score')
		
		man_texture = Texture(Scaler.get_man_idle_path('front.png'))
		
		self.man = SpriteNode(parent=self.menu_bg,texture=man_texture)
		self.man.anchor_point=(0,0)
		
		ratio = self.man.size.w / self.menu_bg.size.w
		
		ratio_target = 0.15
		
		self.man.scale = ratio_target / ratio
		
		self.man.position = (self.menu_bg.size.w/2 - 1.5 * self.man.size.w * self.man.scale, self.menu_bg.size.h/2)
		
		self.did_change_size()

class PurchaseMenuBase(MenuScene):
	
	def get_width(self):
		return 400
		
	def new_info_node(self, info, parent):
		return WrappingInfoNode(info, parent=parent)
		
class ConfirmProductMenu(PurchaseMenuBase):
	
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
		
		MenuScene.__init__(self, header, buttons, infos=infos,button_delta=50)

	def show_menu(self, menu):
	 	
		if 'okay' in menu.lower():
			self.presenting_scene.purchase_product(self.product)
		elif 'cancel' in menu.lower():
			self.presenting_scene.menu_button_selected('purchase menu')
		else:
			self.presenting_scene.menu_button_selected(menu)

	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		self.buttons[0].set_font_scale(1.4)
		self.buttons[1].set_font_scale(1.4)
		
class MakePurchaseMenu(PurchaseMenuBase):
	
	def __init__(self, product):
		
		self.product = product
		
		infos = [(product.title, 'processing')]
		buttons = ['...']
		
		MenuScene.__init__(self, 'Thanks', buttons, infos=infos, button_delta=60)
		
	def setup(self):
		MenuScene.setup(self)
		self.buttons[0].set_font_scale(1.7)
		ProductsController.get().purchase(self.product, self)
		
	def set_button(self, success):
		
		button = self.buttons[0]
		
		if success:
			button.set_title('main menu')
		else:
			button.set_title('purchase menu')
	
	def purchase_successful(self, product_identifier):
		
		self.set_message('successful')
		self.set_button(True)

	def purchase_restored(self, product_identifier):
		
		self.set_message('restored')
		self.set_button(True)

	def purchase_failed(self, product_identifier):
		self.title_label.text = 'Sorry'
		self.set_message('failed')
		self.set_button(False)
	
	def set_message(self, message):
		self.info_nodes[0].info_label.text = message
		
class PurchaseMenu(PurchaseMenuBase):
	
	def __init__(self):
		
		products_controller = ProductsController.get()
		
		infos = []
		buttons = []
		
		self.can_purchase = False
		
		if not products_controller.enabled:
			
			infos.append(('purchases disabled', ''))
			
		else:
			
			if products_controller.validated:
			
				self.checkpoints = products_controller.checkpoints
				
				if self.checkpoints.valid:
					
					if self.checkpoints.purchased:
							
						price = font.TICK
						
					else:
							
						price = self.checkpoints.price
						self.can_purchase = True
						
					button_title = '{0}: {1}'.format(self.checkpoints.title, price)
						
					buttons.append(button_title)
					
					infos.append(('', self.checkpoints.title.lower()+': '+ self.checkpoints.description))
						
				else:
				
					infos.append(('checkpoints', 'product invalid'))
				
			else:
				
				infos.append(('could not validate', 'try again later'))
		
		buttons.append('main menu')
			
		MenuScene.__init__(self, 'Purchase', buttons, infos, button_delta = 60, info_delta=150)
			
	def get_width(self):
		return 400
		
	def new_button_node(self, parent, title):
		
		button = MenuScene.new_button_node(self, parent, title)
		
		if 'menu' not in title:
			if not self.can_purchase:
				button.disable()
		
		return button
	
	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		self.buttons[0].set_font_scale(1.7)
		
	def show_menu(self, menu):
	 	
	 	if menu.lower() in ['main menu']:
	 		self.presenting_scene.menu_button_selected(menu)
	 		
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
		
		self.score_label = ScoreLabelNode(parent=self.menu_bg, score=self.score)
		
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

class PauseMenu(MenuScene):
	
	def __init__(self, tutorial):
		
		buttons = ['unpause']
		
		if tutorial:
			buttons.append('end tutorial')
		else:
			buttons.append('end game')
		
		infos = [('tilt to move MapMan','tap game to pause')]

		MenuScene.__init__(self, 'Paused', buttons, infos=infos, title_size=60)

	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		self.buttons[0].set_font_scale(1.7)
		self.buttons[1].set_font_scale(1.0)
		
	def button_position(self, index):
		
		position = MenuScene.button_position(self, index)
			
		if index > 0:
				
			return (position[0], position[1]-0.5*self.button_delta)
			
		else:
			
			return (position[0], position[1]-0.1*self.button_delta)

	def get_height(self):
		
		height = MenuScene.get_height(self)
		
		return height + self.button_delta

	def touch_ended(self, touch):
		if not MenuScene.touch_ended(self, touch):
			self.show_menu('unpause')
			
class LoseLifeMenu(MenuScene):
	
	def __init__(self, lives):
		
		buttons = ['try again']

		infos = []
		infos.append(('life lost', '{0} lives remaining'.format(lives)))
						
		MenuScene.__init__(self, 'Oh No!', buttons, infos=infos, title_size=60)

	def touch_ended(self, touch):
		if not MenuScene.touch_ended(self, touch):
			self.show_menu('try again')
					
class EndGameMenu(MenuScene):
	
	def __init__(self, score, pb):
		
		buttons = ['main menu']
		
		self.pb = pb
		
		if pb:
			score_text = '{0} - new PB!'.format(score)
		else:
			score_text = '{0}'.format(score)
			
		infos = [('Your Score', score_text)]
		
		MenuScene.__init__(self, 'Game Over', buttons, infos, title_size=40)
		
	def get_width(self):
		return 250

			
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
