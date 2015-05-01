'''
Matthew Beatty
CS51 Final Project
Q Comment Summarization
4/16/15
'''

# Import modules
import networkx as nx

def pagerank(node_list, edge_list, iteration_limit):
    graph = create_graph(node_list, edge_list)
    ranked_graph = rank_graph(graph, iteration_limit)
    ranked_nodes = {}
    for key in ranked_graph.node:
        value = ranked_graph.node[key]['weight']
        ranked_nodes.update({key: value})
    return ranked_nodes


"""
PageRank implementation
The function uses the edge weights between nodes to calculate new values for each iteration.
"""

def rank_graph(graph, propagation_cycles):

    temp_graph = graph
    prop_count = 0

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

# Create the pagerank graph from lists of weighted nodes and edges
def create_graph(node_list, edge_list):
    graph = nx.Graph()
    for node in node_list:
        graph.add_node(node[0], weight=(node[1]))
    for edge in edge_list:
        graph.add_edge(*edge)
    return graph