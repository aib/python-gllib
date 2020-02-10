from .gl import GL

class VBO:
	def __init__(self, buffer_type, usage_hint):
		self.id = GL.glGenBuffers(1)
		self.type = buffer_type
		self.hint = usage_hint

	def activate(self):
		GL.glBindBuffer(self.type, self.id)
