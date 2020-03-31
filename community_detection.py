import networkx as nx
from networkx.algorithms import community
from networkx import edge_betweenness_centrality as betweenness
import csv, os, shutil

input_directory = os.path.join(os.getcwd(), 'co_occurrence_data')
base_output_dir = os.path.join(os.getcwd(), 'communities')

if not os.path.isdir(base_output_dir):
    try:
        os.mkdir(base_output_dir)
    except OSError:
        print("Failed to create the base output directory.")

def get_input_data():
    files = list()
    if os.path.isdir(input_directory):
        with os.scandir(input_directory) as d:
            for entry in d:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(os.path.join(input_directory, entry))
    return files

def import_edge_list(fname):
    weighted_edges = dict()
    weighted_edge_list = list()
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            row = sorted(row)
            weight = weighted_edges.get(row[0], {}).get(row[1])
            if weight:
                weighted_edges[row[0]][row[1]] += 1
            else:
                weighted_edges[row[0]] = dict()
                weighted_edges[row[0]][row[1]] = 1

    for src, vals in weighted_edges.items():
        for dest, weight in vals.items():
            weighted_edge_list.append((src, dest, weight))
    return weighted_edge_list

input_data = get_input_data()
for inp in input_data:
    edge_list = import_edge_list(inp)
    G = nx.Graph()
    G.add_weighted_edges_from(edge_list)
    community_generator = community.girvan_newman(G)
    communities = list(sorted(c) for c in next(community_generator))
    smallest = len(min(communities, key=lambda x: len(x)))
    largest = len(max(communities, key=lambda x: len(x)))
    print("Number of communities: {}\nSmallest community: {}\nLargest community: {}".format(len(communities), smallest, largest))

    # Output communities to files in a new subdirectory
    #stream_type = os.extsep(os.path.split(inp)[-1])
    stream_type = os.path.split(inp)[-1].split(os.extsep)[0]
    output_dir = os.path.join(base_output_dir, stream_type)
    if os.path.isdir(output_dir):
        try:
            shutil.rmtree(output_dir)
        except OSError:
            print("Failed to delete sub-directory: {}".format(output_dir))
    try:
        os.mkdir(output_dir)
    except OSError:
        print("Failed to create output directory: {}".format(output_dir))

    for index, cmnty in enumerate(communities):
        community_path = "{}_community_{}.csv".format(stream_type, index)
        with open(os.path.join(output_dir, community_path), "w") as f:
            f.write("\n".join(cmnty))
