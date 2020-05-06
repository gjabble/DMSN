from igraph import *
import csv, os, json

def read_edges(path):
    edges = list()
    with open(path, 'r') as e:
        r = csv.reader(e, delimiter=";")
        next(r)
        for row in r:
            row[2] = int(row[2])
            edges.append(tuple(row))
    return edges

def create_graph(base_path, edge_file):
    path = os.path.join(base_path, edge_file)
    edge_list = read_edges(path)
    return Graph.TupleList(edge_list, directed=False, weights=True)

def nodes_with_degree(graph, degree):
    degrees = graph.degree()
    labels = [graph.vs[idx]['name'] for idx, d in enumerate(degrees) if graph.vs[idx].degree() == degree]
    return labels

def save_communities(community_list, file_name):
    base_path = os.path.join(os.getcwd(), 'Communities')
    file_name = file_name + ".json"
    with open(os.path.join(base_path, file_name), 'w') as c:
        json.dump(community_list, c)