from igraph import *
from utils import *
import matplotlib.pyplot as plt
import os

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10,6))
line_types = ['bo-', 'ro-', 'go-']
BASE_PATH = os.path.join(os.getcwd(), 'edge_lists')
edge_lists = list()
with os.scandir(BASE_PATH) as elists:
    for elist in elists:
        if "weighted." in elist.name:
            edge_lists.append(elist.name)

for idx, e in enumerate(edge_lists):
    g = create_graph(BASE_PATH, e)
    degrees = g.degree()
    max_degree = max(degrees)
    max_degree_tags = nodes_with_degree(g, max_degree)
    max_degree_count = len(max_degree_tags)
    min_degree = min(degrees)
    min_degree_tags = nodes_with_degree(g, min_degree)
    min_degree_count = len(min_degree_tags)
    print("=== {} STATS ===\n".format(e),
        "nodes: {}\n".format(len(g.vs)),
        "edges: {}\n".format(len(g.es)),
        "max degree: {} `{}`\n".format(max_degree, max_degree_tags),
        "nodes with max degree: {}\n".format(max_degree_count),
        "min degree: {}\n".format(min_degree),
        "nodes with min degree: {}\n".format(min_degree_count),
        "====================\n")

    unique_degrees = sorted(set(degrees))
    degree_counts = [degrees.count(x) for x in unique_degrees]
    label = e.split('_')[1]
    ax.loglog(unique_degrees, degree_counts,  line_types[idx], label=label)
    ax.set_title("Degree distribution of hashtag co-occurrence")
    ax.set_xlabel("Degree")
    ax.set_ylabel("Number of nodes")
    ax.legend()
    #plt.show()
    plt.savefig('./Plots/degree_distribution.png')