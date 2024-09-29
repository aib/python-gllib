import ctypes

from gllib.gl import GL
import gllib.shader
import gllib.vao
import gllib.vbo
import gllib.sdl_runner

VS = """\
attribute vec3 position;
attribute vec3 color;
varying vec3 vf_color;

void main() {
	gl_Position = vec4(position, 1.0);
	vf_color = color;
}
"""

FS = """\
varying vec3 vf_color;

void main() {
	gl_FragColor = vec4(vf_color, 1.0);
}
"""

def main():
	class TriangleScene:
		def gl_init(self, size):
			GL.glClearColor(0, 0, 0, 0)

			self.program = gllib.shader.Program()
			self.program.add_shader(GL.GL_VERTEX_SHADER, VS)
			self.program.add_shader(GL.GL_FRAGMENT_SHADER, FS)
			self.program.link()
			self.vao = gllib.vao.VAO()
			self.pos_vbo = gllib.vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)
			self.col_vbo = gllib.vbo.VBO(GL.GL_ARRAY_BUFFER, GL.GL_STATIC_DRAW)

			with self.pos_vbo as vb:
				vb.set_data(
					(ctypes.c_double * 9)(
						 0.0, +0.77, 0.0,
						-0.5, -0.77, 0.0,
						+0.5, -0.77, 0.0,
					)
				)

			with self.col_vbo as vb:
				vb.set_data(
					(ctypes.c_double * 9)(
						1.0, 0.0, 0.0,
						0.0, 1.0, 0.0,
						0.0, 0.0, 1.0,
					)
				)

			with self.vao as va:
				with self.pos_vbo as vb:
					va.set_vertex_attribute(vb, 0, 3, GL.GL_DOUBLE)
				with self.col_vbo as vb:
					va.set_vertex_attribute(vb, 1, 3, GL.GL_DOUBLE)

		def gl_render(self):
			GL.glClear(GL.GL_COLOR_BUFFER_BIT)

			with self.program as p:
				with self.vao:
					GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

	gllib.sdl_runner.SDLRunner(TriangleScene()).run()

if __name__ == '__main__':
	main()
