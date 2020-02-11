from .gl import GL
from . import contextmanager

@contextmanager.activatable
class VAO:
	def __init__(self):
		self.id = GL.glGenVertexArrays(1)

	def activate(self):
		GL.glBindVertexArray(self.id)

	@contextmanager.activated
	def enable_vertex_attrib_array(self, index):
		GL.glEnableVertexAttribArray(index)
