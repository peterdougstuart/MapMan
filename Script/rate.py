from objc_util import *
import datetime
import os.path

class DummyRater (object):
	
	def request_review(self):
		pass
		
class Rater (object):

	Instance = None
	
	FILE = '.rate_date'
	DATE_FORMAT = '%d-%m-%Y'
	DAYS_BETWEEN = 0
	
	def __init__(self):
		
		self.now = datetime.datetime.now()
		self.delta_days = 0
		
		ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/StoreKit.framework').load()
		
		self.review = ObjCClass("SKStoreReviewController")
		
	@classmethod
	def initialize(cls):
		cls.Instance = Rater()

	@classmethod
	def initialize_dummy(cls):
		cls.Instance = DummyRater()

	def request_review(self):
		
		if not self.can_request():
			return
		
		self.review.requestReview()
		
		self.write_date()

	def can_request(self):
		
		last_date = self.read_date()
		
		if last_date is None:
			self.delta_days = 0
			return True
		
		delta = self.now - last_date
		
		self.delta_days = delta.total_seconds() / (8766.0*60.0*60.0)
		
		if self.delta_days > Rater.DAYS_BETWEEN:
			return True
		else:
			return False
		
	def read_date(self):
		
		if not os.path.isfile(Rater.FILE):
			return None
		
		with open(Rater.FILE, 'r') as f:
			line = f.readline()
			date = datetime.datetime.strptime(line, Rater.DATE_FORMAT)
			return date

	def write_date(self):
		
		with open(Rater.FILE, 'w') as f:
			
			date_text = self.now.strftime(Rater.DATE_FORMAT)
			
			f.write(date_text)

if __name__ == '__main__':
	rater = Rater()
	rater.request_review()
	print rater.delta_days

