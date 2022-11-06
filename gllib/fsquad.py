from .gl import GL
from . import shader
from . import util
from . import vao
from . import vbo

VERTEX_SHADER = """\
#version 100

attribute highp vec3 position;
attribute highp vec2 texCoords;

varying highp vec2 vf_texCoords;

void main()
{
	gl_Position = vec4(position, 1.);
	vf_texCoords = texCoords;
}
"""

FRAGMENT_SHADER = """\
#version 100

uniform sampler2D t_texture;

varying highp vec2 vf_texCoords;

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
				va.set_vertex_attribute(vb, 0, 2, GL.GL_FLOAT)

			with self.texcoords_vbo as vb:
				vb.set_data(util.to_float_array(TEXCOORDS))
				va.set_vertex_attribute(vb, 1, 2, GL.GL_FLOAT)

	def set_texture_unit(self, unit):
		with self.program as p:
			GL.glUniform1i(p.get_uniform_location('t_texture'), unit)

	def draw(self):
		with self.program:
			with self.vao:
				GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)
