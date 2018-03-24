from objc_util import *
import os.path
import time

class InAppProxy:

    SLEEP_STEP = 0.1
    MAX_SLEEP = 5.0

    PRODUCTS_FILE = '.products'

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

    def get_products(self):
        
        try:

            my_class = ObjCClass("PAAppDelegate")
            my_class.fetchProducts()
        
            if self.wait_products():

                f = open(InAppProxy.ProductsFile, 'r')
                data = f.readline().split(',')
                f.close()

                self.products.append(Product(data[0], data[0], data[0], float(data[1])))

            else:

                self.products_validated = True

        except None as e:

            self.products_validated = True

    def wait_products(start=False):

        total_wait = 0.0

        while(total_wait < InAppProxy.MAX_SLEEP):

            time.sleep(InAppProxy.SLEEP_STEP)
            total_wait += InAppProxy.SLEEP_STEP

            if os.path.isfile(InAppProxy.PRODUCTS_FILE):
                return True

        return False


