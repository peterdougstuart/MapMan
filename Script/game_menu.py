# coding: utf-8
# This module implements the menu that is used by all game examples. It doesn't do much by itself.

from scene import *
import ui
import sound
import os
import objc_util

A = Action

class InfoNode (SpriteNode):
	
	def __init__(self, info, parent):
		
		SpriteNode.__init__(self, parent=parent)
		
		button_font = ('Courier', 20)
		
		self.heading_label = LabelNode(info[0], font=button_font, color='#71c0e2', position=(0, 5), parent=self)
		
		self.info_label = LabelNode(info[1], font=button_font, color='#000000', position=(0, -20), parent=self)
		
		if len(info) >= 3:
			self.heading_label.font = (button_font[0], info[2])

		if len(info) >= 4:
			self.info_label.font = (button_font[0], info[3])
			
		self.size = (self.parent.size.w * 0.8, self.heading_label.size.h + self.info_label.size.h)
		
class ButtonNode (SpriteNode):
	
	def __init__(self, title, parent):
		
		SpriteNode.__init__(self, parent=parent)
		
		button_font = ('Courier', 20)
		
		self.label = LabelNode(title, font=button_font, color='#71c0e2', position=(0, 0), parent=self)
		
		self.label.anchor_point = (0.5,0.5)
		
		self.title = title
		
		self.size = (self.parent.size.w * 0.9, self.label.size.h*1.25)

class MenuScene (Scene):
	
	def __init__(self, title, button_titles, infos=[], title_size=60, y_position_delta=0):
		
		Scene.__init__(self)
		
		self.title = title
		self.button_titles = button_titles
		self.infos = infos
		self.title_size = title_size
		self.y_position_delta = y_position_delta
		
	def setup(self):
		
		title_font = ('Avenir Rounded Bold', self.title_size)
		
		info_delta = 64
		button_delta = 40
		
		number_of_buttons = len(self.button_titles)
		number_of_infos = len(self.infos)
				
		self.bg = SpriteNode(color='#71c0e2', parent=self)

		background_texture = Texture(os.path.join('Gradients', 'MapMan-background-TRANSPARENCY.png'))
		
		self.background_gradient = SpriteNode(position=(0,0), parent=self)
		self.background_gradient.anchor_point=(0,0)
		
		self.background_gradient.texture = background_texture
		
		bg_shape = ui.Path.rounded_rect(0, 0, 240, number_of_buttons * button_delta + number_of_infos * info_delta+5, 16)
		
		bg_shape.line_width = 0
		
		self.menu_bg = ShapeNode(bg_shape, position=(self.size.w/2,self.size.h/2+self.y_position_delta), color='#ffffff', parent=self)
		
		self.menu_bg.anchor_point = (0.5, 0.5)
		
		self.title_label = LabelNode(self.title, font=title_font, color='#ffffff', parent=self)
		
		self.title_label.anchor_point = (0.5, 0)
		
		self.buttons = []
		
		for i, info in enumerate(self.infos):
			
			node = InfoNode(info, parent=self.menu_bg)
			
			node.anchor_point = (0.5, 1)
			
			node.position = 0, self.menu_bg.size.h/2 - (i+0.5) * info_delta

		for i, title in enumerate(self.button_titles):
			
			btn = ButtonNode(title, parent=self.menu_bg)
			
			btn.anchor_point = (0.5, 1)
			
			btn.position = 0, self.menu_bg.size.h/2 - (i+0.5) * button_delta - number_of_infos * info_delta
			
			self.buttons.append(btn)
			
		self.did_change_size()
		#self.menu_bg.scale = 0
		
		self.bg.alpha = 0
		self.bg.run_action(A.fade_to(1))
		#self.background_gradient.alpha = 0
		#self.background_gradient.run_action(A.fade_to(1))
		
		self.background_color = 'white'
		
	def did_change_size(self):
		self.bg.size = self.size + (2, 2)
		self.bg.position = self.size/2
		self.menu_bg.position = (self.size.w/2,self.size.h/2+self.y_position_delta)
		self.size/2
		self.title_label.position=(self.size.w/2, self.size.h/2+self.menu_bg.size.h/2-self.title_label.size.h * 0.2+self.y_position_delta)
		self.background_gradient.size=(self.size.w, self.size.h)
		
	def touch_began(self, touch):
		
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			
			if touch_loc in btn.frame:
				
				btn.label.color = '#e28c9b'
				btn.label.font = (btn.label.font[0], 25)
	
	def touch_ended(self, touch):
	
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		
		for btn in self.buttons:
			
			btn.label.color = '#71c0e2'
			btn.label.font = (btn.label.font[0], 20)
							
			if self.presenting_scene and touch_loc in btn.frame:
				
				new_title = self.presenting_scene.menu_button_selected(btn.title)
				
				if new_title:
					btn.title = new_title
					btn.title_label.text = new_title

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
		
		buttons = ['play', 'tutorial', 'credits']
		
		infos = []
		infos.append(('MapMan', 'Prepare to be AmazeMazed', 30, 15))
		
		MenuScene.__init__(self, '', buttons, infos, y_position_delta=-25)

	def setup(self):
		
		MenuScene.setup(self)
		
		button_font = ('Courier', 20)
		score_text = 'best score {0} {1} {0}'.format(unichr(9733), self.high_score)
		
		self.score_label = LabelNode(score_text, font=button_font, color='#ffffff',  parent=self.menu_bg)
		
		self.score_label.anchor_point = (0.5,0.5)
		
		self.score_label.position=(0, -self.menu_bg.size.h/2-self.score_label.size.h)
		
		man_texture = Texture(os.path.join('Man','Idle', 'MapMan-idle-FRONT-2.png'))
		
		self.man = SpriteNode(parent=self.menu_bg,texture=man_texture)
		self.man.anchor_point=(0,0)
		
		ratio = self.man.size.w / self.menu_bg.size.w
		
		ratio_target = 0.2
		
		self.man.scale = ratio_target / ratio
		
		self.man.position = (self.menu_bg.size.w/2 - 1.5 * self.man.size.x * self.man.scale, self.menu_bg.size.h/2)
		
class EndLevelMenu(MenuScene):
	
	def __init__(self, level, level_points, time_bonus, stars):
		
		buttons = ['Play Next Level']

		infos = []
		infos.append(('level bonus', str(level_points)))
		infos.append(('time bonus', str(time_bonus)))
		infos.append(('collected', str(stars)))
						
		MenuScene.__init__(self, 'Level {0} Clear'.format(level), buttons, infos=infos, title_size=40)

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
