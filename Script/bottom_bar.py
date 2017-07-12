# coding: utf-8

from scene import *
from effect import Effect
from timer import Timer

class WrappingLabelNode(LabelNode):
	
	def __init__(self, parent, target_width, position, anchor_point):
		
		LabelNode.__init__(self, parent=parent, position=position, anchor_point=anchor_point, text='')
		
		self.target_width = target_width
		
	def set_text(self, text, size):
		
		text = text.replace('\n',' ')
		multi = ''
		
		self.font = (BottomBar.FONT, size)
		
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
				
class BottomBar (object):
	
	FONT = 'Avenir Next'
	
	def __init__(self, parent):
		
		self.parent = parent
		self.add_background()
		self.add_controls_message()
		self.add_tutorial_message()
		self.add_time_message()
		self.timer = Timer(parent)
		self.effect = Effect(parent)
				
	def set_tutorial_text(self, text):
		self.tutorial_message.set_text(text, 15)
		
	def add_background(self):
		self.height = 85
		self.top_bg = SpriteNode(parent=self.parent, position=(0, self.height))
		self.top_bg.color = '#1c1c1c'
		self.top_bg.size = self.parent.size.w, self.height
		self.top_bg.anchor_point = (0, 1)
		
	def set_time_message(self,text,size=30):
		
		self.time_message_label_bottom.font = (BottomBar.FONT, size)
		
		self.time_message_label_bottom.text = text
	
	def set_controls_message(self,text,size=30):
		
		self.controls_message.set_text(text, size)
		
	def add_controls_message(self):
		
		anchor_point = (0, 0.5)
		
		position = (87, self.height/2)
		
		target_width = self.parent.size.w * 0.33
				
		self.controls_message = WrappingLabelNode(parent=self.parent, anchor_point=anchor_point, position=position, target_width=target_width)

	def add_tutorial_message(self):
		
		anchor_point = (0, 0.5)
		
		x_position = self.controls_message.position.x+self.controls_message.target_width+10
		
		position = (x_position, self.height/2)
		
		target_width = self.parent.size.w - x_position - 10
		
		self.tutorial_message = WrappingLabelNode(parent=self.parent, anchor_point=anchor_point, position=position, target_width=target_width)
		
	def add_time_message(self):
	
		self.time_message_label_bottom = LabelNode(position=(self.parent.size.w-100, 42.5), parent=self.parent)
	

