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
		
	def log_price(self, product_identifier, product_price):

		file = self.get_price_log_file(product_identifier)
		
		with open(file, 'w') as f:
			f.write(str(product_price))
	
	def is_discounted(self, product_identifier, product_price):
		
		file = self.get_price_log_file(product_identifier)
		
		if not os.path.isfile(file):
			return False
		
		try:
			with open(file, 'r') as f:
				old_price = float(f.readline())
				return (product_price < old_price)
		except:
			return False

	def get_price_log_file(self, product_identifier):
		return '.{0}.price'.format(product_identifier)
		

