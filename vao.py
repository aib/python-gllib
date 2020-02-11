from .gl import GL
from . import contextmanager

@contextmanager.activatable
class VAO:
	def __init__(self):
		self.id = GL.glGenVertexArrays(1)

	def activate(self):
		GL.glBindVertexArray(self.id)

	@contextmanager.activated
	def set_vertex_attrib(self, vbo, index, components, item_type):
		GL.glEnableVertexAttribArray(index)
		vbo._vertex_attrib_pointer(index, components, item_type)
