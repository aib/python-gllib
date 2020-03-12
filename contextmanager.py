import functools

_ACTIVE_ATTR_NAME = '_gllib_contextmanager_active'

class ActivationRequiredException(Exception):
	def __init__(self, obj, method):
		self.obj = obj
		self.method = method
		self.message = "Method " + str(self.method.__name__) + " requires activation"

	def __str__(self):
		return self.message

def activatable(cls):
	def activatable_enter(self):
		self.activate()
		_activate(self)
		return self

	def activatable_exit(self, exc_type, exc_value, traceback):
		_deactivate(self)

	cls.__enter__ = activatable_enter
	cls.__exit__ = activatable_exit
	setattr(cls, _ACTIVE_ATTR_NAME, False)
	return cls

def activated(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		if not getattr(self, _ACTIVE_ATTR_NAME):
			raise ActivationRequiredException(self, func)
		return func(self, *args, **kwargs)
	return wrapper

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
		_activate(self)
		return self.original

	def __exit__(self, exc_type, exc_value, traceback):
		_deactivate(self.original)

def _activate(self):
	setattr(self, _ACTIVE_ATTR_NAME, True)

def _deactivate(self):
	setattr(self, _ACTIVE_ATTR_NAME, False)
	if hasattr(self, 'deactivate'):
		self.deactivate()
