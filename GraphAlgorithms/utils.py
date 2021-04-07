from random import shuffle, randrange, randint
import random
import math
import yaml
import networkx as nx
import matplotlib.pyplot as plt

with open('config.yaml') as file:
    config = yaml.safe_load(file)
file.close()


MAZE_SIZE = config['MAZE'].get("MAZE_SIZE")
NODES = config['SHORTEST_PATH'].get("NODES")               # defines number of nodes in the graph
EDGES = config['SHORTEST_PATH'].get("EDGES")              # defines number of edges in the graph
DIRECTED = config['SHORTEST_PATH'].get("DIRECTED")         # defines if the graph is directed or undirected
NEGATIVE_WEIGHT = config['SHORTEST_PATH'].get("NEGATIVE_WEIGHT") # defines if the edges can have negative weight
INFINITY = math.inf                                     # defines a variable for infinity


def make_maze():

    vis = [[0] * MAZE_SIZE + [1] for _ in range(MAZE_SIZE)] + [[1] * (MAZE_SIZE + 1)]
    ver = [["|:"] * MAZE_SIZE + ["|"] for _ in range(MAZE_SIZE)] + [[]]
    hor = [["+-"] * MAZE_SIZE + ["+"] for _ in range(MAZE_SIZE + 1)]
    
    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
            if yy == y:
                ver[y][max(x, xx)] = " :"
            walk(xx, yy)
    
    walk(randrange(MAZE_SIZE), randrange(MAZE_SIZE))

    s = ""
    for (a, b) in zip(hor, ver):
        s += "".join(a + ["\n"] + b + ["\n"])

    s_temp = s
    graph = [[] for i in range(MAZE_SIZE * MAZE_SIZE)]
    for col in range(MAZE_SIZE):
        for row in range(MAZE_SIZE):
            if s_temp[(2 * row + 1) * (2 * MAZE_SIZE + 2) + (2 * col)] == " " or (
                random.random() < 1 / (2 * MAZE_SIZE) and col != 0
            ):
                graph[col + MAZE_SIZE * row].append(col - 1 + MAZE_SIZE * row)
                graph[col - 1 + MAZE_SIZE * row].append(col + MAZE_SIZE * row)

            if s_temp[(2 * row + 2) * (2 * MAZE_SIZE + 2) + (2 * col) + 1] == " " or (
                random.random() < 1 / (2 * MAZE_SIZE) and row != MAZE_SIZE - 1
            ):
                graph[col + MAZE_SIZE * row].append(col + MAZE_SIZE * (row + 1))
                graph[col + MAZE_SIZE * (row + 1)].append(col + MAZE_SIZE * row)

    return graph

def print_maze(g, path, players):

    s = ""
    for col in range(MAZE_SIZE):
        s += "+---"
    s += "+\n"

    for row in range(MAZE_SIZE):
        s += "|"
        for col in range(MAZE_SIZE):
            if row * MAZE_SIZE + col == players[0]:
                s += "👨 "
            elif row * MAZE_SIZE + col == players[1]:
                s += "🙋‍♀️ "
            elif row * MAZE_SIZE + col in path:
                ind = path.index(row * MAZE_SIZE + col)
                if path[ind + 1] == row * MAZE_SIZE + col + 1:
                    s += " → "
                elif path[ind + 1] == row * MAZE_SIZE + col - 1:
                    s += " ← "
                elif path[ind + 1] == row * MAZE_SIZE + col + MAZE_SIZE:
                    s += " ↓ "
                elif path[ind + 1] == row * MAZE_SIZE + col - MAZE_SIZE:
                    s += " ↑ "
                else:
                    s += "ppp"
            else:
                s += "   "
            if (row * MAZE_SIZE + col + 1) in g[row * MAZE_SIZE + col]:
                s += " "
            else:
                s += "|"

        s += "\n+"
        for col in range(MAZE_SIZE):
            if ((row + 1) * MAZE_SIZE + col) in g[row * MAZE_SIZE + col]:
                s += "   +"
            else:
                s += "---+"
        s += "\n"

    print(s)

def make_graph():
    if NODES*NODES<EDGES: 
        print("Impossible to generate a simple graph with %i nodes and %i edges!\n" %(NODES,EDGES))
        return None
    g = [[] for i in range(NODES)]
    for i in range(EDGES):
        while True:
            start_node = randint(0,NODES-1)
            end_node = randint(0,NODES-1)
            if NEGATIVE_WEIGHT: weight = randint(-20,20)
            else: weight = randint(1,20)
            if (start_node != end_node): 
                found = False
                for j in range(len(g[start_node])): 
                    if g[start_node][j][0] == end_node: found = True
                if not found: break            
        g[start_node].append([end_node, weight])
        if DIRECTED==False: g[end_node].append([start_node, weight])
    return g
 
# function that prints the graph
def print_graph(g):
    if DIRECTED: G = nx.DiGraph()
    else: G = nx.Graph()
    for i in range(len(g)): G.add_node(i)
    for i in range(len(g)):
        for j in range(len(g[i])): G.add_edge(i,g[i][j][0],weight=g[i][j][1])
    for i in range(len(g)):
        print("from node %02i: " %(i),end="")
        print(g[i])
    try: 
        pos = nx.planar_layout(G)
        nx.draw(G,pos, with_labels=True)
    except nx.NetworkXException:
        print("\nGraph is not planar, using alternative representation")
        pos = nx.spring_layout(G)
        nx.draw(G,pos, with_labels=True)
    if DIRECTED: 
        labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, label_pos=0.3)
    else:
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
