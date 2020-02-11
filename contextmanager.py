def activatable(cls):
	cls.__enter__ = _activatable_enter
	cls.__exit__ = _activatable_exit
	return cls

def activated(func):
	return func

def _activatable_enter(self):
	self.activate()
	return self

def _activatable_exit(self, exc_type, exc_value, traceback):
	if hasattr(self, 'deactivate'):
		self.deactivate()
