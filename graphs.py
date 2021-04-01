import numpy as np
from collections import deque
from decorator import execution_time

class GraphAlgorithms:

    def __init__(self):
        self.INFINITY = np.inf

    @execution_time
    def DFS(self, graph, startNode, endNode = None, *args, **kwargs):
        """ Assumes that adjaceny list has weights but does not consdier
         them in computing the path
        """

        visitedAlready = {}                 # To keep track of the vertices we have already seen
        visitedAlready[startNode] = True    # Mark the startNode as already seen
        pathToNode = [startNode]            # Add the startNode to our callStack and path
        callStack = pathToNode.copy()

        if endNode is not None:             # If we want to find the shortest path to a specific node
            while pathToNode:               # While the call stack is not empty

                node = pathToNode[-1]       # Take the last element of our call stack
                if node == endNode:         # Check if this node is equal to the node we are looking for
                    return pathToNode
                
                noFurtherNodes = True       # Assume that node does not have any further nodes

                for adjacentVertice, weight in graph[node]:         # Check all the adjacent vertices of our node
                    if adjacentVertice not in visitedAlready:   # If any of them are not in our cloud
                        pathToNode.append(adjacentVertice)      # Append them to our path 
                        visitedAlready[adjacentVertice] = True  # And mark them as seen
                        noFurtherNodes = False                  # Our assumption of no further nodes was false
                        break
                if noFurtherNodes:          # If our assumption still holds true, it means all adjacent vertices have been seen
                    pathToNode.pop()        # So move on to next element of call stack

        else:                               # Incase the endNode is not give, we want to perform a traversal to find all connected nodes
            while callStack:                # While call stack is not empty
                node = callStack[-1]        # Take last element of call stack
                noFurtherNodes = True       # Assume no further nodes

                for adjacentVertice, weight in graph[node]:     # For all adjacent nodes of the current node
                    if adjacentVertice not in visitedAlready:   # If any of them have not been seen already
                        callStack.append(adjacentVertice)       # Add them to call stack and our path
                        pathToNode.append(adjacentVertice)
                        visitedAlready[adjacentVertice] = True  # And mark them as seen
                        noFurtherNodes = False                  # Our assumption was false
                        break
                if noFurtherNodes:          # If our assumption holds true then we have explored all neighours of current node
                    callStack.pop()         # Move onto next element of call stack
            else:
                for node in pathToNode: 
                    print(node, end=" ")
                return pathToNode           # Return all the nodes
    
    @execution_time
    def BFS(self, graph, startNode, *args, **kwargs):
        """ Performs BFS but cannot make maze for some reason """
        
        visitedAlready = {}                 # Keep track of all the nodes already seen
        visitedAlready[startNode] = True    # Mark the startNode as already seen
        callQueue = deque()                 # We use a queue for BFS as compared to a stack for DFS
        callQueue.append(startNode)         # Add the startNode to our queue
        
        while callQueue:                    # While our queue is not empty

            node = callQueue.popleft()      # Take the first element in our queue
            print(node, end=" ")            # And print it

            for adjacentVertice in graph[node]:             # For each neighbour of our node
                if adjacentVertice not in visitedAlready:   # If our node has not already been visited
                    callQueue.append(adjacentVertice)       # Add it to our queue 
                    visitedAlready[adjacentVertice] = True  # And mark it as already visited

    @execution_time
    def dijkstra(self, graph, startNode, *args, **kwargs):
               
        distanceToNodes = [self.INFINITY]*len(graph)    # Initally all nodes are at a distance infinity from the startNode
        distanceToNodes[startNode] = 0                  # Start Node is at a distance of 0 from itself
        visitedAlready = {}                     # Dictionary to keep track of the vertices in the cloud
        visitedAlready[startNode] = True        # Mark the start node as already in the cloud

        if not graph[startNode]:                # Edge case incase there are no neighbouring vertices of startNode
            return distanceToNodes

        for vertice, edge in graph[startNode]:  # To take the initial values of all the vertices connected to the start_node
            distanceToNodes[vertice] = edge

        for _ in enumerate(graph):

            # Taking the closest vertices with respect to their distance from the startNode
            adjacentVertices = sorted(list(range(len(graph))), key = lambda vertice: distanceToNodes[vertice])  
            for vertice in adjacentVertices:
                if vertice not in visitedAlready and graph[vertice]:    # If ther vertice has not already been seen and has neighbours
                    closestVertice = vertice                            # We shall take that vertice as our closestVertice
                    break

            visitedAlready[closestVertice] = True                       # Mark the closestVertice as already visited

            for vertice, weight in graph[closestVertice]:               # Find all the vertices that the closestVertice is connected to
                if vertice not in visitedAlready:                       # If any of the vertices is not already in the cloud
                    if distanceToNodes[closestVertice] + weight < distanceToNodes[vertice]: # And if a shorter path to that vertice exists
                        distanceToNodes[vertice] = distanceToNodes[closestVertice] + weight # Change the distance to that vertice  

        return distanceToNodes

    @execution_time
    def floyd_warshall(self, graph, startNode, returnPath, *args, **kwargs):
        """ O(n^3) algorithm, If user wants the shortest distance between two nodes, 
        they must supply the two nodes in returnPath as a tuple (initialNode, endNode)
        """
        distanceToNodes = np.full(shape=(len(graph), len(graph)), fill_value=self.INFINITY) # Mark the distance to all nodes as infinity
        shortestPath = np.full(shape=(len(graph), len(graph)), fill_value=None)             # To tkae note of the path to each node
        
        for vertice, weight in graph[startNode]:            # For each vertice that our startNode is connected to
            distanceToNodes[startNode][vertice] = weight    # Update the distance table with the initial distances
            shortestPath[startNode][vertice] = vertice      # And take note of the path
        
        for identicalVertice in range(len(graph)):          # The diagonal elements of the distance table are 0
            distanceToNodes[identicalVertice][identicalVertice] = 0
            shortestPath[identicalVertice][identicalVertice] = identicalVertice

        for k in range(len(distanceToNodes)):               # For each initial vertex
            for j in range(len(distanceToNodes)):           # For each final vertex
                for i in range(len(distanceToNodes)):       # For each intermediate vertex
                    
                    intermediateDistance = distanceToNodes[i][k] + distanceToNodes[k][j]
                    initialDistance = distanceToNodes[i][j]
                    # If the distance through the intermediate vertex is less than the current distance to the final node
                    if intermediateDistance < initialDistance:
                        distanceToNodes[i][j] = intermediateDistance    # Update the distance table

        if returnPath:      # If the user wants the shortest path to a specific set of vertices
            initialNode, endNode = returnPath   

            if shortestPath[initialNode][endNode] == None:  # If there is no intermediate path between the two vertices
                print(f'Error! No path exists between the two nodes: {returnPath}')
                return []                                   # Return nothing

            pathToNode = [initialNode]      # Else take note of the path

            while initialNode != endNode:   

                initialNode = shortestPath[initialNode][endNode]
                pathToNode.append(initialNode)

            return pathToNode               # Return the path to the node
            
        return distanceToNodes
    
    @execution_time
    def bellman_ford(self, graph, startNode, *args, **kwargs):
        
        distanceToNode = [self.INFINITY] * len(graph)       # Mark the current distance to each node as infinity
        predecessor = [None] * len(graph)                   # To keep track of the path
        distanceToNode[startNode] = 0                       # Initial node is at a distance of zero from itself
        allEdges = [[initialNode, endNode, weight] for initialNode in range(len(graph)) \
                    for endNode, weight in graph[initialNode]]  # Find all the edges in the graph

        for _ in range(len(graph)):

            for node, intermediateNode, weight in allEdges:                         # For each edge
                # If the distance is smaller through an intermediate node
                if distanceToNode[intermediateNode] > distanceToNode[node] + weight:
                    # Then update the distance table accordingly
                    distanceToNode[intermediateNode] = distanceToNode[node] + weight
                    predecessor[intermediateNode] = node
        
        for node, intermediateNode, weight in allEdges:     # Incase improvements can still be made in the distance table
            if distanceToNode[intermediateNode] > distanceToNode[node] + weight:
                    # Such a case cannot exist and proves the existence of a negative cycle in the loop
                    raise ValueError("There exists a negative cycle in the loop")
        
        return distanceToNode
