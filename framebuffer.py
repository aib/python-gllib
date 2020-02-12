from .gl import GL
from . import contextmanager

@contextmanager.activatable
class Framebuffer:
	@contextmanager.activatable
	class FramebufferTexture:
		def __init__(self, size):
			self.size = size
			self.id = GL.glGenTextures(1)
			self.last_active_id = None
			with self:
				GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, self.size[0], self.size[1], 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
				GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST);
				GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST);

		def activate(self):
			self.last_active_id = GL.glGetInteger(GL.GL_TEXTURE_BINDING_2D)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)

		def deactivate(self):
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.last_active_id)
			self.last_active_id = None

	def __init__(self, size):
		self.size = size
		self.id = GL.glGenFramebuffers(1)
		self.last_active_id = None

		self.texture = self._create_texture()
		with self:
			GL.glFramebufferTexture2D(GL.GL_DRAW_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture.id, 0)

	def activate(self):
		self.last_active_id = GL.glGetInteger(GL.GL_DRAW_FRAMEBUFFER_BINDING)
		GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self.id)

	def deactivate(self):
		GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self.last_active_id)
		self.last_active_id = None

	def activate_for_read(self):
		GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self.id)

	def _create_texture(self):
		return self.FramebufferTexture(self.size)
