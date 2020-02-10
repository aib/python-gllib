from .gl import GL

class VAO:
	def __init__(self):
		self.id = GL.glGenVertexArrays(1)

	def activate(self):
		GL.glBindVertexArray(self.id)
