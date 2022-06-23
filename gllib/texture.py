from .gl import GL
from . import contextmanager

@contextmanager.activatable
class Texture:
	def __init__(self, texture_type, binding_type):
		self.type = texture_type
		self.binding_type = binding_type

		self.id = GL.glGenTextures(1)
		self.last_active_id = None

	def activate(self):
		self.last_active_id = GL.glGetInteger(self.binding_type)
		GL.glBindTexture(self.type, self.id)

	def deactivate(self):
		GL.glBindTexture(self.type, self.last_active_id)
		self.last_active_id = None
