from . import vector

import math

import numpy

def identity(dtype=None):
	return numpy.array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	], dtype=dtype)

def translate(v, dtype=None):
	return numpy.array([
		[1, 0, 0, v[0]],
		[0, 1, 0, v[1]],
		[0, 0, 1, v[2]],
		[0, 0, 0,   1 ]
	], dtype=dtype)

def scale(s, dtype=None):
	return numpy.array([
		[s, 0, 0, 0],
		[0, s, 0, 0],
		[0, 0, s, 0],
		[0, 0, 0, 1]
	], dtype=dtype)

# https://en.wikipedia.org/wiki/Euler%E2%80%93Rodrigues_formula
def rotate(axis, theta, dtype=None):
	a = numpy.cos(theta / 2)
	b, c, d = vector.normalize3(axis) * -math.sin(theta / 2)
	aa, bb, cc, dd = a * a, b * b, c * c, d * d
	bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
	return numpy.array([
		[aa + bb - cc - dd,   2 * (bc + ad),     2 * (bd - ac),   0 ],
		[  2 * (bc - ad),   aa + cc - bb - dd,   2 * (cd + ab),   0 ],
		[  2 * (bd + ac),     2 * (cd - ab),   aa + dd - bb - cc, 0 ],
		[        0,                 0,                 0,         1 ]
	], dtype=dtype)

def rotate3(axis, theta, dtype=None):
	return rotate(axis, theta, dtype=dtype)[0:3, 0:3]

def perspective(fovy, aspect, zNear, zFar, dtype=None):
	f = 1 / math.tan(fovy / 2)
	M = numpy.array([
		[f/aspect, 0,                0,                                   0               ],
		[    0,    f,                0,                                   0               ],
		[    0,    0, (zFar + zNear) / (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar)],
		[    0,    0,               -1,                                   0               ]
	], dtype=dtype)
	return M

def lookAt(eye, center, up, dtype=None):
	eye, center, up = numpy.asarray(eye), numpy.asarray(center), numpy.asarray(up)
	f = vector.normalize3(center - eye)
	s = vector.normalize3(vector.cross3(f, up))
	u = vector.cross3(s, f)
	M = numpy.array([
		[ s[0],  s[1],  s[2], 0],
		[ u[0],  u[1],  u[2], 0],
		[-f[0], -f[1], -f[2], 0],
		[  0,     0,     0,   1]
	], dtype=dtype)
	return M @ translate(-eye, dtype=dtype)
