import unittest

from gllib import contextmanager

class TestContextManager(unittest.TestCase):
	@contextmanager.activatable
	class SimpleActivated:
		def __init__(self):
			self.activated = False
			self.active = False
			self.deactivated = False

		def activate(self):
			self.activated = True
			self.active = True

		def deactivate(self):
			self.active = False
			self.deactivated = True

	def test_default_activation(self):
		sa = self.SimpleActivated()

		self.assertFalse(sa.activated)
		self.assertFalse(sa.active)
		self.assertFalse(sa.deactivated)

		with sa as s:
			self.assertTrue(s.activated)
			self.assertTrue(s.active)
			self.assertFalse(s.deactivated)

		self.assertTrue(sa.activated)
		self.assertFalse(sa.active)
		self.assertTrue(sa.deactivated)

	@contextmanager.activatable
	class AlternativelyActivated:
		def __init__(self):
			self.activated = False
			self.active = False
			self.deactivated = False

		@contextmanager.activator
		def alternatively_activate(self):
			self.activated = True
			self.active = True

		def deactivate(self):
			self.active = False
			self.deactivated = True

	def test_alternative_activation(self):
		aa = self.AlternativelyActivated()

		self.assertFalse(aa.activated)
		self.assertFalse(aa.active)
		self.assertFalse(aa.deactivated)

		with aa.alternatively_activate() as a:
			self.assertTrue(a.activated)
			self.assertTrue(a.active)
			self.assertFalse(a.deactivated)

		self.assertTrue(aa.activated)
		self.assertFalse(aa.active)
		self.assertTrue(aa.deactivated)
