from scene import LabelNode
import font

class WrappingLabelNode(LabelNode):
	
	def __init__(self, parent, target_width, position, anchor_point, font_type, color='#ffffff'):
		
		LabelNode.__init__(self, parent=parent, position=position, text='')
		
		self.anchor_point=anchor_point
		
		self.target_width = target_width
		self.font_type = font_type
		
		self.color = color
		
	def set_text(self, text, size):
		
		text = text.replace('\n',' ')
		multi = ''
		
		self.font = (self.font_type, size)
		
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
