# coding: utf-8

from scene import *
from effect import Effect
from timer import Timer
import font
from scaler import Scaler

class WrappingLabelNode(LabelNode):
	
	def __init__(self, parent, target_width, position, anchor_point):
		
		LabelNode.__init__(self, parent=parent, position=position, text='')
		
		self.anchor_point=anchor_point
		
		self.target_width = target_width
		
	def set_text(self, text, size):
		
		text = text.replace('\n',' ')
		multi = ''
		
		self.font = (font.BOTTOM_BAR, size)
		
		words = text.split(' ')
			
		for word in words:
			
			if len(multi) > 0:
				trial = multi + ' ' + word
			else:
				trial = word
			
			self.text  = trial
			
			if self.bbox.w > self.target_width:
				multi += ('\n' + word)
				self.text = multi
			else:
				multi = trial
				
class BottomBar (SpriteNode):
	
	def __init__(self, parent):
		
		SpriteNode.__init__(self,
											  parent=parent,
											  position=(0, 0),
											  size=(parent.size.w, 80 * Scaler.get_scale())
											  )
											  
		self.color = '#1c1c1c'
		self.anchor_point = (0, 0)

		self.add_controls_message()
		self.add_tutorial_message()
		self.add_time_message()
		self.timer = Timer(self)
		self.effect = Effect(self)
				
	def set_tutorial_text(self, text):
		self.tutorial_message.set_text(text, int(15*Scaler.get_scale()))

	def set_time_message(self,text,size=30):
		
		self.time_message_label_bottom.font = (font.BOTTOM_BAR, int(size*Scaler.get_scale()))
		
		self.time_message_label_bottom.text = text
	
	def set_controls_message(self,text,size=30):
		
		self.controls_message.set_text(text, int(size*Scaler.get_scale()))
		
	def add_controls_message(self):
		
		anchor_point = (0, 0.5)
		
		position = (87*Scaler.get_scale(), self.size.h/2)
		
		target_width = self.size.w * 0.27
				
		self.controls_message = WrappingLabelNode(parent=self, anchor_point=anchor_point, position=position, target_width=target_width)

	def add_tutorial_message(self):
		
		anchor_point = (0, 0.5)
		
		x_position = self.controls_message.position.x+self.controls_message.target_width+10*Scaler.get_scale()
		
		position = (x_position, self.size.h/2)
		
		target_width = self.parent.size.w - x_position - 10*Scaler.get_scale()
		
		self.tutorial_message = WrappingLabelNode(parent=self, anchor_point=anchor_point, position=position, target_width=target_width)
		
	def add_time_message(self):
	
		self.time_message_label_bottom = LabelNode(position=(self.size.w-100*Scaler.get_scale(), 42.5*Scaler.get_scale()), parent=self)
	

