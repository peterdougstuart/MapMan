from objc_util import *
import ctypes

#http://omz-software.com/pythonista/docs/ios/objc_util.html
#http://omz-software.com/pythonista/docs/ios/objc_util.html#objc_util.create_objc_class
#https://www.tutorialspoint.com/ios/ios_in_app_purchase.htm

def PurchaseController_fetchAvailableProducts(_self, _cmd):

    obj = ObjCInstance(_self)
    
    sk_class = ObjCClass("SKProductsRequest")
    products_request = sk_class.alloc().init(productIdentifiers=InApp.PRODUCTS)
    
    products_request.delegate = obj
    products_request.start()

def PurchaseController_canMakePurchases(_self, _cmd):
    sk_class = ObjCClass("SKPaymentQueue")
    return sk_class.canMakePayments()

def productsRequest_didReceiveResponse_(_self, _cmd, request, response):
    #defined here: https://developer.apple.com/documentation/storekit/skproductsrequestdelegate/1506070-productsrequest
    InApp.Instance.receive_products(response)

def paymentQueue_updatedTransactions_(_self, _cmd, queue, transactions):
    InApp.Instance.update_transactions(queue, transactions)

class Product:
	
    def __init__(self, identifer, title, description, price):
        self.identifer = identifer
        self.title = title
        self.description = description
        self.price = price
	
class InAppDummy:
    def __init__(self):
        self.products = []
        self.products.append(Product('Prod01', 'DummyA', 'Dummy', 1.0))
        self.products.append(Product('Prod01', 'DummyB', 'Dummy', 0.25))
        self.products_received = True

class InApp:
    
    PRODUCTS = ["MapManPurchase001"]
    Instance = None
    
    @classmethod
    def initialize(cls):
        cls.Instance = InApp()

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
        
        valid_products = ObjCInstance(response).products()
        
        for valid_product in valid_products:
            
            if valid_product.productIdentifier in InApp.PRODUCTS:
                
                product = Product(valid_product.productIdentifier,
                                  valid_product.localizedTitle,
                                  valid_product.localizedDescription,
                                  valid_product.price)
                              
            self.valid_products.append(product)

    def __init__(self):
        
        self.observers = []
        self.log = []
        
        self.products = []
        self.products_received = False
        
        ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/StoreKit.framework').load()
        
        superclass = ObjCClass("NSObject")
        
        methods = [PurchaseController_fetchAvailableProducts,
                   PurchaseController_canMakePurchases,
                   productsRequest_didReceiveResponse_,
                   paymentQueue_updatedTransactions_]
        
        protocols = ['SKProductsRequestDelegate', 'SKPaymentTransactionObserver']
        
        purchase_controller_class = create_objc_class('PurchaseController', superclass, methods=methods, protocols=protocols)

        self.purchase_controller = purchase_controller_class.alloc().init()
        
        self.can_make_purchases = purchase_controller.canMakePurchases()
        
        self.purchase_controller.fetchAvailableProducts()
