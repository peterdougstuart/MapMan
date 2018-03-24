from objc_util import *

class DummyRater (object):
	
	def request_review(self):
		pass
		
class Rater (object):

	Instance = None

	@classmethod
	def initialize(cls):
		cls.Instance = Rater()

	@classmethod
	def initialize_dummy(cls):
		cls.Instance = DummyRater()

	def request_review(self):
		
		review = ObjCClass("SKStoreReviewController")
		
		review.requestReview()


    

