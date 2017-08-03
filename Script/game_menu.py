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
from in_app import InApp

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
	
	def __init__(self, node, index):
		self.node = node
		self.on = False
		self.base_color = self.node.color
		self.base_font = self.node.font
		self.index = index
		
	def __call__(self):
		if not self.on:
			sound.play_effect('arcade:Powerup_3', 1, 1 + 1.0/8.0 * self.index)
			#self.node.color = '#e28c9b'
			self.node.font = (self.node.font[0], int(30*Scaler.get_scale()))
			self.on = True
		else:
			self.node.color = self.base_color
			self.node.font = self.base_font
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
		
		if len(text) > 1:
			self.node.info_label.text = text[1:]
		else:
			self.node.info_label.text = ''
		
		self.score_node.add_score()
		
class InfoNode (SpriteNode):
	
	def __init__(self, info, parent):
		
		SpriteNode.__init__(self, parent=parent)
		
		button_font = (font.BUTTON, int(20*Scaler.get_scale()))
		
		self.heading_label = LabelNode(info[0], font=button_font, color='#71c0e2', position=(0, 5), parent=self)
		
		self.info_label = LabelNode(info[1], font=button_font, color='#000000', position=(0, -20*Scaler.get_scale()), parent=self)
		
		if len(info) >= 3:
			self.heading_label.font = (button_font[0], info[2]*Scaler.get_scale())

		if len(info) >= 4:
			self.info_label.font = (button_font[0], info[3]*Scaler.get_scale())
			
		self.size = (self.parent.size.w * 0.8, self.heading_label.size.h + self.info_label.size.h)
		
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
		self.y_position_delta = y_position_delta*Scaler.get_scale()
		
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
		
		self.menu_bg = ShapeNode(bg_shape, position=(self.size.w/2,self.size.h/2+self.y_position_delta), color='#ffffff', parent=self)
		
		self.menu_bg.anchor_point = (0.5, 0.5)
		
		self.title_label = LabelNode(self.title, font=title_font, color='#ffffff', parent=self)
		
		self.title_label.anchor_point = (0.5, 0)
		
		self.buttons = []
		self.info_nodes = []
		
		for i, info in enumerate(self.infos):
			
			node = InfoNode(info, parent=self.menu_bg)
			
			node.anchor_point = (0.5, 1)
			
			node.position = 0, self.menu_bg.size.h/2 - (i+0.5) * info_delta
			
			self.info_nodes.append(node)

		for i, title in enumerate(self.button_titles):
			
			btn = ButtonNode(title, parent=self.menu_bg)
			
			btn.anchor_point = (0.5, 1)
			
			btn.position = 0, self.menu_bg.size.h/2 - (i+0.5) * button_delta - number_of_infos * info_delta
			
			self.buttons.append(btn)
			
		self.did_change_size()
		#self.menu_bg.scale = 0
		
		self.bg.alpha = 0
		self.bg.run_action(Action.fade_to(1))
		
		#self.background_gradient.alpha = 0
		#self.background_gradient.run_action(A.fade_to(1))
		
		self.background_color = 'white'
		
	def did_change_size(self):
		self.bg.size = self.size + (2, 2)*Scaler.get_scale()
		self.bg.position = self.size/2
		self.menu_bg.position = (self.size.w/2,self.size.h/2+self.y_position_delta)
		self.size/2
		self.title_label.position=(self.size.w/2, self.size.h/2+self.menu_bg.size.h/2-self.title_label.size.h * 0.2+self.y_position_delta)
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
				
					new_title = self.presenting_scene.menu_button_selected(btn.title)
				
					if new_title:
						btn.title = new_title
						btn.title_label.text = new_title

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
		
		MenuScene.__init__(self,'Credits', buttons, infos=infos, y_position_delta=-20)

class MainMenu(MenuScene):
	
	def __init__(self, high_score):
		
		self.high_score = high_score
		
		buttons = ['play', 'continue', 'tutorial', 'purchase', 'credits']
		
		infos = []
		
		MenuScene.__init__(self, '', buttons, infos, y_position_delta=-25)

	def setup(self):
		
		MenuScene.setup(self)
		
		self.score_label = ScoreLabelNode(parent=self.menu_bg, score=self.high_score, base_text='best score')
		
		man_texture = Texture(os.path.join('Man','Idle', 'MapMan-idle-FRONT-2.png'))
		
		self.man = SpriteNode(parent=self.menu_bg,texture=man_texture)
		self.man.anchor_point=(0,0)
		
		ratio = self.man.size.w / self.menu_bg.size.w
		
		ratio_target = 0.2
		
		self.man.scale = ratio_target / ratio
		
		self.man.position = (self.menu_bg.size.w/2 - 1.5 * self.man.size.x * self.man.scale, self.menu_bg.size.h/2)

class PurchaseMenu(MenuScene):
	
	def __init__(self):

		infos = []
		buttons = []
		
		if InApp.Instance.can_make_purchases:
			infos.append(('purchases enabled', ''))
		else:
			infos.append(('purchases disabled', ''))
		
		if InApp.Instance.products_received:
			for product in InApp.Instance.products:
				buttons.append(product.description)
		else:
			infos.append(('no items available', 'try again later'))
		
		buttons.append('main menu')
		
		MenuScene.__init__(self, 'Purchase', buttons, infos)
		
class EndLevelMenu(MenuScene):
	
	def __init__(self, level, score, level_points, time_bonus, stars, check_point):
		
		self.score = score
		
		buttons = []
		infos = []
		
		infos.append(('level bonus', font.STAR * level_points))
		
		infos.append(('time bonus', font.STAR * time_bonus))

		infos.append(('collected', font.STAR * stars))
		
		if check_point:
			infos.append(('checkpoint passed', ''))

		MenuScene.__init__(self, 'Level {0} Clear'.format(level), buttons, infos=infos, title_size=40)

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
		
		next_level_button = self.buttons[0]
		
		next_level_button.alpha = 0
		
		actions.append(Action.wait(0.2))
		
		actions += self.add_star_action(0)

		actions += self.add_star_action(1)
		
		actions += self.add_star_action(2)
		actions.append(Action.call(StartFade(next_level_button)))
		self.info_nodes[0].run_action(Action.sequence(actions))
	
	def add_star_action(self, index):
		
		actions = []
		
		actions.append(Action.wait(0.2))
		
		action = self.star_action(index)
		
		if action is not None:
			actions.append(action)
			
		return actions
		
	def star_action(self, index):
		
		node = self.info_nodes[index]
		count = len(node.info_label.text)
		
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
		
if __name__ == '__main__':
	
	#run(MainMenu(33))
	
	run(CreditsMenu())
	
	#run(EndGameMenu(50, True))
	
	#run(LoseLifeMenu())
