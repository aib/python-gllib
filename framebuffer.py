from .gl import GL
from . import contextmanager
from . import texture

@contextmanager.activatable
class Framebuffer:
	class FramebufferTexture(texture.Texture):
		def __init__(self, size):
			super().__init__(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BINDING_2D)
			self.size = size

			with self:
				GL.glTexImage2D(self.type, 0, GL.GL_RGBA, self.size[0], self.size[1], 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
				GL.glTexParameter(self.type, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST);
				GL.glTexParameter(self.type, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST);

	def __init__(self, size):
		self.size = size
		self.id = GL.glGenFramebuffers(1)
		self.last_active_id = None

		self.texture = self._create_texture()
		with self:
			GL.glFramebufferTexture2D(GL.GL_DRAW_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, self.texture.type, self.texture.id, 0)

	def activate(self):
		self.last_active_id = GL.glGetInteger(GL.GL_DRAW_FRAMEBUFFER_BINDING)
		GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self.id)

	def deactivate(self):
		GL.glBindFramebuffer(GL.GL_DRAW_FRAMEBUFFER, self.last_active_id)
		self.last_active_id = None

	def activate_for_read(self):
		GL.glBindFramebuffer(GL.GL_READ_FRAMEBUFFER, self.id)

	def blit(self):
		GL.glBlitFramebuffer(0, 0, self.size[0], self.size[1], 0, 0, self.size[0], self.size[1], GL.GL_COLOR_BUFFER_BIT, GL.GL_NEAREST)

	def _create_texture(self):
		return self.FramebufferTexture(self.size)

class MultisampledFramebuffer(Framebuffer):
	class MultisampledFramebufferTexture(texture.Texture):
		def __init__(self, samples, size):
			super().__init__(GL.GL_TEXTURE_2D_MULTISAMPLE, GL.GL_TEXTURE_BINDING_2D_MULTISAMPLE)
			self.samples = samples
			self.size = size

			with self:
				GL.glTexImage2DMultisample(self.type, self.samples, GL.GL_RGBA8, self.size[0], self.size[1], False)

	def __init__(self, samples, size):
		self.samples = samples
		super().__init__(size)

	def _create_texture(self):
		return self.MultisampledFramebufferTexture(self.samples, self.size)
