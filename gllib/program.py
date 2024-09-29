from dataclasses import dataclass

from .gl import GL
from .shader import Program
from .vao import VAO
from .vbo import VBO
from .util import dtype_to_gl

import numpy

@dataclass
class Attribute:
	vbo: VBO
	array: any
	elements: int
	components: int
	gltype: any

class Program(Program):
	def __init__(self, vertex_shader=None, fragment_shader=None):
		super().__init__()

		if vertex_shader is not None:
			self.add_shader(GL.GL_VERTEX_SHADER, vertex_shader)

		if fragment_shader is not None:
			self.add_shader(GL.GL_FRAGMENT_SHADER, fragment_shader)

		self.link()
		self.vao = VAO()
		self.attributes = []

	def create_attribute(self, shape, index_or_name=None, dtype=float, buffer_type=GL.GL_ARRAY_BUFFER, usage_hint=GL.GL_DYNAMIC_DRAW):
		array = numpy.zeros(shape, dtype=dtype)
		if len(array.shape) == 1:
			components = 1
		else:
			components = array.shape[-1]
		elements = array.size // components

		gltype = dtype_to_gl(array.dtype.type)

		if index_or_name is None:
			location = len(self.attributes)
		elif isinstance(index_or_name, int):
			location = index
		else:
			with self as p:
				location = p.get_attribute_location(index_or_name)

		vbo = VBO(buffer_type=buffer_type, usage_hint=usage_hint)
		with self.vao as va:
			with vbo as vb:
				va.set_vertex_attribute(vb, location, components, gltype)

		self.attributes.append(Attribute(vbo, array, elements, components, gltype))
		return array

	def update_attributes(self):
		for attribute in self.attributes:
			with attribute.vbo as vb:
				vb.set_data(attribute.array)

	def draw_arrays(self, mode, first=None, count=None):
		self.update_attributes()

		if first is None:
			first = 0

		if count is None:
			count = self.attributes[0].elements

		with self:
			with self.vao:
				GL.glDrawArrays(mode, first, count)

# @deprecated
class VertexFragmentProgram(Program):
	def __init__(self, vertex_shader, fragment_shader):
		super().__init__()
		self.add_shader(GL.GL_VERTEX_SHADER, vertex_shader)
		self.add_shader(GL.GL_FRAGMENT_SHADER, fragment_shader)
		self.link()
