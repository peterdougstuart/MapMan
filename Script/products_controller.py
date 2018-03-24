from in_app import InApp
from product_registry import ProductRegistry

class Product(object):
	
	def __init__(self, identifier, consumable=False):
		
		self.identifier = identifier
		
		self.valid = False
		self.purchased = ProductRegistry.get().is_purchased(identifier)
		self.can_purchase = False
		self.why_cant_purchase = ''
		
		self.title = ''
		self.description = ''
		self.price = 0.0
		self.consumable = consumable
		self.discounted = False
		
		self.update_can_purchase()
	
	def extend(self, in_app):
		
		product = self.match(in_app)
		
		if product is not None:
			self.title = product.title
			self.price = product.price
			self.description = product.description    
			self.valid = True

			self.discounted = ProductRegistry.get().is_discounted(product.identifier, product.price)
			ProductRegistry.get().log_price(product.identifier, product.price)
	
	def match(self, in_app):
		
		for product in in_app.products:
			if product.identifier.lower() == self.identifier.lower():
				return product
		
		return None
		
	def update_can_purchase(self):
		
		if self.purchased:
			self.can_purchase = False
			self.why_cant_purchase = 'Item already purchased'
		else:
			self.can_purchase = True
			self.why_cant_purchase = ''
		
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
		
		self.enabled = InApp.Instance.can_make_purchases
		
		self.checkpoints = Product('com.mapman.checkpoints')
		
		self.dict = {}
		
		self.dict[self.checkpoints.identifier] = self.checkpoints
		
		self.validated = False
		
		self.validate()
		
	def validate(self):
		
		if self.validated:
			raise Exception('Already validated')
			
		if InApp.Instance.products_validated:
			
			self.validated = True
			self.valid_count = InApp.Instance.valid_count
			
			if len(InApp.Instance.products) > 0:
				self.checkpoints.extend(InApp.Instance)
				
		else:
			
			self.validated = False
			self.valid_count = 0
			
	def offer_active(self):
		
		if self.checkpoints.purchased:
			return False
			
		return self.checkpoints.discounted
		
	def purchase(self, product, caller):
		
		if not product.can_purchase:
			raise Exception('Cannot purchase product')
		
		self.caller = caller
		InApp.Instance.purchase(product.identifier)
		
	def purchase_successful(self, product_identifier):
		ProductRegistry.get().register(product_identifier)
		self.caller.purchase_successful(product_identifier)
		self.caller = None
		
		product = self.dict[product_identifier]
		
		if not product.consumable:
			product.purchased = True

		product.update_can_purchase()
		
	def purchase_restored(self, product_identifier):
		ProductRegistry.get().register(product_identifier)
		self.caller.purchase_restored(product_identifier)
		self.caller = None
		
		product = self.dict[product_identifier]
		
		if not product.consumable:
			product.purchased = True
		
		product.update_can_purchase()
		 
	def purchase_failed(self, product_identifier):
		self.caller.purchase_failed(product_identifier)
		
		self.caller = None
	
