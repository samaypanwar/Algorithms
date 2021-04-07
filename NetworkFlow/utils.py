import yaml
import math
import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os

os.path
with open('config.yaml') as config:
    configurations = yaml.safe_load(config)
config.close()

try:

    MAX_LAYERS = configurations.get("MAX_LAYERS")  # defines max number of layers in the graph
    MAX_SIZE_LAYERS = configurations.get("MAX_SIZE_LAYERS")  # defines max size for each layer in the graph
    MAX_CAPACITY = configurations.get("MAX_CAPACITY")  # defines the max capacity of an edge
    EDGE_DENSITY_FORWARD = configurations.get("EDGE_DENSITY_FORWARD")  # defines the forward edge density at each layer
    EDGE_DENSITY_BACKWARDS = configurations.get("EDGE_DENSITY_BACKWARDS")  # defines the backwards edge density at each layer
    EDGE_DENSITY_SIDE = configurations.get("EDGE_DENSITY_SIDE")  # defines the side edge density at each layer
    

except: raise ValueError('Configurations for Network not yet set')

LAYERS = [rd.randint(2, MAX_SIZE_LAYERS) if 0 < i <= MAX_LAYERS else 1 \
            for i in range(MAX_LAYERS + 2)]
NODES = sum(LAYERS)
INFINITY = math.inf

# function that creates the graph
def make_graph():

    g = [[] for i in range(len(LAYERS)) for j in range(LAYERS[i])]

    for n_out in range(LAYERS[1]):
        g[0].append([1 + n_out, rd.randint(1, MAX_CAPACITY)])
    for n_in in range(LAYERS[-2]):
        g[len(g) - 1 + n_in - LAYERS[-2]].append(
            [len(g) - 1, rd.randint(1, MAX_CAPACITY)]
        )

    start_index = 1
    for l in range(1, MAX_LAYERS):
        for n_in in range(LAYERS[l]):
            for n_out in range(LAYERS[l + 1]):
                to_add = (
                    (MAX_SIZE_LAYERS * MAX_SIZE_LAYERS - LAYERS[l] * LAYERS[l + 1])
                    * (1 - EDGE_DENSITY_FORWARD)
                    / (MAX_SIZE_LAYERS * MAX_SIZE_LAYERS)
                )
                if rd.uniform(0, 1) < EDGE_DENSITY_FORWARD + to_add:
                    g[start_index + n_in].append(
                        [start_index + LAYERS[l] + n_out, rd.randint(1, MAX_CAPACITY)]
                    )

            if n_in != LAYERS[l] and rd.uniform(0, 1) < EDGE_DENSITY_SIDE:
                if rd.uniform(0, 1) < 0.5:
                    g[start_index + n_in].append(
                        [start_index + n_in + 1, rd.randint(1, MAX_CAPACITY)]
                    )
                else:
                    g[start_index + n_in + 1].append(
                        [start_index + n_in, rd.randint(1, MAX_CAPACITY)]
                    )

        for n_in in range(LAYERS[l]):
            for n_out in range(LAYERS[l + 1]):
                if rd.uniform(0, 1) < EDGE_DENSITY_BACKWARDS:
                    found = False
                    for j in range(len(g[start_index + n_in])):
                        if (
                            g[start_index + n_in][j][0]
                            == start_index + LAYERS[l] + n_out
                        ):
                            found = True
                            break
                    if not found:

                        g[start_index + LAYERS[l] + n_out].append(
                            [start_index + n_in, rd.randint(1, MAX_CAPACITY)]
                        )

        start_index = start_index + LAYERS[l]

    return g

# function that prints the graph
def print_graph(g, flow):

    G = nx.DiGraph()
    for i in range(len(g)):
        G.add_node(i)
    for i in range(len(g)):
        for j in range(len(g[i])):
            G.add_edge(i, g[i][j][0], capacity=g[i][j][1], my_flow=flow[i][g[i][j][0]])
    for i in range(len(g)):
        print("from node %02i: " % (i) + str(g[i]))

    pos = []
    [
        pos.append(np.array([1.5 * i, j]))
        for i in range(len(LAYERS))
        for j in range(LAYERS[i])
    ]
    nx.draw(G, pos, with_labels=True)

    colors = [
        "r" if d["my_flow"] == d["capacity"] else "k" for u, v, d in G.edges(data=True)
    ]
    nx.draw_networkx_edges(G, pos, edge_color=colors)
    labels = dict([((u,v,),(str(d["my_flow"]) + "/" + str(d["capacity"])),)
                for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=15, label_pos=0.3)

    colors = ["c" for u in G.nodes()]
    colors[0] = colors[NODES - 1] = "g"
    nx.draw_networkx_nodes(G, pos, node_color=colors)
    plt.show()
