from .gl import GL
from . import contextmanager
from . import uniform

class ShaderCompileError(Exception):
	def __init__(self, info_log):
		super().__init__("Error compiling shader: %s" % (info_log,))

class ProgramLinkError(Exception):
	def __init__(self, info_log):
		super().__init__("Error linking program: %s" % (info_log,))

def create_shader(shader_type, shader_source):
	shader_id = GL.glCreateShader(shader_type)
	GL.glShaderSource(shader_id, shader_source)
	GL.glCompileShader(shader_id)

	if GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS) == GL.GL_FALSE:
		info_log = GL.glGetShaderInfoLog(shader_id)
		if info_log != '': info_log = info_log.decode('ascii')
		raise ShaderCompileError(info_log)

	return shader_id

def create_program(shaders):
	program_id = GL.glCreateProgram()
	link_program(program_id, shaders)
	return program_id

def link_program(program_id, shaders):
	for shader_id in shaders:
		GL.glAttachShader(program_id, shader_id)

	GL.glLinkProgram(program_id)

	if GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS) == GL.GL_FALSE:
		info_log = GL.glGetProgramInfoLog(program_id)
		if info_log != '': info_log = info_log.decode('ascii')
		raise ProgramLinkError(info_log)

@contextmanager.activatable
class Program:
	def __init__(self):
		self.id = GL.glCreateProgram()
		self.shader_ids = []
		self._uniform_locations = {}

	def add_shader(self, shader_type, shader_source):
		shader_id = create_shader(shader_type, shader_source)
		self.shader_ids.append(shader_id)

	def link(self):
		link_program(self.id, self.shader_ids)

	def activate(self):
		GL.glUseProgram(self.id)

	def get_uniform_location(self, name, silent=False):
		if name not in self._uniform_locations:
			location = uniform.get_uniform_location(self.id, name, silent=silent)
			if location != -1:
				self._uniform_locations[name] = location

		return self._uniform_locations[name]

class VertexFragmentProgram(Program):
	def __init__(self, vertex_shader, fragment_shader):
		super().__init__()
		self.add_shader(GL.GL_VERTEX_SHADER, vertex_shader)
		self.add_shader(GL.GL_FRAGMENT_SHADER, fragment_shader)
		self.link()
