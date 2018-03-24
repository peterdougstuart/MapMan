from objc_util import *
import os.path
import time
from in_app import Product

class InAppProxy:

    SLEEP_STEP = 0.1
    MAX_SLEEP = 5.0

    PRODUCTS_FILE = '.products'
    PURCHASE_FILE = '.purchase'

    def __init__(self):

        self.observers = []
        self.products = []
        
        self.check_purchases_enabled()
        self.get_products() 
        
        self.valid_count = len(self.products)

    @on_main_thread
    def check_purchases_enabled(self):
        sk_payment_queue_class = ObjCClass("SKPaymentQueue")
        self.can_make_purchases = sk_payment_queue_class.canMakePayments()

    def purchase(self, product_identifier):
    	
        try:

            my_class = ObjCClass("PAAppDelegate")
            my_class.purchase()
        
            if self.wait_file(InAppProxy.PURCHASE_FILE):

                f = open(InAppProxy.PURCHASE_FILE, 'r')
                data = f.readline()
                f.close()

                self.inform_observers(0)

            else:

                self.inform_observers(1)

        except Exception as e:

            self.inform_observers(1)

        
    def inform_observers(self, outcome):
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

    def get_products(self):
        
        try:

            my_class = ObjCClass("PAAppDelegate")
            my_class.fetchProducts()
        
            if self.wait_file(InAppProxy.PRODUCTS_FILE):

                f = open(InAppProxy.ProductsFile, 'r')
                data = f.readline().split(',')
                f.close()

                self.products.append(Product(identifier=data[0], title=data[0], description=data[0], price=float(data[1])))

            else:

                self.products_validated = True

        except Exception as e:

            self.products_validated = False

    def wait_file(file_name):

        total_wait = 0.0

        while(total_wait < InAppProxy.MAX_SLEEP):

            time.sleep(InAppProxy.SLEEP_STEP)
            total_wait += InAppProxy.SLEEP_STEP

            if os.path.isfile(file_name):
                return True

        return False



