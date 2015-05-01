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


def pagerank(node_list, edge_list, alpha, iteration_limit):
    '''node_list = [("test", 0.9), ("midterm", 2.1), ("exam", 1.4), ("professor", 0.5), ("music", 1.9), ("teacher", 2.9)]
    edge_list = [("test", "midterm", {'weight': 0.9}), ("test", "exam", {'weight': 0.8}), ("test", "professor", {'weight': 0.7}),
                     ("test", "teacher", {'weight': 0.8}), ("test", "music", {'weight': 0.6}), ("exam", "midterm", {'weight': 0.2}), ("professor", "midterm", {'weight': 0.2}),
                     ("midterm", "teacher", {'weight': 0.0}), ("midterm", "music", {'weight': 0.1}), ("professor", "exam", {'weight': 0.2}), ("exam", "teacher", {'weight': 0.2}),
                     ("exam", "music", {'weight': 0.5}),("professor", "teacher", {'weight': 0.2}), ("professor", "music", {'weight': 0.5}),
                     ("teacher", "music", {'weight': 0.5})]'''
    graph = create_graph(node_list, edge_list)
    ranked_graph = rank_graph(graph, alpha, iteration_limit)
    ranked_nodes = {}
    for key in ranked_graph.node:
        value = ranked_graph.node[key]['weight']
        ranked_nodes.update({key: value})
    return ranked_nodes


"""
PageRank implementation
Will not implement random surfer now, might want to later...
"""


def rank_graph(graph, alpha, propagation_cycles):

    temp_graph = graph
    prop_count = 0
    # dampening = 1 - alpha

    while prop_count < propagation_cycles:

        for node in temp_graph.__iter__():
            total_edge_weight = 0.0
            for neighbor_node in temp_graph.neighbors(node):
                total_edge_weight += graph[node][neighbor_node]['weight']
            for n in temp_graph.neighbors(node):
                edge_weight = graph[node][n]['weight']
                graph.node[n]['weight'] += edge_weight/total_edge_weight

            temp_graph = normalize(temp_graph)
        prop_count += 1

    return temp_graph


# Normalize node values
def normalize(graph):

    total_value = 0.0
    for node in graph.__iter__():
        total_value += graph.node[node]['weight']
    for node in graph.__iter__():
        graph.node[node]['weight'] = graph.node[node]['weight']/total_value
    return graph


def create_graph(node_list, edge_list):
    graph = nx.Graph()
    for node in node_list:
        graph.add_node(node[0], weight = (node[1]))
    for edge in edge_list:
        graph.add_edge(*edge)
    return graph

pg = pagerank([], [], 0.15, 100)