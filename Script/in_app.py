from objc_util import *
import time
from random import randint
import os.path

def successful_dummy_(_self, _cmd, identifier, dummy):
	product_identifier = str(ObjCInstance(identifier))
	InApp.Instance.inform_observers(0, product_identifier)
	
def failed_error_(_self, _cmd, identifier, error):
	product_identifier = str(ObjCInstance(identifier))
	InApp.Instance.inform_observers(1, product_identifier, error=str(ObjCInstance(error)))
	
def restored_dummy_(_self, _cmd, identifier, dummy):
	product_identifier = str(ObjCInstance(identifier))
	InApp.Instance.inform_observers(2, product_identifier)
	
def inProgress_dummy_(_self, _cmd, identifier, dummy):
	product_identifier = str(ObjCInstance(identifier))
	InApp.Instance.inform_observers(3, product_identifier)

def deferred_dummy_(_self, _cmd, identifier, dummy):
	product_identifier = str(ObjCInstance(identifier))
	InApp.Instance.inform_observers(4, product_identifier)
	
def loaded(_self, _cmd):
	InApp.Instance.loaded()
	
class Product:

	def __init__(self, identifier, price):
		self.identifier = identifier
		self.price = price
		
		
class InApp:

	PRODUCTS_FILE = '.products'
	
	Instance = None
	
	@classmethod
	def initialize(cls):
		cls.Instance = InApp()
		
	@classmethod
	def initialize_dummy(cls):
		cls.Instance = InAppDummy()
		
	def __init__(self):
	
		self.outer = ObjCClass("PAAppDelegate")
		
		self.observers = []
		
	def can_make_purchases(self):
		return self.outer.canMakePayments()
		
	def purchase(self, product_identifier):
		
		try:
		
			superclass = ObjCClass("NSObject")
			
			call_back_class = create_objc_class('PythonPurchaseCallBack',
			ObjCClass("NSObject"),
			methods=[successful_dummy_, failed_error_, restored_dummy_, deferred_dummy_, inProgress_dummy_],
			protocols=['PurchaseCallBack'])
			
			call_back_object = call_back_class.alloc().init()
			self.outer.purchase_callBack_(product_identifier, call_back_object)
			
		except Exception as e:
			self.inform_observers(1)
			
			
	def inform_observers(self, outcome, product_identifier, error=None):
	
		for observer in self.observers:
			if outcome == 0:
				observer.purchase_successful(product_identifier)
			elif outcome == 1:
				observer.purchase_failed(product_identifier, error)
			elif outcome == 2:
				observer.purchase_restored(product_identifier)
			elif outcome == 3:
				observer.purchase_in_progress(product_identifier)
			elif outcome == 4:
				observer.purchase_deferred(product_identifier)
			else:
				raise Exception('Unknown outcome')
				
	def add_observer(self, observer):
		self.observers.append(observer)
		
	def get_products(self):
	
		try:
		
			superclass = ObjCClass("NSObject")
			
			call_back_class = create_objc_class('PythonProductsCallBack',
			ObjCClass("NSObject"),
			methods=[loaded],
			protocols=['ProductsCallBack'])
			
			call_back_object = call_back_class.alloc().init()
			
			self.outer.fetchProducts_dummy_(call_back_object, 'dummy')
			
		except Exception as e:
			for observer in self.observers:
				observer.validate(False)
				
	def loaded(self):
	
		try:
		
			products = {}
			
			f = open(InApp.PRODUCTS_FILE, 'r')
			
			for line in f.readlines():
			
				line = line.strip()
				
				if len(line) > 0:
					
					data = line.split(',')
					
					identifier = data[0].strip().lower()
					
					price = float(data[1])
					
					products[identifier] = Product(identifier=identifier, price=price)
					
			f.close()
			
			for observer in self.observers:
				observer.validate(True, products)
				
		except Exception as e:
			for observer in self.observers:
				observer.validate(False)
				

class InAppDummy:

	def __init__(self):
	
		self.observers = []
		
	def can_make_purchases(self):
		return True
		
	def get_products(self):
	
		products = {}
		
		discounted = (randint(0, 2) == 0)
		
		identifier = 'com.mapmangame.checkpoints'
		
		if discounted:
			price = 0.99
		else:
			price = 1.99
			
		products[identifier] = Product(identifier, price)
		
		for observer in self.observers:
			observer.validate(True, products)
			
	def register(self, name):
	
		file = self.get_file(name)
		
		if not os.path.isfile(file):
			with open(file, 'w') as f:
				f.write(name)
				
	def get_file(self, name):
		return '.{0}'.format(name)
		
	def purchase(self, product_identifier):
		
		for observer in self.observers:
			observer.purchase_in_progress(product_identifier)
				
		time.sleep(1.0)
		
		outcome = (randint(0, 4) == 0)
		
		for observer in self.observers:
			if outcome == 0:
				self.register(product_identifier)
				observer.purchase_successful(product_identifier)
			elif outcome == 1:
				observer.purchase_failed(product_identifier)
			elif outcome == 2:
				self.register(product_identifier)
				observer.purchase_restored(product_identifier)
			elif outcome == 3:
				observer.purchase_deferred(product_identifier)
			else:
				raise Exception('Unknown outcome')
				
	def add_observer(self, observer):
		self.observers.append(observer)

