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


def pagerank(edge_list, alpha, iteration_limit):
    graph = create_graph(edge_list)
    ranked_graph = rank_graph(graph, alpha, iteration_limit)
    ranked_nodes = {}
    for key in ranked_graph.node:
        value = ranked_graph.node[key]["value"]
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
                graph.node[n]['value'] += edge_weight/total_edge_weight

            temp_graph = normalize(temp_graph)
            prop_count += 1

        return temp_graph


# Normalize node values
def normalize(graph):

    total_value = 0.0
    for node in graph.__iter__():
        total_value += graph.node[node]['value']
    for node in graph.__iter__():
        graph.node[node]['value'] = graph.node[node]['value']/total_value
    return graph


def create_graph(edge_list):
    graph = nx.Graph()
    for edge in edge_list:
        graph.add_edge(*edge)
    nx.set_node_attributes(graph, 'value', 1.0)
    return graph