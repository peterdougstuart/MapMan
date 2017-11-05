# coding: utf-8
import datetime

class Countdown(object):
	
	def __init__(self, parent, initial_seconds):
		
		self.parent = parent
		self.initial_seconds = initial_seconds
		self.base_initial_seconds = initial_seconds
		self.reset()
		self.started = False
	
	def add_time(self, time):
		self.start_time += datetime.timedelta(seconds=time)
		
	def reset(self):
		self.start_time = datetime.datetime.now()
		self.initial_seconds = self.base_initial_seconds
		
	def stop(self):
		self.initial_seconds = self.seconds_remaining(True)
		self.started = False

	def start(self):
		self.start_time = datetime.datetime.now()
		self.started = True
		
	def seconds_remaining(self, fractional=False):
		
		if not self.started:
			return self.initial_seconds
			
		elapsed = datetime.datetime.now() - self.start_time
		
		elapsed_seconds = elapsed.total_seconds()
		
		countdown = self.initial_seconds - elapsed_seconds

		if not fractional:
			countdown = int(countdown)
		
		if countdown < 0:
			return 0
		else:
			return countdown

