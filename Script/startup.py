from sync import Sync
from scaler import Scaler

class SyncCommand(object):
	
	def __init__(self, name, extension, filter=None, recursive=True):
	
		self.name = name
		self.extension = extension
		self.filter = filter
		self.recursive = recursive
		
	def execute(self):
		
		return Sync.sync(self.name, self.extension, self.filter, self.recursive)

class Startup (object):
	
	def __init__(self, game):
		
		self.error = False
		
		self.syncs = self.new_syncs()
		self.resources = game.get_resource_actions()
		
		self.total = len(self.syncs)+len(self.resources)
		
	def fraction_complete(self):
		
		remaining = float(len(self.syncs)+len(self.resources)) / float(self.total)
		
		return 1.0 - remaining
	
	def is_complete(self):
		if len(self.syncs) > 0 or len(self.resources) > 0:
			return False
		else:
			return True
	
	def next(self):
		
		if len(self.syncs) > 0:
			action = self.syncs[-1]
			del self.syncs[-1]
			sync = True
		elif len(self.resources) > 0:
			action = self.resources[-1]
			del self.resources[-1]
			sync = False
		else:
			raise Exceptions('No startup actions remaining')
		
		try:
			
			success = action.execute()
			
			if not success:
				
				self.error = True
				
				if sync:
					self.error_message = 'failed to decompress files\ntry freeing up some space\non your device'
				else:
					self.error_message = 'Action Failed: {0}'.format(action.name)
			
			else:
				
				self.error = False
				self.error_message = ''
				
		except Exception as e:
			
			self.error = True

			self.error_message = 'Action Failed: {0} - {1}'.format(action.name, e)
		
	def new_syncs(self):
		
		syncs = []
		filter = Scaler.get_filter()
		syncs.append(SyncCommand('Buttons','png',filter))
		syncs.append(SyncCommand('CheckPoint','png',filter))
		syncs.append(SyncCommand('Effects','png',filter))
		syncs.append(SyncCommand('GameMusic','caf'))
		syncs.append(SyncCommand('Gradients','png'))
		
		#note heart is always normal size (never large)
		syncs.append(SyncCommand('Heart','png'))
		syncs.append(SyncCommand('Hearts','png',filter))
		syncs.append(SyncCommand('Man','png',filter, recursive=True))
		syncs.append(SyncCommand('Menu','png',filter))
		syncs.append(SyncCommand('SoundEffects','caf'))
		
		#note star is always normal size (never large)
		syncs.append(SyncCommand('Star','png'))
		syncs.append(SyncCommand('Tiles','png',filter))
		syncs.append(SyncCommand('Vortex','png',filter))
		syncs.append(SyncCommand('Woman','png',filter, recursive=True))
		
		return syncs
		
