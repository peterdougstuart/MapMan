# coding: utf-8
import datetime

class Countdown(object):
	
	def __init__(self, parent, initial_seconds):
		
		self.parent = parent
		self.base_initial_seconds = initial_seconds
		self.initial_seconds = initial_seconds
		self.reset()
	
	def add_time(self, time):
		self.start += datetime.timedelta(seconds=time)
		
	def reset(self, reset_initial_seconds = False):
		self.start = datetime.datetime.now()
		if reset_initial_seconds:
			self.initial_seconds = self.base_initial_seconds
			
	def seconds_remaining(self):
		
		if self.parent.tutorial:
			return 999
			
		elapsed = datetime.datetime.now() - self.start
		elapsed_seconds = int(elapsed.total_seconds())
		return self.initial_seconds - elapsed_seconds
		
