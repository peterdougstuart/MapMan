from objc_util import *
import os.path

class Sync:

	Instance = None
	
	@classmethod
	def initialize(cls):
		cls.Instance = Sync()
		
	@classmethod
	def initialize_dummy(cls):
		cls.Instance = SyncDummy()

	@classmethod
	def sync(cls, name, extension, filter, recursive):
		return cls.Instance.do_sync(name, extension, filter, recursive)

	def __init__(self):
	
		self.outer = ObjCClass("PAAppDelegate")
		
	def do_sync(self, name, extension, filter, recursive):
		
		try:
			
			return self.outer.syncFolder_extension_filter_recursive_(name, extension, filter, recursive)
		
		except Exception as e:
			
			print e
			
			return False


class SyncDummy (object):
	
	def do_sync(self, name, extension, filter, recursive):
		
		if not os.path.isdir(name):
			raise Exception('Non-existent folder {0}'.format(name))
			
		return True
	
