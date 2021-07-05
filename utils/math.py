class Vector2(object):
	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y

	def get_coords(self):
		return (self.x, self.y,)