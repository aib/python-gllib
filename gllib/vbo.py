from .gl import GL
from . import contextmanager

import ctypes

@contextmanager.activatable
class VBO:
	def __init__(self, buffer_type, usage_hint):
		self.id = GL.glGenBuffers(1)
		self.type = buffer_type
		self.hint = usage_hint

	def activate(self):
		GL.glBindBuffer(self.type, self.id)

	@contextmanager.activator
	def bind_as(self, bind_type):
		GL.glBindBuffer(bind_type, self.id)

	@contextmanager.activated
	def set_data(self, data):
		GL.glBufferData(self.type, data, self.hint)

	def bind_base(self, index):
		GL.glBindBufferBase(self.type, index, self.id)

	@contextmanager.activated
	def _vertex_attrib_pointer(self, index, components, item_type, stride=0, offset=0):
		GL.glVertexAttribPointer(index, components, item_type, False, stride, ctypes.c_void_p(offset))
