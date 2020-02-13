import functools

def activatable(cls):
	cls.__enter__ = _activatable_enter
	cls.__exit__ = _activatable_exit
	return cls

def activated(func):
	return func

def activator(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		func(self, *args, **kwargs)
		return _ActivatorProxy(self)

	return wrapper

class _ActivatorProxy:
	def __init__(self, original):
		self.original = original

	def __enter__(self):
		return self.original

	def __exit__(self, exc_type, exc_value, traceback):
		pass

def _activatable_enter(self):
	self.activate()
	return self

def _activatable_exit(self, exc_type, exc_value, traceback):
	if hasattr(self, 'deactivate'):
		self.deactivate()
