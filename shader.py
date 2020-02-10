from .gl import GL

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

	for shader_id in shaders:
		GL.glAttachShader(program_id, shader_id)

	GL.glLinkProgram(program_id)

	if GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS) == GL.GL_FALSE:
		info_log = GL.glGetProgramInfoLog(program_id)
		if info_log != '': info_log = info_log.decode('ascii')
		raise ProgramLinkError(info_log)

	return program_id
