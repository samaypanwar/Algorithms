import os
os.chdir("NetworkFlow/")

from network_flow import NetworkFlow
from utils import make_graph, print_graph
import matplotlib.pyplot as plt


if __name__ == "__main__":

    graph = make_graph()
    NetworkFlow = NetworkFlow()
    maximumFlow = NetworkFlow.edmonds_karp(graph)
    
    plt.figure(1, figsize=(30, 30))
    # print_graph(graph, maximumFlow)
    # plt.show()

