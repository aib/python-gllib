import collections

from . import sdl_runner

import sdl2

class Scene:
	def __init__(self, title, esc_to_exit=False):
		self.title = title
		self.esc_to_exit = esc_to_exit
		self.keys = collections.defaultdict(lambda: False)

	def gl_fps(self, fps):
		self.fps = fps
		self.update_title()

	def sdl_event(self, ev):
		if self.esc_to_exit and ev.type == sdl2.SDL_KEYUP and ev.key.keysym.sym == sdl2.SDLK_ESCAPE:
			return True
		elif ev.type == sdl2.SDL_KEYDOWN and ev.key.repeat == 0:
			key = sdl2.SDL_GetKeyName(ev.key.keysym.sym).decode('ascii').lower()
			self.key_down(key)
			self.keys[key] = True
		elif ev.type == sdl2.SDL_KEYUP and ev.key.repeat == 0:
			key = sdl2.SDL_GetKeyName(ev.key.keysym.sym).decode('ascii').lower()
			self.key_up(key)
			self.keys[key] = False

	def update_title(self):
		sdl2.SDL_SetWindowTitle(sdl2.SDL_GL_GetCurrentWindow(), f"{self.title} — {self.fps:.1f} FPS".encode('utf-8'))

	def get_runner(self):
		return sdl_runner.SdlRunner(self) \
			.set_title(self.title)

	def key_down(self, key):
		pass

	def key_up(self, key):
		pass
