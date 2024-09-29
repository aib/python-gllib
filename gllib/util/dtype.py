from ..gl import GL

import numpy

DTYPE_TO_GL = {
	numpy.float32: GL.GL_FLOAT,
	numpy.float64: GL.GL_DOUBLE,
	numpy.int8: GL.GL_BYTE,
	numpy.uint8: GL.GL_UNSIGNED_BYTE,
	numpy.int16: GL.GL_SHORT,
	numpy.uint16: GL.GL_UNSIGNED_SHORT,
	numpy.int32: GL.GL_INT,
	numpy.uint32: GL.GL_UNSIGNED_INT,
}

def dtype_to_gl(dtype):
	gltype = DTYPE_TO_GL.get(dtype, None)
	if gltype is None:
		raise Exception(f"No corresponding OpenGL type for dtype \"{dtype}\"")
	else:
		return gltype
