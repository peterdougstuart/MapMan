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
		
		button_font = (font.BUTTON, int(20*Scaler.get_scale()))
		
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
			
			sound.play_effect('arcade:Powerup_3', 0.5, (1 + 1.0/8.0 * self.index))
			
			for i in range(len(self.nodes)):
				node = self.nodes[i]
				#node.color = '#e28c9b'
				node.font = (node.font[0], int(30*Scaler.get_scale()))
			
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
		
		sound.play_effect('game:Ding_3')
		
		points = extract_stars(text)
		
		self.node.info_label.text = star_text(points-1)
		
		self.score_node.add_score()
		
class InfoNode (SpriteNode):
	
	def __init__(self, info, parent):
		
		SpriteNode.__init__(self, parent=parent)
		
		button_font = (font.BUTTON, int(20*Scaler.get_scale()))
		
		self.heading_label = LabelNode(info[0], font=button_font, color='#71c0e2', position=(0, 5), parent=self)
		
		self.info_label = self.new_info_label(info[1], font=button_font, color='#000000', position=(0, -20*Scaler.get_scale()), parent=self)
		
		if len(info) >= 3:
			self.heading_label.font = (button_font[0], info[2]*Scaler.get_scale())

		if len(info) >= 4:
			self.info_label.font = (button_font[0], info[3]*Scaler.get_scale())
			
		self.size = (self.parent.size.w * 0.8, self.heading_label.size.h + self.info_label.size.h)

	def new_info_label(self, text, font, color, position, parent):
		return LabelNode(text, font=font, color=color, position=position, parent=parent)

class WrappingInfoNode(InfoNode):

	def new_info_label(self, text, font, color, position, parent):
		
		node = WrappingLabelNode(parent=parent, anchor_point=(0.5, 0.5), position=position,
		target_width=parent.parent.size.w,
		font_type=font[0],
		color=color)
		
		node.set_text(text, font[1])
		
		return node
		
class ButtonNode (LabelNode):
	
	def __init__(self, title, parent):
		
		self.title = title
		
		self.untouch_color = '#71c0e2'
		self.touch_color = '#e28c9b'
		self.untouch_font_size = 20*Scaler.get_scale()
		self.touch_font_size = 25*Scaler.get_scale()
		
		button_font = (font.BUTTON, self.untouch_font_size)
		
		text = title
		
		while len(text) < 20:
			text = ' {0} '.format(text)
			
		LabelNode.__init__(self, text, font=button_font, color=self.untouch_color, position=(0, 0), parent=parent)
		
		self.anchor_point = (0.5,1)
		self.enabled = True
	
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
	
	def __init__(self, title, button_titles, infos=[], title_size=60, y_position_delta=0):
		
		Scene.__init__(self)
		
		self.title = title
		self.button_titles = button_titles
		self.infos = infos
		self.title_size = title_size*Scaler.get_scale()

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
		
	def setup(self):
		
		title_font = (font.TITLE, self.title_size)
		
		info_delta = 60*Scaler.get_scale()
		button_delta = 40*Scaler.get_scale()
		
		number_of_buttons = len(self.button_titles)
		number_of_infos = len(self.infos)
				
		self.bg = SpriteNode(color=palette.BASE_BG, parent=self)

		self.background_gradient = Gradient(self)
		
		bg_shape = ui.Path.rounded_rect(0, 0, 240*Scaler.get_scale(), number_of_buttons * button_delta + number_of_infos * info_delta+10*Scaler.get_scale(), 16*Scaler.get_scale())
		
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
			
			node.position = 0, self.menu_bg.size.h/2 - (i+0.5) * info_delta
			
			self.info_nodes.append(node)

		for i, title in enumerate(self.button_titles):
			
			btn = self.new_button_node(self.menu_bg, title)
			
			btn.anchor_point = (0.5, 1)
			
			btn.position = 0, self.menu_bg.size.h/2 - (i+0.5) * button_delta - number_of_infos * info_delta
			
			self.buttons.append(btn)
			
		self.did_change_size()

		self.bg.alpha = 0
		self.bg.run_action(Action.fade_to(1))
	
	def new_button_node(self, parent, title):
		return ButtonNode(title, parent=parent)
		
	def new_info_node(self, info, parent):

		return InfoNode(info, parent=parent)

	def did_change_size(self):
		
		self.bg.size = self.size + (2, 2)*Scaler.get_scale()
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
	 	
