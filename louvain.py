import networkx as nx
import community
import os

EDGE_LIST_PATH = os.path.join(os.getcwd(), 'edge_lists')
edge_lists = list()
with os.scandir(EDGE_LIST_PATH) as elists:
    for elist in elists:
        edge_lists.append(os.path.join(EDGE_LIST_PATH, elist.name))

for e in edge_lists:
    G = nx.read_weighted_edgelist(e, delimiter=";")
    partition = community.best_partition(G, weight='weight')
    size = float(len(set(partition.values())))
    mod = community.modularity(partition, G, weight='weight')
    print(size, mod)
    dendo = community.generate_dendrogram(G)
    #for level in range(len(dendo) - 1):
    #    print("partition at level ", level, " is ", community.partition_at_level(dendo, level))
