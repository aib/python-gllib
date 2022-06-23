import math

import numpy

def dot3(v0, v1):
	return v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2]

def cross3(v0, v1):
	return numpy.array([v0[1]*v1[2] - v0[2]*v1[1], v0[2]*v1[0] - v0[0]*v1[2], v0[0]*v1[1] - v0[1]*v1[0]])

def norm3(v):
	return math.sqrt(dot3(v, v))

def normalize3(v):
	return v / norm3(v)
