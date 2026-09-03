import csv

import networkx as nx
import numpy as np

G = nx.Graph()
penguin_dict = {}
penguin_descrip_dict = {}

with open("Penguins of Kyoto - Metadata.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)
    j = 0
    for row in reader:
        G.add_node(row[0], sex=row[1], info=row[2].split(" and "))
        penguin_dict[j] = row[0]
        penguin_descrip_dict[j] = row[2].split(" and ")
        j += 1

num_penguins = len(G.nodes)

for relationship in ["Couples", "Exes", "Complicated", "Friends", "Enemies", "Family"]:
    couples_matrix = np.zeros((num_penguins, num_penguins))

    with open(f"csv/Penguins of Kyoto - {relationship}.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        j = 0
        for row in reader:
            row_list = [int(i) for i in row[1:]]
            couples_matrix[j, :] = row_list
            j += 1

    couples_graph = nx.from_numpy_array(couples_matrix, create_using=nx.DiGraph)
    couples_graph = nx.relabel_nodes(couples_graph, penguin_dict)
    nx.set_node_attributes(couples_graph, penguin_descrip_dict)

    if relationship is not "Family":
        couples_md_dict = {}
        with open(f"csv/Penguins of Kyoto - {relationship} metadata.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)
            for row in reader:
                couples_md_dict[(row[0], row[1])] = row[2]
        nx.set_edge_attributes(couples_graph, couples_md_dict, "info")

    nx.write_gexf(couples_graph, f"gexf/Penguin_{relationship}.gexf")
