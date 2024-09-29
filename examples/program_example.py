import ctypes

from gllib.gl import GL
import gllib.program
import gllib.vao
import gllib.vbo
import gllib.sdl_runner
from gllib.scene import Scene

VS = """\
#version 330

in vec3 position;
in vec3 color;
out vec3 vf_color;

void main() {
	gl_Position = vec4(position, 1.0);
	vf_color = color;
}
"""

FS = """\
#version 330

in vec3 vf_color;
out vec4 fragColor;

void main() {
	fragColor = vec4(vf_color, 1.0);
}
"""

def main():
	class TriangleScene(Scene):
		def __init__(self):
			super().__init__("Program Example", esc_to_exit=True)

		def gl_init(self, size):
			GL.glClearColor(0, 0, 0, 0)

			self.program = gllib.program.Program(vertex_shader=VS, fragment_shader=FS)

			pos = self.program.create_attribute((3, 3), 'position')
			pos[:] = [
				[ 0.0, +0.77, 0.0],
				[-0.5, -0.77, 0.0],
				[+0.5, -0.77, 0.0],
			]

			col = self.program.create_attribute((3, 3)) # location 1 because this is the second attribute
			col[:] = [
				[1.0, 0.0, 0.0],
				[0.0, 1.0, 0.0],
				[0.0, 0.0, 1.0],
			]

		def gl_render(self):
			GL.glClear(GL.GL_COLOR_BUFFER_BIT)
			self.program.draw_arrays(GL.GL_LINE_LOOP)

	TriangleScene().get_runner() \
		.set_fullscreen(False) \
		.set_resolution_by_scale(.9) \
		.run()

if __name__ == '__main__':
	main()
