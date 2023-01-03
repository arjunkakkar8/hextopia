import random
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

from config import NUM_REGIONS, NUM_NODES_PER_REGION, COMPACTNESS_THRESHOLD
from region import Region
from node import Node
from graph import graph

graph_boundary = [node for node in graph if len(node.neighbour_ids) < 6]

def visualize(node_list):
	G = nx.Graph()

	for node in node_list:
		G.add_node(node.id, color = node.color, minority = node.minority, title = str(node.id), label = str(node.region_id), group = node.region_id)
		G.add_edges_from([(node.id, neighbour_id) for neighbour_id in node.neighbour_ids])

	net = Network(select_menu=True)
	net.from_nx(G)
	net.show_buttons()
	net.show('../output/graph.html')

	# node_colors = [node.color for node in node_list]
	# node_labels = {node.id: node.id for node in node_list}
	# node_sizes = [500 if node.minority else 300 for node in node_list]
	# nx.draw_kamada_kawai(G, node_color = node_colors, labels = node_labels, node_size=node_sizes)
	# nx.draw_networkx_nodes(G, pos = nx.kamada_kawai_layout(G), node_color = node_colors)
	# plt.savefig('graph.png')

def runIteration(boundary_count = 8):
	for node in graph:
		node.region_id = None
	regions = []
	boundary_seeds = random.choices(graph_boundary, k = boundary_count)
	interior_seeds = random.choices(graph, k = NUM_REGIONS - boundary_count)
	# interior_seeds = [graph[27], graph[96]]
	seeds = boundary_seeds + interior_seeds
	stop_signal = False

	for i, seed in enumerate(seeds): 
		region = Region(i, [seed])
		regions.append(region)

	while not stop_signal:
		stop_signal = True

		for region in regions:
			if len(region.nodes) == NUM_NODES_PER_REGION:
				continue

			stop_signal = False
			growth = region.growBoundary()

			if not growth:
				return []

	return regions

def runExperiment(min_wins = 8, min_minority = 2, min_compact = 8, boundary_count = 8):
	regions = []
	minority = 0
	compact = 0
	purple = 0
	iter_num = 0

	while len(regions) == 0 or minority < min_minority or compact < min_compact or NUM_REGIONS - min_wins < purple < min_wins:
		purple = 0
		minority = 0
		compact = 0
		iter_num += 1

		regions = runIteration(boundary_count)
		
		for region in regions:
			compact += region.getPerimeter() < COMPACTNESS_THRESHOLD
			minority += region.getMinority()
			purple += region.getWinner() == 'purple'

		if not len(regions) == 0:
			print('Trying iteration:', iter_num, minority, compact, purple)

	print('Success! Compact Regions:', compact, 'Minority Regions:', minority)
	for region in regions:
		print(region.id, region.getWinner(), region.getPerimeter(), region.getStats())

	visualize(graph)

## Run experiment to find configuration satisfying minimum
## constraints
runExperiment(min_wins = 8, min_compact = 9, boundary_count = 7)

## Run isolated iteration
# runIteration(8)
# visualize(graph)
