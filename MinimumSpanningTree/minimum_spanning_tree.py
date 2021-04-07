import numpy as np
from collections import deque
import sys
sys.path.append('../')
from decorators import execution_time

class MinimumSpanningTrees:
    
    def __init__(self):
        ... 
    @execution_time
    def kruskal(self, graph, *args, **kwargs):
        
        setOfClusters = {str(node):[node] for node in range(len(graph))}    # Each node lies in its own cluster in the beginning
        minimumSpanningTree = []    # The minimum spanning tree is empty in the beginning
        sortedEdges = []

        for i in range(len(graph)): # Create a list of lists containing a list of edgeWeight, (initialVertex, endVertex)
            for j in range(len(graph)):
                sortedEdges.append([graph[i][j], (i, j)])
        
        # Sort the above list by the edge weight
        sortedEdges = sorted(sortedEdges, key = lambda weight: weight[0], reverse=True)

        while len(minimumSpanningTree) < len(graph) - 1:    # While not all the nodes have been added to the MST

            _, indices = sortedEdges.pop()      # Take smallest edge pair
            u, v = min(indices), max(indices)   # and initialise u and v
            isCycle = False                     # We assume there exist no cycles in the beginning

            if setOfClusters[str(u)] != setOfClusters[str(v)]:  # If u and v do not lie in the same cluster
                for index in minimumSpanningTree:
                    if index[0] == u:           # If any of the indices in the MST are equal to u then
                        isCycle = True          # There exists a cycle
                        break

                if isCycle: continue            # If there is a cycle then we don't add that edge and move on

                minimumSpanningTree.append((u, v))  # Otherwise add that edge pair to the MST
                setOfClusters[str(u)] = {*setOfClusters[str(v)].copy(), *setOfClusters[str(u)].copy()}    # Merge the two clusters
        
        return minimumSpanningTree

    @execution_time
    def prim_jarnik(self, graph, startNode = 0, *args, **kwargs):

        cluster = []                # Initialise the cluster as empty
        cluster.append(startNode)   # Add our startNode to our cluster
        minimumSpanningTree = []    # Our MST is empty in the beginning

        while len(cluster) < len(graph) - 1:    # While our cluster does not contain all the elements
            
            # Make a list of lists of all the edge pairs going from inside the cluster to outside the cluster
            edgesGoingFromInsideToOutside = [[insideVertice, outsideVertice, weight] \
                                            for insideVertice in cluster   \
                                            for outsideVertice, weight in enumerate(graph[insideVertice])  \
                                            if outsideVertice not in cluster]
            # Find the smallest edge pair from inside to outside
            smallestEdge = sorted(edgesGoingFromInsideToOutside, key = lambda vertice: vertice[2])
            insideVertice, outsideVertice, weight = smallestEdge[0] # Take the smallest such edge pair
            cluster.append(outsideVertice)                          # Add the outsideVertice to our cluster
            minimumSpanningTree.append((insideVertice, outsideVertice)) # Add the edge pair to our MST

        return minimumSpanningTree
            

