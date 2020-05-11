from igraph import Graph
import os, sys

OUTPUT_DIR = os.path.join(os.getcwd(), 'Random Graphs', 'igraph')
random_stats = {
    'BL': {
        'n': 10772,
        'p': 0.000265 # p value to use to get similar number of edges for BL
    },
    'AD': {
        'n': 24647,
        'p': 0.00014 # p value to use to get similar number of edges for AD 
    },
    'EX': {
        'n': 16787,
        'p': 0.0002 # p value to use to get similar number of edges for EX
    }
}

if not os.path.isdir(OUTPUT_DIR):
    try:
        os.mkdir(OUTPUT_DIR)
    except FileExistsError:
        print("Directory already exists. Not overwriting existing.")
        sys.exit(0)
g = Graph()
for stream, data in random_stats.items():
    for i in range(3):
        er_graph = g.Erdos_Renyi(data['n'], p=data['p'])
        out_file = os.path.join(OUTPUT_DIR, f"{stream}{i}.csv")
        with open(out_file, 'w') as f:
            er_graph.write_edgelist(f)