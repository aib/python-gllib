from .gl import GL
from . import contextmanager

@contextmanager.activatable
class VBO:
	def __init__(self, buffer_type, usage_hint):
		self.id = GL.glGenBuffers(1)
		self.type = buffer_type
		self.hint = usage_hint

	def activate(self):
		GL.glBindBuffer(self.type, self.id)

	@contextmanager.activated
	def set_data(self, data):
		GL.glBufferData(self.type, data, self.hint)

	@contextmanager.activated
	def _vertex_attrib_pointer(self, index, components, item_type):
		GL.glVertexAttribPointer(index, components, item_type, False, 0, None)
