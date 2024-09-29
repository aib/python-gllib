from .gl import GL
from .shader import Program

class VertexFragmentProgram(Program):
	def __init__(self, vertex_shader, fragment_shader):
		super().__init__()
		self.add_shader(GL.GL_VERTEX_SHADER, vertex_shader)
		self.add_shader(GL.GL_FRAGMENT_SHADER, fragment_shader)
		self.link()
