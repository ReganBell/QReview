'''
Matthew Beatty
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

    def __init__(self, edge_list, alpha, iteration_limit):
        edge_list = [("test", "midterm", {'weight': 0.9}), ("test", "exam", {'weight': 0.8}), ("test", "professor", {'weight': 0.7}),
                     ("test", "teacher", {'weight': 0.8}), ("test", "music", {'weight': 0.6}), ("exam", "midterm", {'weight': 0.2}), ("professor", "midterm", {'weight': 0.2}),
                     ("midterm", "teacher", {'weight': 0.0}), ("midterm", "music", {'weight': 0.1}), ("professor", "exam", {'weight': 0.2}), ("exam", "teacher", {'weight': 0.2}),
                     ("exam", "music", {'weight': 0.5}),("professor", "teacher", {'weight': 0.2}), ("professor", "music", {'weight': 0.5}),
                     ("teacher", "music", {'weight': 0.5})]
        self.graph = self._create_graph(edge_list)
        self.pagerank_graph = self._pagerank(self.graph, alpha, iteration_limit)
        self._print_results(self.pagerank_graph)


    # PageRank implementation
    # will not implement random surfer now, might want to later...
    def _pagerank(self, graph, alpha, propogation_cycles):

        temp_graph = graph
        prop_count = 0
        dampening = 1 - alpha

        while prop_count < propogation_cycles:

            for node in temp_graph.__iter__():
                total_edge_weight = 0.0
                for neighbornode in temp_graph.neighbors(node):
                    total_edge_weight += graph[node][neighbornode]['weight']
                for n in temp_graph.neighbors(node):
                    edge_weight = graph[node][n]['weight']
                    graph.node[n]['value'] += edge_weight/total_edge_weight

            temp_graph = self._normalize(temp_graph)
            prop_count += 1

        return temp_graph

    # Normalize node values
    def _normalize(self, graph):

        total_value = 0.0
        for node in graph.__iter__():
            total_value += graph.node[node]['value']
        for node in graph.__iter__():
            graph.node[node]['value'] = graph.node[node]['value']/total_value
        return graph

    def _create_graph(self, edge_list):
        graph = nx.Graph()
        for edge in edge_list:
            graph.add_edge(*edge)
        nx.set_node_attributes(graph, 'value', 1.0)
        return graph

    def _print_results(self, graph):
        nx.info(graph)



pg = PageRank([], 0.15, 100)