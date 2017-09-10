import os.path
import datetime

class ProductRegistry (object):
	
	Instance = None

	@classmethod
	def get(cls):
		
		if cls.Instance is None:
			cls.Instance = ProductRegistry()
		
		return cls.Instance
		
	def __init__(self):
		
		self.purchased = {}
	
	def load(self, name):
		return os.path.isfile(self.get_file(name))

	def save(self, name):
		
		file = self.get_file(name)
		
		with open(file, 'w') as f:
			f.write(str(datetime.datetime.now()))
		
	def get_file(self, name):
		return '.{0}'.format(name)
		
	def register(self, product_identifier):
		self.save(product_identifier)
		self.purchased[product_identifier] = True
	
	def is_purchased(self, product_identifier):
		
		if not product_identifier in self.purchased:
			self.purchased[product_identifier] = self.load(product_identifier)
			
		return self.purchased[product_identifier]