class ContinueMenu(MenuScene):
	
	def __init__(self, check_points):
		
		buttons = []
		self.enables = []
		
		for level in sorted(check_points):
			
			check_point = check_points[level]
			buttons.append('Checkpoint - L{0}'.format(check_point.level))
			self.enables.append(check_point.complete)
			
		buttons.append('main menu')
		infos = []
		
		infos.append(('select checkpoint', ''))
		
		MenuScene.__init__(self,'Continue', buttons, infos=infos, y_position_delta=-20)
		
	def setup(self):
			
		MenuScene.setup(self)
			
		for i in range(len(self.enables)):
			if not self.enables[i]:
				self.buttons[i].disable()
		
class CreditsMenu(MenuScene):
	
	def __init__(self):
		
		buttons = ['main menu']
		infos = []
		
		infos.append(('creator', 'Peter Stuart'))
		infos.append(('art', 'Fred Mangan'))
		infos.append(('music', 'David Sedgwick'))
		infos.append(('info', 'www.mapmangame.com'))
		
		MenuScene.__init__(self,'Credits', buttons, infos=infos)

class PurchaseToPlayMenu(MenuScene):
	
	def __init__(self):
		
		buttons = ['okay']
		infos = []
		
		infos.append(('purchase required', self.get_description()))

		MenuScene.__init__(self,'More?', buttons, infos=infos)

	def get_description(self):
		return "to advance level"
		
	def setup(self):
		MenuScene.setup(self)
		self.info_nodes[0].heading_label.color = '#000000'
		
class PurchaseToCheckpointMenu(PurchaseToPlayMenu):
	
	def get_description(self):
		return "to use checkpoints"
		
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
	
	def __init__(self, high_score, purchase_to_play = False):
		
		self.high_score = high_score
		self.purchase_to_play = purchase_to_play
		
		if self.purchase_to_play:
			buttons = ['resume', 'new game']
		else:
			buttons = ['play', 'continue', 'tutorial']
			
		buttons += ['purchase', 'credits']
		
		infos = []
		
		self.man = None
		self.score_label = None
		
		MenuScene.__init__(self, '', buttons, infos)

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
		
		man_texture = Texture(os.path.join('Man','Idle', 'MapMan-idle-FRONT-2.png'))
		
		self.man = SpriteNode(parent=self.menu_bg,texture=man_texture)
		self.man.anchor_point=(0,0)
		
		ratio = self.man.size.w / self.menu_bg.size.w
		
		ratio_target = 0.2
		
		self.man.scale = ratio_target / ratio
		
		self.man.position = (self.menu_bg.size.w/2 - 1.5 * self.man.size.w * self.man.scale, self.menu_bg.size.h/2)
		
		self.did_change_size()

class ConfirmProductMenu(MenuScene):
	
	def __init__(self, product):
		
		self.product = product
		
		if product.can_purchase:
			buttons = ['confirm purchase']
		else:
			buttons = []
		
		buttons.append('purchase menu')
		
		infos = []
		
		if product.can_purchase:
			description = product.description
			header = 'Confirm'
			title = 'Buy {0}'.format(product.title)
		else:
			description = product.why_cant_purchase
			header = 'Cannot'
			title = product.title
			
		infos.append((title, description))
		
		MenuScene.__init__(self, header, buttons, infos=infos)

	def new_info_node(self, info, parent):
		return WrappingInfoNode(info, parent=parent)

	def show_menu(self, menu):
	 	
	 	if menu.lower() in ['main menu', 'purchase menu']:
	 		self.presenting_scene.menu_button_selected(menu)
	 	else:
			self.presenting_scene.purchase_product(self.product)

class MakePurchaseMenu(MenuScene):
	
	def __init__(self, product, purchase_to_play=False):
		
		self.product = product
		self.purchase_to_play = purchase_to_play
		
		infos = [(product.title, 'processing')]
		buttons = ['...']
		
		MenuScene.__init__(self, 'Thanks', buttons, infos=infos)
		
	def setup(self):
		MenuScene.setup(self)
		ProductsController.get().purchase(self.product, self)
	
	def set_button(self, success):
		
		check_points = (self.product.title.lower() == 'checkpoints')
		
		button = self.buttons[0]
		
		if (not self.purchase_to_play) or (not success) or check_points:
			button.set_title('purchase menu')
		else:
			button.set_title('resume game')
			
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
		
