import os
os.chdir("MinimumSpanningTree/")
from minimum_spanning_tree import MinimumSpanningTrees
from utils import make_graph, plot_MST
import matplotlib.pyplot as plt

if __name__ == '__main__':

    MST = MinimumSpanningTrees()
    graph = make_graph()
    minimumSpanningTreeAlgorithms = [algo for algo in dir(MST) if not algo.startswith("_")]

    for algo in minimumSpanningTreeAlgorithms:

        mstGraph = eval("MST." + algo + "(graph)")
        # plot_MST(make_graph.points, mstGraph)

        