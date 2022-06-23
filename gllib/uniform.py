from .gl import GL

class UniformNotFound(Exception):
	def __init__(self, uniform_name):
		super().__init__("Uniform \"%s\" not found" % (uniform_name,))

def get_uniform_location(program_id, name, silent=False):
	location = GL.glGetUniformLocation(program_id, name)
	if location == -1:
		if not silent:
			raise UniformNotFound(name)
	return location
