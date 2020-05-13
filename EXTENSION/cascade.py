import os
import json
import networkx as nx
import ndlib.models.ModelConfig as mc 
import ndlib.models.epidemics as ep 

cwd = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = os.path.join(cwd, "Original_Graphs")

# Calculate the seed nodes:
#   - highest degree centrality node
#   - neighbour of that node with highest degree centrality
def find_seeds(g):
    deg_cent = nx.degree_centrality(g)
    max_cent = max(deg_cent, key=lambda k: deg_cent[k])
    max_neighbour = max(g.neighbors(max_cent), key=lambda x: deg_cent[x])
    return [max_cent, max_neighbour]

# For each stream type simulate a cascade with 200 iterations 
# with specified threshold value 
def simulate_cascade(graph_path, threshold):
    g = nx.read_weighted_edgelist(graph_path, delimiter=";")
    model = ep.ThresholdModel(g)
    config = mc.Configuration()
    seed_nodes = find_seeds(g)
    config.add_model_initial_configuration("Infected", seed_nodes) # only seed nodes start as infected
    for i in g.nodes():
        config.add_node_configuration('threshold', i, threshold) # set threshold to be the same for all nodes
    model.set_initial_status(config)
    iterations = model.iteration_bunch(50) # execute 50 iterations 
    return iterations

OUTPUT_DIR = os.path.join(cwd, 'Cascades')
with os.scandir(INPUT_DIR) as it:
    for entry in it:
        if entry.name.endswith('.csv') and entry.is_file():
            graph_path = os.path.join(INPUT_DIR, entry.name)
            cascade_data = dict()
            thresholds = [0.25, 0.75]
            for thresh in thresholds:
                cascade = simulate_cascade(graph_path, thresh)
                cascade_data[thresh] = cascade
            stream = f"{entry.name.split('_')[1]}.json"
            out_file = os.path.join(OUTPUT_DIR, stream)
            with open(out_file, 'w') as of:
                json.dump(cascade_data, of)
            