from .gl import GL

import time

import sdl2

class SdlRunner:
	def __init__(self, scene):
		self.scene = scene
		self.fullscreen = True
		self.title = ""
		self.vsync = None
		self.fps_calc_time = 1
		self.width = None
		self.height = None

		sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
		self.set_resolution_by_scale(1)

	def set_fullscreen(self, fullscreen):
		self.fullscreen = fullscreen
		return self

	def set_title(self, title):
		self.title = title
		return self

	def set_vsync(self, vsync):
		self.vsync = vsync
		return self

	def set_fps_calc_time(self, fps_calc_time):
		self.fps_calc_time = fps_calc_time
		return self

	def set_resolution(self, width, height):
		self.width = width
		self.height = height
		return self

	def set_resolution_by_scale(self, scale):
		dm = sdl2.SDL_DisplayMode()
		sdl2.SDL_GetDesktopDisplayMode(0, dm)
		return self.set_resolution(round(dm.w * scale), round(dm.h * scale))

	def run(self):
		window_flags = sdl2.SDL_WINDOW_OPENGL | (sdl2.SDL_WINDOW_FULLSCREEN if self.fullscreen else 0)
		window = sdl2.SDL_CreateWindow(self.title.encode('utf-8'), sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED, self.width, self.height, window_flags)
		context = sdl2.SDL_GL_CreateContext(window)

		if self.vsync is not None:
			if self.vsync:
				if sdl2.SDL_GL_SetSwapInterval(-1) == -1:
					sdl2.SDL_GL_SetSwapInterval(1)
			else:
				sdl2.SDL_GL_SetSwapInterval(0)

		try:
			self._safe_call_scene('gl_init', (self.width, self.height))
			self._run_event_loop(window, context)
			self._safe_call_scene('gl_quit')
		finally:
			sdl2.SDL_GL_DeleteContext(context)
			sdl2.SDL_DestroyWindow(window)
			sdl2.SDL_Quit()

	def _run_event_loop(self, window, context):
		ev = sdl2.SDL_Event()

		frames = 0
		frame_count_time = last_update_time = time.perf_counter()

		while True:
			now = time.perf_counter()

			while True:
				if sdl2.SDL_PollEvent(ev) == 0:
					break

				if ev.type == sdl2.SDL_QUIT:
					return

				quit = self._safe_call_scene('sdl_event', ev)
				if quit:
					return

			self._safe_call_scene('gl_update', now - last_update_time)
			last_update_time = now

			self._safe_call_scene('gl_render')
			sdl2.SDL_GL_SwapWindow(window)

			frames += 1
			elapsed = now - frame_count_time
			if elapsed > self.fps_calc_time:
				fps = frames / elapsed
				frames = 0
				frame_count_time = now
				self._safe_call_scene('gl_fps', fps)

	def _safe_call_scene(self, func, *args, **kwargs):
		if hasattr(self.scene, func):
			func = getattr(self.scene, func)

		if callable(func):
			return func(*args, **kwargs)
