from .dtype import *

import ctypes
import itertools

def flatten(xs):
	return list(itertools.chain.from_iterable(xs))

def to_float_array(buf):
	return (ctypes.c_float * len(buf))(*buf)
