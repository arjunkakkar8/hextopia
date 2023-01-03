class Node:
	def __init__(self, id = None, color = None, minority = None, neighbour_ids = []):
		self.id = id
		self.color = color
		self.minority = minority
		self.neighbour_ids = neighbour_ids
		self.region_id = None

	def getNeighbours(self):
		return self.neighbours