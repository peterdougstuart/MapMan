from in_app import InApp
import os.path


class Product(object):

	def __init__(self, identifier):
	
		self.identifier = identifier
		
		self.valid = False
		self.price = 0.0
		self.discounted = False
		
		self.update()
		
	def is_purchased(self, product_identifier):
		return os.path.isfile('.{0}'.format(product_identifier))
		
	def log_price(self, product_identifier, product_price):
	
		file_name = self.get_price_log_file(product_identifier)
		
		with open(file_name, 'w') as f:
			f.write(str(product_price))
			
	def is_discounted(self, product_identifier, product_price):
	
		file_name = self.get_price_log_file(product_identifier)
		
		if not os.path.isfile(file_name):
			return False
		
		try:
			with open(file_name, 'r') as f:
				old_price = float(f.readline())
				return (product_price < old_price)
		except:
			return False
			
	def get_price_log_file(self, product_identifier):
		return '.{0}.price'.format(product_identifier)
		
	def get_product(self, in_app):
	
		if not InApp.Instance.products_validated:
			return None
			
		for product in InApp.Instance.products:
			if product.identifier.lower() == self.identifier.lower():
				return product
				
		return None
		
	def update(self):
	
		self.purchased = self.is_purchased(self.identifier)
		
		if self.purchased:
			self.can_purchase = False
			self.why_cant_purchase = 'Item already purchased'
		else:
			self.can_purchase = True
			self.why_cant_purchase = ''
			
	def validate(self, products):
		
		if self.identifier in products:
			
			product = products[self.identifier]
			
			self.valid = True
			self.price = product.price
			self.discounted = self.is_discounted(product.identifier, product.price)
			
			self.log_price(product.identifier, product.price)
			
			
class ProductsController(object):

	Instance = None
	
	@classmethod
	def get(cls):
	
		if cls.Instance is None:
			cls.Instance = ProductsController()
			
		return cls.Instance
		
	def __init__(self):
	
		InApp.Instance.add_observer(self)
		
		self.caller = None
		
		self.enabled = InApp.Instance.can_make_purchases()
		
		self.checkpoints = Product('com.mapmangame.checkpoints')
		
		self.dict = {}
		
		self.dict[self.checkpoints.identifier] = self.checkpoints
		
		self.validated = False
		
		InApp.Instance.get_products()
	
	def detach_caller(self):
		self.caller = None
	
	def update(self):
		
		if self.validated:
			for key in self.dict:
				product = self.dict[key]
				product.update()
				
	def validate(self, valid, products=None):
		
		if self.validated:
			raise Exception('Already validated')
			
		self.validated = valid
		
		if valid:
			for key in self.dict:
				self.dict[key].validate(products)
				
	def valid_count(self):
	
		if not self.validated:
			return 0
			
		count = 0
		
		for key in self.dict:
			if self.dict[key].valid:
				count += 1
				
		return count
		
	def offer_active(self):
	
		for key in self.dict:
			product = self.dict[key]
			if product.discounted and not product.purchased:
				return True
				
		return False
		
	def purchase(self, product, caller):
	
		if not product.can_purchase:
			raise Exception('Cannot purchase product')
			
		self.caller = caller
		InApp.Instance.purchase(product.identifier)
		
	def purchase_in_progress(self, product_identifier):
		
		if self.caller is not None:
			self.caller.purchase_in_progress(product_identifier)
			
	def purchase_successful(self, product_identifier):
	
		if self.caller is not None:
			self.caller.purchase_successful(product_identifier)
		
		else:
			
			print 'purchase successful'
			
		self.dict[product_identifier].update()
		
	def purchase_restored(self, product_identifier):
	
		if self.call is not None:
			self.caller.purchase_restored(product_identifier)
		
		else:
			
			print 'purchase restored'
		
		self.dict[product_identifier].update()
		
	def purchase_failed(self, product_identifier, error=None):
	
		if self.caller is not None:
			self.caller.purchase_failed(product_identifier, error)
		
		else:
			
			print 'purchase failed'

	def purchase_deferred(self, product_identifier, error=None):
	
		if self.caller is not None:
			self.caller.purchase_deferred(product_identifier)
		
		else:
			
			print 'purchase deferred'

