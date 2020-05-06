from igraph import *
from utils import *
from collections import Counter
import os, json

BASE_PATH = os.path.join(os.getcwd(), 'edge_lists')
edge_lists = list()
with os.scandir(BASE_PATH) as elists:
    for elist in elists:
        if "weighted." in elist.name:
            edge_lists.append(elist.name)

for e in edge_lists:
    g = create_graph(BASE_PATH, e)
    communities = g.community_multilevel(weights='weight')
    dendrogram = Dendrogram(communities)
    print(dendrogram)
    hashtag_communities = dict()
    for idx, community in enumerate(communities):
        hashtag_communities[idx] = dict()
        hashtags = list()
        for node in community:
            hashtags.append(g.vs[node]['name'])
        hashtag_communities[idx] = hashtags
    #community_sizes = Counter([len(hashtag_communities[c]) for c in [k for k in hashtag_communities.keys()]]).most_common()
    #print(len(hashtag_communities), community_sizes)
    outfile = e.split('_')[1]
    save_communities(hashtag_communities, outfile)