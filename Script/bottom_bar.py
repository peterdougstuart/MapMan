# coding: utf-8

from scene import *
from effect import Effect
from timer import Timer
import font
from scaler import Scaler
from wrapping import WrappingLabelNode
				
class BottomBar (SpriteNode):
	
	def __init__(self, parent):
		
		SpriteNode.__init__(self,
											  parent=parent,
											  position=(0, 0),
											  size=(parent.size.w, 80 * Scaler.Bottom_bar)
											  )
											  
		self.centre_height = self.size.h*0.5
		
		self.color = '#1c1c1c'
		self.anchor_point = (0, 0)

		self.add_controls_message()
		self.add_tutorial_message()
		self.add_time_message()
		self.timer = Timer(self)
		self.effect = Effect(self)
	
	def hide(self):
		self.scale = 0
		
	def show(self):
		self.scale = 1
		
	def set_tutorial_text(self, text):
		self.tutorial_message.set_text(text, int(15*Scaler.Bottom_bar))

	def set_time_message(self,text,size=30):
		
		self.time_message_label_bottom.font = (font.BOTTOM_BAR, int(size*Scaler.Bottom_bar))
		
		self.time_message_label_bottom.text = text
	
	def set_controls_message(self,text,size=30):
		
		self.controls_message.set_text(text, int(size*Scaler.Bottom_bar))
		
	def add_controls_message(self):
		
		anchor_point = (0, 0.5)
		
		position = (87*Scaler.Bottom_bar, self.centre_height)
		
		target_width = self.size.w * 0.27
				
		self.controls_message = WrappingLabelNode(parent=self, anchor_point=anchor_point, position=position, target_width=target_width,
		font_type=font.BOTTOM_BAR)

	def add_tutorial_message(self):
		
		anchor_point = (0, 0.5)
		
		x_position = self.controls_message.position.x+self.controls_message.target_width+10*Scaler.Bottom_bar
		
		position = (x_position, self.centre_height)
		
		target_width = self.parent.size.w - x_position - 10 * Scaler.Bottom_bar
		
		self.tutorial_message = WrappingLabelNode(parent=self, anchor_point=anchor_point, position=position, target_width=target_width,
		font_type=font.BOTTOM_BAR)
		
	def add_time_message(self):
	
		self.time_message_label_bottom = LabelNode(position=(self.size.w * 0.75 + 10 * Scaler.Bottom_bar, self.centre_height), parent=self)
		self.time_message_label_bottom.anchor_point = (0.5, 0.5)
	

