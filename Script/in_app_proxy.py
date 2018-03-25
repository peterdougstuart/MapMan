from objc_util import *
import os.path

from in_app import Product
from in_app import InApp

def successful(_self, _cmd):
    InApp.Instance.inform_observers(0)

def failed(_self, _cmd):
    InApp.Instance.inform_observers(1)

def restored(_self, _cmd):
    InApp.Instance.inform_observers(2)

def inProgress(_self, _cmd):
    InApp.Instance.inform_observers(3)

def loaded(_self, _cmd):
    InApp.Instance.loaded()

class InAppProxy:

    PRODUCTS_FILE = '.products'

    def __init__(self):

        self.outer = ObjCClass("PAAppDelegate")

        self.products_validated = False

        self.observers = []
        self.products = []
        
        self.can_make_purchases = self.outer.canMakePayments()
        
        self.valid_count = 0

        self.product_identifier = None

    def purchase(self, product_identifier):
    	
        if self.product_identifier is not None:
            raise Exception('purchase already in progress')

        try:

            superclass = ObjCClass("NSObject")

            call_back_class = create_objc_class('PythonPurchaseCallBack',
                                                ObjCClass("NSObject"),
                                                methods=[successful, failed, restored, inProgress],
                                                protocols=['PurchaseCallBack'])

            call_back_object = call_back_class.alloc().init()

            self.outer.purchase_callBack_(product_identifier, call_back_object)
        
        except Exception as e:
            
            self.inform_observers(1)

        
    def inform_observers(self, outcome):

        for observer in self.observers:
            if outcome == 0:
                observer.purchase_successful(self.product_identifier)
            elif outcome == 1:
                observer.purchase_failed(self.product_identifier)
            elif outcome == 2:
                observer.purchase_restored(self.product_identifier)
            elif outcome == 3:
                observer.purchase_in_progress(self.product_identifier)
            else:
                raise Exception('Unknown outcome')
        
        self.product_identifier = None

    def add_observer(self, observer):
        self.observers.append(observer)

    def get_products(self):
        
        try:

            self.products_validated = False
            self.products = []

            superclass = ObjCClass("NSObject")

            call_back_class = create_objc_class('PythonProductsCallBack',
                                                ObjCClass("NSObject"),
                                                methods=[loaded],
                                                protocols=['ProductsCallBack'])

            call_back_object = call_back_class.alloc().init()

            self.outer.fetchProducts_dummy_(call_back_object, 'dummy')

        except Exception as e:
            self.products_validated = False

    def loaded(self):

        try:

            f = open(InAppProxy.PRODUCTS_FILE, 'r')
            
            for line in f.readlines():

                line = line.strip()

                if len(line) > 0:
                    data = line.split(',')
                    self.products.append(Product(identifier=data[0], title=data[0], description=data[0], price=float(data[1])))

            f.close()

            self.products_validated = True
            self.valid_count = len(self.products)

        except Exception as e:
            self.products_validated = False
            self.valid_count = 0

        for observer in self.observers:
            observer.validate()
