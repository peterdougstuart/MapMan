from objc_util import *
import ctypes

#http://omz-software.com/pythonista/docs/ios/objc_util.html
#http://omz-software.com/pythonista/docs/ios/objc_util.html#objc_util.create_objc_class
#https://www.tutorialspoint.com/ios/ios_in_app_purchase.htm

def PurchaseController_fetchAvailableProducts(_self, _cmd):

    obj = ObjCInstance(_self)
    
    sk_class = ObjCClass("SKProductsRequest")
    products_request = sk_class.alloc().init(productIdentifiers=[InApp.PRODUCT_ID])
    
    products_request.delegate = obj
    products_request.start()

def PurchaseController_canMakePurchases(_self, _cmd):
    sk_class = ObjCClass("SKProductsRequest")
    return sk_class.canMakePayments()

def PurchaseController_purchase(_self, _cmd):
    pass

def PurchaseController_purchaseMyProduct(_self, _cmd):
    pass

def productsRequest_request_didReceiveResponse(_self, _cmd, request, response):
    #defined here: https://developer.apple.com/documentation/storekit/skproductsrequestdelegate/1506070-productsrequest
    InApp.receive_products(response)

class Product:
	
    def __init__(self, description):
        self.description = description
	
class InAppDummy:
    def __init__(self):
        self.products = []
        self.products.append(Product('DummyA'))
        self.products.append(Product('DummyB'))
        self.products_received = True

class InApp:
    
    PRODUCT_ID = "MapManPurchase001"
    Instance = None
    
    @classmethod
    def initialize(cls):
        cls.Instance = InApp()

    @classmethod
    def initialize_dummy(cls):
        cls.Instance = InAppDummy()
        
    @classmethod
    def receive_products(cls, response):
        cls.Instance.products_received = True
        self.products.append(Product('Dummy1'))
        self.products.append(Product('Dummy2'))
    
    def __init__(self):
        
        self.products = []
        self.products_received = False
        
        ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/StoreKit.framework').load()
        
        superclass = ObjCClass("NSObject")
        
        methods = [PurchaseController_fetchAvailableProducts,
                   PurchaseController_canMakePurchases,
                   productsRequest_request_didReceiveResponse]
        
        protocols = ['SKProductsRequestDelegate', 'SKPaymentTransactionObserver']
        
        purchase_controller_class = create_objc_class('PurchaseController', superclass, methods=methods, protocols=protocols)

        purchase_controller = purchase_controller_class.alloc().init()

        purchase_controller.fetchAvailableProducts()
