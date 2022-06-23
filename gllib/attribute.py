from .gl import GL

class AttributeNotFound(Exception):
	def __init__(self, attribute_name):
		super().__init__("Attribute \"%s\" not found" % (attribute_name,))

def get_attribute_location(program_id, name, silent=False):
	location = GL.glGetAttribLocation(program_id, name)
	if location == -1:
		if not silent:
			raise AttributeNotFound(name)
	return location
