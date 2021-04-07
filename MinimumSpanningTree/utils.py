import matplotlib.pyplot as plt
import numpy as np
import random
import yaml

with open('config.yaml') as file:
    config = yaml.safe_load(file)
file.close()

# displays a MST
def plot_MST(pts, MST):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    for i in range(len(MST)):
        for j in range(len(MST)):
            if MST[i][j]!= np.infty: ax.plot([pts[i][0],pts[j][0]], [pts[i][1],pts[j][1]], "bo-")
    ax.title.set_text('Minimum Spanning Tree')
    plt.show()

# computes the Euclidean distance between two points p1 and p2
def euclidean_distance(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def make_graph():

    NUMBER_OF_POINTS = config.get('NUMBER_OF_POINTS')
    # generates random points and sort them accoridng to x coordinate
    pts = []
    for i in range(NUMBER_OF_POINTS): pts.append([random.randint(0,1000),random.randint(0,1000)])
    pts = sorted(pts, key=lambda x: x[0])

    make_graph.points = pts

    graph = [[]]*NUMBER_OF_POINTS
    for i in range(NUMBER_OF_POINTS):
        graph[i] = [euclidean_distance(pts[i],pts[j]) for j in range(NUMBER_OF_POINTS)]
    
    return graph