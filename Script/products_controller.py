from in_app import InApp
from product_registry import ProductRegistry

class NullProduct(object):
	
	def __init__(self):
		
		self.valid = False
		self.purchased = False
		self.can_purchase = False
		self.why_cant_purchase = ''
		
		self.identifier = ''
		self.title = ''
		self.description = ''
		self.price = 0.0
		
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
		
		self.checkpoints = NullProduct()
		self.l26_l50 = NullProduct()
		self.l51_l75 = NullProduct()
		self.l76_l100 = NullProduct()
		self.everything = NullProduct()
		
		if InApp.Instance.products_validated:
			
			self.validated = True
			
			if len(InApp.Instance.products) > 0:
				
				for product in InApp.Instance.products:
					
						self.map_to_attribute(product)
				
		else:
			
			self.validated = False
			
		self.check_can_purchase()
		
		self.products = []
		self.products.append(self.checkpoints)
		self.products.append(self.l26_l50)
		self.products.append(self.l51_l75)
		self.products.append(self.l76_l100)
		self.products.append(self.everything)
		
		self.dict = {}
		
		for product in self.products:
			self.dict[product.identifier] = product
		
		self.update_purchase_everything()
		
	def get_products(self):
		
		products = []
		
		for product in self.products:
					
			if product.valid:
						
				if product.title.lower() != 'everything' or product.can_purchase:
					
					products.append(product)
		
		return products
		
	def map_to_attribute(self, product):
		
		if product.identifier == 'com.mapman.checkpoints':
			self.checkpoints = self.extend(product)
		elif product.identifier == 'com.mapman.l26-50':
			self.l26_l50 = self.extend(product)
		elif product.identifier == 'com.mapman.l51-75':
			self.l51_l75 = self.extend(product)
		elif product.identifier == 'com.mapman.l76-100':
			self.l76_l100 = self.extend(product)
		elif product.identifier == 'com.mapman.everything':
			self.everything = self.extend(product)
			
	def extend(self, product):
		
		product.purchased = ProductRegistry.get().is_purchased(product.identifier)
		
		product.can_purchase = False
		product.valid = True
		product.why_cant_purchase = ''
		
		return product
		
	def check_can_purchase(self):
		
		self.check_can_purchase_checkpoints()
		self.check_can_purchase_everything()
		self.check_can_purchase_l26_l50()
		self.check_can_purchase_l51_l75()
		self.check_can_purchase_l76_l100()
	
	def base_can_purchase(self, product):
		
		if product.purchased:
			product.can_purchase = False
			product.why_cant_purchase = 'Item already purchased'
			return False
		elif self.everything.purchased:
			product.can_purchase = False
			product.why_cant_purchase = 'Everything already purchased'
			return False
		else:
			product.can_purchase = True
			product.why_cant_purchase = ''
			return True
	
	def remaining_price(self, product):
		if product.purchased:
			return 0.0
		else:
			return product.price
		
	def check_can_purchase_checkpoints(self):
		self.base_can_purchase(self.checkpoints)
		
	def check_can_purchase_everything(self):
		
		if not self.base_can_purchase(self.everything):
			return
			
		remaining = 0.0
		remaining += self.remaining_price(self.checkpoints)
		remaining += self.remaining_price(self.l26_l50)
		remaining += self.remaining_price(self.l51_l75)
		remaining += self.remaining_price(self.l76_l100)
			
		if remaining >= self.everything.price:
			self.everything.can_purchase = True
		else:
			self.everything.can_purchase = False
			self.everything.why_cant_purchase = 'It is cheaper to purchase remaining non-purchased items individually'
		
	def check_can_purchase_l26_l50(self):
		self.base_can_purchase(self.l26_l50)

	def check_can_purchase_l51_l75(self):
		
		if not self.base_can_purchase(self.l51_l75):
			return
			
		if self.l26_l50.purchased:
			self.l51_l75.can_purchase = True
		else:
			self.l51_l75.can_purchase = False
			self.l51_l75.why_cant_purchase = 'You must first purchase levels 26-50'
			
	def check_can_purchase_l76_l100(self):
		
		if not self.base_can_purchase(self.l76_l100):
			return
			
		if self.l51_l75.purchased:
			self.l76_l100.can_purchase = True
		else:
			self.l76_l100.can_purchase = False
			self.l76_l100.why_cant_purchase = 'You must first purchase levels 51-75'

	def purchase(self, product, caller):
		
		if not product.can_purchase:
			raise Exception('Cannot purchase product')
		
		self.caller = caller
		InApp.Instance.purchase(product.identifier)
		
	def purchase_successful(self, product_identifier):
		ProductRegistry.get().register(product_identifier)
		self.caller.purchase_successful(product_identifier)
		self.caller = None
		
		self.dict[product_identifier].purchased = True
		
		self.update_purchase_everything()
		self.check_can_purchase()
		
	def purchase_restored(self, product_identifier):
		ProductRegistry.get().register(product_identifier)
		self.caller.purchase_restored(product_identifier)
		self.caller = None
		
		self.dict[product_identifier].purchased = True
		
		self.update_purchase_everything()
		self.check_can_purchase()
		
	def purchase_failed(self, product_identifier):
		self.caller.purchase_failed(product_identifier)
		self.caller = None
	
	def update_purchase_everything(self):
		
		if not self.everything.purchased:
			return
			
		for product in self.products:
			product.purchased = True
			product.can_purchase = False
		
