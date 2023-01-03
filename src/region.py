import copy
from config import NUM_NODES_PER_REGION
from graph import graph

class Region:
	def __init__(self, id = None, nodes = []):
		self.id = id
		self.nodes = nodes
		self.boundary_nodes = copy.deepcopy(nodes)

		for node in nodes:
			node.region_id = id

	def getStats(self):
		stats = {
			"purple": 0,
			"yellow": 0,
			"minority": 0,
			"total": len(self.nodes)
		}

		for node in self.nodes:
			stats["yellow"] += node.color == 'yellow'
			stats["purple"] += node.color == 'purple'
			stats["minority"] += node.minority

		return stats

	def getPerimeter(self):
		perimeter = 6 * NUM_NODES_PER_REGION
		for node in self.nodes:
			for neighbour_id in node.neighbour_ids:
				if graph[neighbour_id].region_id == self.id:
					perimeter -= 1
		return perimeter


	def getMinority(self): 
		minority = 0
		for node in self.nodes:
			minority += node.minority

		return minority > NUM_NODES_PER_REGION/2

	def getWinner(self):
		if(len(self.nodes) < NUM_NODES_PER_REGION):
			return None

		yellow = 0

		for node in self.nodes:
			yellow += node.color == 'yellow'

		return 'yellow' if yellow > NUM_NODES_PER_REGION/2 else 'purple'

	def growBoundary(self):
		new_nodes = []
		for node in self.boundary_nodes:
			for neighbour_id in node.neighbour_ids:
				if len(self.nodes) == NUM_NODES_PER_REGION:
					break

				if graph[neighbour_id].region_id is None:
					# print('Added node', neighbour_id)
					graph[neighbour_id].region_id = self.id
					self.nodes.append(graph[neighbour_id])
					new_nodes.append(graph[neighbour_id])

		self.boundary_nodes = new_nodes

		if len(self.nodes) < NUM_NODES_PER_REGION and len(new_nodes) == 0:
			return False

		return True