from .gl import GL

class ShaderCompileError(Exception):
	def __init__(self, info_log):
		super().__init__("Error compiling shader: %s" % (info_log,))

def create_shader(shader_type, shader_source):
	shader_id = GL.glCreateShader(shader_type)
	GL.glShaderSource(shader_id, shader_source)
	GL.glCompileShader(shader_id)

	if GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS) == GL.GL_FALSE:
		info_log = GL.glGetShaderInfoLog(shader_id)
		if info_log != '': info_log = info_log.decode('ascii')
		raise ShaderCompileError(info_log)

	return shader_id
