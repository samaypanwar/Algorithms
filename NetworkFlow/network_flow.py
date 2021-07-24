import numpy as np
from collections import deque
import sys
sys.path.append('../')
from decorators import execution_time

class NetworkFlow:

    def BFS_search(self, graph, *args, **kwargs):
        """ Our BFS algorithm takes in an adjacency matrix and computes the shortest path from source to sink. """

        # Create a function to unravel the dictionary to get the shortest path
        def get_previous_path(parentOfCurrentNode, sinkNode, sourceNode):
            path = []
            previousNode = sinkNode
            while previousNode != sourceNode:  # While the parent node is not the sourceNode
                currentNode = previousNode
                previousNode, residualEdgeCapacity = parentOfCurrentNode[currentNode]  # Find the parent of the currentNode
                path.insert(0, [previousNode, currentNode, residualEdgeCapacity])      # And insert the parent into the start of the path

            return path  # Return the shortest path

        sourceNode = 0
        sinkNode = len(graph) - 1

        if sourceNode == sinkNode:  # Base case
            return [sourceNode]

        callQueue = deque([sourceNode])  # Make a queue for FIFO order as compared to stack for DFS
        parentOfCurrentNode = {}         # We create a dictionary to keep track of the parent of each node
        parentOfCurrentNode[sourceNode] = [sourceNode, 0]


        while callQueue:  # While the callQueue is not empty

            currentNode = callQueue.popleft()  # Take the first node in the queue

            for adjacentNode, residualEdgeCapacity in enumerate(graph[currentNode]):
                # For all the neighbouring nodes of the currentNode
                if (adjacentNode not in parentOfCurrentNode) and residualEdgeCapacity != 0 :  # If adjacentNode has not already been seen
                    parentOfCurrentNode[adjacentNode] = [currentNode, residualEdgeCapacity]   # Note down the parent of the neighbour

                    if (adjacentNode == sinkNode):  # If the adjacentNode is equal to the sinkNode
                        # We unravel the path to the sourceNode by iteratively finding the parents of each node in the path to the sinkNode
                        return get_previous_path(parentOfCurrentNode, adjacentNode, sourceNode)

                    else:
                        callQueue.append(adjacentNode)  # Else we add the neighbouring node to our queue

    # function that returns the residual graph from the input graph
    def build_residual_graph(self, graph, flow, *args, **kwargs):

        # First we want to change our graph structure to an adjacency matrix for easier subtracting
        adjacencyMatrixForCapacities = np.zeros(shape=(len(graph), len(graph)))
        for i in range(len(graph)):
            for j, weight in graph[i]:
                adjacencyMatrixForCapacities[i][j] = weight

        # Create the residual graph by subtracting the flow from all the capacities
        residualGraphAsAdjacencyMatrix = np.subtract(adjacencyMatrixForCapacities, flow)

        return residualGraphAsAdjacencyMatrix

    # function that implements the Edmonds Karp algorithm to find max-flow of a network graph
    @execution_time
    def edmonds_karp(self, graph, *args, **kwargs):

        flow = [[0 for i in enumerate(graph)] for j in enumerate(graph)]    # Initially nothing flows through the graph

        while True:

            residualGraph = self.build_residual_graph(graph, flow)   # Build a residual graph
            augmentedPath = self.BFS_search(residualGraph)           # Find the shortest path from the source to the sink using BFS

            if augmentedPath == None:       # If no such path exists then the maximum flow has been reached and we return the flow
                return flow

            # Find residual capacity for this path and add it to the flow of all its edges
            # The residual capacity is just the minimum weight in all the paths of the bfs returned augmented path
            augmentedCapacity = min(augmentedPath, key=lambda edge: edge[2])[2]

            for firstNode, secondNode, edge in augmentedPath:   # For each pair of edge nodes
                # When we add and subtract, it ensures that the total net flow remains zero
                flow[firstNode][secondNode] += augmentedCapacity    # Add the augmentedCapacity to all forward edges
                flow[secondNode][firstNode] -= augmentedCapacity    # Subtract the augmentedCapcacity from all backward edges

