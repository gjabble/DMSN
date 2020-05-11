import os
import csv
from pathlib import Path

cwd = os.path.dirname(os.path.realpath(__file__))
INPUT_DIR = os.path.join(cwd, "Random Graphs")

def convert_to_edge_list(matrix_file):
    edge_list = list()
    with open(matrix_file, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        header = list()
        for row in reader:
            if len(header) == 0:
                header = row[1:]
                continue
            node = row[0]
            adjacent_nodes = row[1:]
            for idx, adj in enumerate(adjacent_nodes):
                if int(adj) == 1:
                    edge = [min(node, header[idx]), max(node, header[idx])]
                    if edge not in edge_list:
                        edge_list.append(edge)
    out_name = f"{Path(matrix_file).stem}_edge_list.csv"
    out_path = os.path.join(INPUT_DIR, out_name)
    with open(out_path, 'w') as of:
        writer = csv.writer(of, delimiter=";")
        writer.writerow(['source', 'target'])
        for e in edge_list:
            writer.writerow(e)


with os.scandir(INPUT_DIR) as it:
    for entry in it:
        if entry.name.endswith('.csv') and entry.is_file():
            input_file = os.path.join(INPUT_DIR, entry.name)
            convert_to_edge_list(input_file)