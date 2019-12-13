# class definitions for raycasting.py

class Point():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Vector():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class RGB_Float():
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

class Sphere():
	def __init__(self, center, radius, color):
		self.center = center
		self.radius = radius
		self.color = color