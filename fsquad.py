from .gl import GL
from . import shader
from . import util
from . import vao
from . import vbo

VERTEX_SHADER = """\
#version 110

attribute vec2 texCoords;

varying vec2 vf_texCoords;

void main()
{
	gl_Position = gl_Vertex;
	vf_texCoords = texCoords;
}
"""

FRAGMENT_SHADER = """\
#version 110

uniform sampler2D t_texture;

varying vec2 vf_texCoords;

void main()
{
	gl_FragColor = texture2D(t_texture, vf_texCoords);
}
"""

VERTICES  = util.flatten([(-1., +1.), (-1., -1.), (+1., +1.), (+1., -1.)])
TEXCOORDS = util.flatten([( 0.,  1.), ( 0.,  0.), ( 1.,  1.), ( 1.,  0.)])

class FSQuad:
	def __init__(self):
		self.program = shader.VertexFragmentProgram(VERTEX_SHADER, FRAGMENT_SHADER)
		self.vao = vao.VAO()
		self.vertices_vbo = vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
		self.texcoords_vbo = vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)

		with self.vao as va:
			with self.vertices_vbo as vb:
				vb.set_data(util.to_float_array(VERTICES))
				va.set_vertex_attrib(vb, 0, 2, GL.GL_FLOAT)

			with self.texcoords_vbo as vb:
				vb.set_data(util.to_float_array(TEXCOORDS))
				va.set_vertex_attrib(vb, 1, 2, GL.GL_FLOAT)

	def set_texture_unit(self, unit):
		with self.program as p:
			GL.glUniform1i(p.get_uniform_location('t_texture'), unit)

	def draw(self):
		with self.program:
			with self.vao:
				GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)