class PurchaseMenu(MenuScene):
	
	def __init__(self):
		
		products_controller = ProductsController.get()
		
		self.products = {}
		
		infos = []
		buttons = []
		
		if not products_controller.enabled:
			
			infos.append(('purchases disabled', ''))
			
		else:
			
			if products_controller.validated:
			
				for product in products_controller.get_products():
							
					if product.purchased:
							
						price = font.TICK
						
					else:
							
						price = product.price
						
					button_title = '{0}: {1}'.format(product.title, price)
						
					buttons.append(button_title)
						
					self.products[button_title] = 	product
					
			else:
				
				infos.append(('could not validate', 'try again later'))
			
		buttons.append('main menu')
		
		MenuScene.__init__(self, 'Purchase', buttons, infos)

	def new_button_node(self, parent, title):
		
		button = MenuScene.new_button_node(self, parent, title)
		
		if not title in self.products:
			return button
			
		product = self.products[title]
		
		if not product.can_purchase:
			button.disable()
		
		return button
			
	def show_menu(self, menu):
	 	
	 	if menu.lower() == 'main menu':
	 		self.presenting_scene.menu_button_selected(menu)
	 		
	 	else:
	 		
			product = self.products[menu]
			self.presenting_scene.product_selected(product)
	 	
class EndLevelMenu(MenuScene):
	
	def __init__(self, level, score, level_points, time_bonus, stars, check_point):
		
		self.complete = False
		self.score = score
		self.check_point = check_point
		self.stars = stars
		
		self.score_label = None
		self.next_level_button = None
		
		buttons = []
		infos = []
		
		infos.append(('level bonus', star_text(level_points)))
		
		infos.append(('time bonus', star_text(time_bonus)))
		
		if self.stars > 0:
			infos.append(('collected', star_text(stars)))
		
		if self.check_point:
			infos.append(('checkpoint', 'passed'))

		MenuScene.__init__(self, 'Level {0} Clear'.format(level), buttons, infos=infos, title_size=40)

	def below_height(self):
		
		height = 0
		
		if self.score_label is not None:
			height += self.score_label.size.h

		if self.next_level_button is not None:
			height += self.next_level_button.size.h
			
		return height
			
	def setup(self):
		
		MenuScene.setup(self)
		
		self.score_label = ScoreLabelNode(parent=self.menu_bg, score=self.score)
		
		btn = ButtonNode('play next level', parent=self.menu_bg)
		
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
		
		actions += self.add_star_action(0)

		actions += self.add_star_action(1)
		
		if self.stars > 0:
			actions += self.add_star_action(2)
		
		if self.check_point:
			
			index = len(self.info_nodes) - 1
			
			self.info_nodes[index].info_label.color = '#71c0e2'
			
			items = [self.info_nodes[index].heading_label, self.info_nodes[index].info_label]
			
			emphasise = EmphasiseText(items, index)
			
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
		
		stars = Action.repeat(star_and_wait, count)
		
		unemphasise_action = Action.call(emphasise)
		
		return Action.sequence([emphasise_action, Action.wait(0.2), stars, unemphasise_action])

	def touch_ended(self, touch):
		if not MenuScene.touch_ended(self, touch):
			if self.complete:
				self.show_menu('next level')
					
class LoseLifeMenu(MenuScene):
	
	def __init__(self, lives):
		
		buttons = ['Try Again']

		infos = []
		infos.append(('life lost', '{0} lives remaining'.format(lives)))
						
		MenuScene.__init__(self, 'Oh No!', buttons, infos=infos, title_size=60)
		
class EndGameMenu(MenuScene):
	
	def __init__(self, score, pb):
		
		buttons = ['main menu']
		
		if pb:
			buttons = ['tweet PB'] + buttons
		
		if pb:
			score_text = '{0} - new PB!'.format(score)
		else:
			score_text = '{0}'.format(score)
			
		infos = [('Your Score', score_text)]
		
		MenuScene.__init__(self, 'Game Over', buttons, infos, title_size=40)
		
