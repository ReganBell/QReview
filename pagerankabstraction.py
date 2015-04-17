'''
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/16/15
'''

# Import modules
import networkx as nx


'''

We import the NetworkX library to use their DiGraph (directed graph) for our PageRank algorithm.

'''

class PageRank(object):

	'''
	Init Function
	'''

	def __init__(edges_weight_list, dampening):
		self.graph = _create_graph
		self._pagerank = _pagerank(G, dampening, propogation_cycles)
		G = nx.DiGraph()
		G.add_edges_from(edges_weight_list)
		self.nodescores = retrievePageRankNodeScores(self._pagerank)


	'''
	Private Methods
	'''

	# PageRank implementation
	def _pagerank(graph, dampening, propogation_cycles):
		return TODO
		# Will have to create node list for retrievePageRankNodeScores

	'''
	PageRank Helpers
	'''

	# Normalize node values
	def _normalize(graph):
		return TODO

	# Propogate node values
	def _calculatePropogation(graph):
		return TODO

	# Return the results of PageRank on graph
	# should return list of objects with (Vertice * Value)
	def retrievePageRankNodeScores(graph):
		return TODO

