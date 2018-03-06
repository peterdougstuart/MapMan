from objc_util import *
import ctypes
import time
from random import randint

#http://omz-software.com/pythonista/docs/ios/objc_util.html
#http://omz-software.com/pythonista/docs/ios/objc_util.html#objc_util.create_objc_class
#https://www.tutorialspoint.com/ios/ios_in_app_purchase.htm

def fetchAvailableProducts(_self, _cmd):

    obj = ObjCInstance(_self)
    
    sk_class = ObjCClass("SKProductsRequest")
    
    InApp.Instance.products_request = sk_class.alloc().init(productIdentifiers=ns(InApp.PRODUCTS))
    InApp.Instance.products_request.delegate = obj
    InApp.Instance.products_request.start()

def productsRequest_didReceiveResponse_(_self, _cmd, request, response):
    #defined here: https://developer.apple.com/documentation/storekit/skproductsrequestdelegate/1506070-productsrequest
    InApp.Instance.receive_products(response)

def paymentQueue_updatedTransactions_(_self, _cmd, queue, transactions):
    InApp.Instance.update_transactions(queue, transactions)

class Product:
	
    def __init__(self, identifier, title, description, price):
        self.identifier = identifier
        self.title = title
        self.description = description
        self.price = price
	
class InAppDummy:
    def __init__(self):
    	
        self.observers = []
        self.products = []
        
        discounted = (randint(0, 2) == 0)
        
        if discounted:
        	price = 0.99
        else:
        	price = 1.99
        self.products.append(Product('com.mapman.checkpoints', 'Checkpoints', 'activate ability to restart game from achieved checkpoints. great for practicing later levels without having to start from the beginning', price))
        
        self.invalid_products = []
        
        self.products_validated = True
        self.can_make_purchases = True

    def purchase(self, product_identifier):
    	
        time.sleep(1.0)
        
        outcome = (randint(0, 3) == 0)
        
        for observer in self.observers:
            if outcome == 0:
                observer.purchase_successful(product_identifier)
            elif outcome == 1:
                observer.purchase_failed(product_identifier)
            elif outcome == 2:
                observer.purchase_restored(product_identifier)
            else:
                raise Exception('Unknown outcome')
              
    def add_observer(self, observer):
    	self.observers.append(observer)
    	
class InApp:
    
    PRODUCTS = ['com.mapman.checkpoints']
    
    Instance = None
    
    @classmethod
    def initialize(cls):
        cls.Instance = InApp()
        cls.Instance.fetch()

    @classmethod
    def initialize_dummy(cls):
        cls.Instance = InAppDummy()
    
    def log(self, message):
        self.log.append(message)
    
    def update_successfull_purchase(self, product_identifier):
        for observer in self.observers:
            observer.purchase_successful(product_identifier)

    def update_failed_purchase(self, product_identifier):
        for observer in self.observers:
            observer.purchase_failed(product_identifier)

    def update_restored_purchase(self, product_identifier):
        for observer in self.observers:
            observer.purchase_restored(product_identifier)
    
    def get_valid_product(self, product_identifier):
        
        for product in self.valid_products:
            if product.product_identifier == product_identifier:
                return product

        raise Exception('Product is not valid: {0}'.format(product_identifier))

    def is_valid_product(self, product_identifier):
    
        for product in self.valid_products:
            if product.product_identifier == product_identifier:
                return True
        
        return False

    def purchase(self, product_identifier):

        if not self.can_make_purchases:
            raise Exception('Purchases are disabled')
        else:
            product = self.get_valid_product(product_identifier)
            sk_payment_class = ObjCClass("SKPayment")
            payment = sk_payment_class.alloc().init(product=product)
            default_queue = ObjCClass("SKPaymentQueue").defaultQueue
            default_queue.addTransactionObserver(self.purchase_controller)
            default_queue.addPayment(sk_payment_queue_class)
    
    def update_transactions(self, queue, transactions):
        
        for transaction in ObjCInstance(transactions):

            transaction_state = transaction.transactionState
            
            if transaction_state == "SKPaymentTransactionStatePurchasing":
        
                self.log('Purchasing')
            
            elif transaction_state == "SKPaymentTransactionStatePurchased":

                if transaction.payment.productIdentifier in InApp.PRODUCTS:
                    self.log('Purchased')
                    self.update_successfull_purchase(transaction.payment.productIdentifier)
                    default_queue = ObjCClass("SKPaymentQueue").defaultQueue
                    default_queue.finishTransaction(transaction)
                        
            elif transaction_state == "SKPaymentTransactionStateRestored":

                self.log('Restored')
                self.update_restored_purchase(transaction.payment.productIdentifier)
                default_queue = ObjCClass("SKPaymentQueue").defaultQueue
                default_queue.finishTransaction(transaction)
            
            elif transaction_state == "SKPaymentTransactionStateFailed":
                self.update_failed_purchase(transaction.payment.productIdentifier)
                self.log('Failed')
                
    def receive_products(self, response):

        self.products_validated = True
        self.valid_products = []
        self.invalid_products = []
        
        obj_response = ObjCInstance(response)
        valid_products = ObjCInstance(obj_response.products())
        
        self.valid_count = len(valid_products)
        
        for valid_product in valid_products:
            
            if (valid_product.productIdentifier in InApp.PRODUCTS) or True:
                
                product = Product(valid_product.productIdentifier,
                                  valid_product.localizedTitle,
                                  valid_product.localizedDescription,
                                  valid_product.price)
                              
                self.valid_products.append(product)
    
        for invalid in obj_response.invalidProductIdentifiers():
            self.invalid_products.append(invalid)
    
    def __init__(self):
        
        self.products_request = None
        
        self.observers = []
        self.log = []
        
        self.products = []
        self.products_validated = False
        
        self.valid_count = 0
        self.invalid_products = []
        
		
    def add_observer(self, observer):
        self.observers.append(observer)
			
    #@on_main_thread
    def fetch(self):
        
        self.check_purchases_enabled()
        
        ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/StoreKit.framework').load()
        
        superclass = ObjCClass("NSObject")
        
        methods = [fetchAvailableProducts,
                   productsRequest_didReceiveResponse_,
                   paymentQueue_updatedTransactions_]
            
        protocols = ['SKProductsRequestDelegate', 'SKPaymentTransactionObserver']
        
        purchase_controller_class = create_objc_class('PurchaseController', superclass, methods=methods, protocols=protocols)
          
        self.purchase_controller = purchase_controller_class.alloc().init()

        self.purchase_controller.fetchAvailableProducts()
    
    def check_purchases_enabled(self):
        sk_payment_queue_class = ObjCClass("SKPaymentQueue")
        self.can_make_purchases = sk_payment_queue_class.canMakePayments()
