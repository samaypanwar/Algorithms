
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
        
        visitedAlready = {}
        visitedAlready[startNode] = True
        callQueue = deque()
        callQueue.append(startNode)
        
        while callQueue:

            node = callQueue.popleft()
            print(node, end=" ")

            for adjacentVertice in graph[node]:
                if adjacentVertice not in visitedAlready:
                    callQueue.append(adjacentVertice)
                    visitedAlready[adjacentVertice] = True

    @execution_time
    def dijkstra(self, graph, startNode, *args, **kwargs):

                   
        distanceToNodes = [self.INFINITY]*len(graph) # Initally all nodes are at a distance infinity from the startNode
        distanceToNodes[startNode] = 0          # Start Node is at a distance of 0 from itself
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
        distanceToNodes = np.full(shape=(len(graph), len(graph)), fill_value=self.INFINITY)
        shortestPath = np.full(shape=(len(graph), len(graph)), fill_value=None)
        
        for vertice, weight in graph[startNode]:
            distanceToNodes[startNode][vertice] = weight
            shortestPath[startNode][vertice] = vertice
        
        for identicalVertice in range(len(graph)):
            distanceToNodes[identicalVertice][identicalVertice] = 0
            shortestPath[identicalVertice][identicalVertice] = identicalVertice

        for k in range(len(distanceToNodes)):
            for j in range(len(distanceToNodes)):
                for i in range(len(distanceToNodes)):

                    intermediateDistance = distanceToNodes[i][k] + distanceToNodes[k][j]
                    initialDistance = distanceToNodes[i][j]

                    if intermediateDistance < initialDistance:
                        distanceToNodes[i][j] = intermediateDistance

        if returnPath:
            initialNode, endNode = returnPath

            if shortestPath[initialNode][endNode] == None:
                print(f'Error! No path exists between the two nodes: {returnPath}')
                return []

            pathToNode = [initialNode]

            while initialNode != endNode:

                initialNode = shortestPath[initialNode][endNode]
                pathToNode.append(initialNode)

            return pathToNode
            
        return distanceToNodes
    
    @execution_time
    def bellman_ford(self, graph, startNode, *args, **kwargs):
        
        distanceToNode = [self.INFINITY] * len(graph)
        predecessor = [None] * len(graph)
        distanceToNode[startNode] = 0
        allEdges = [[initialNode, endNode, weight] for initialNode in range(len(graph)) \
                    for endNode, weight in graph[initialNode]]

        for _ in range(len(graph)):

            for node, intermediateNode, weight in allEdges:
                if distanceToNode[intermediateNode] > distanceToNode[node] + weight:
                    distanceToNode[intermediateNode] = distanceToNode[node] + weight
                    predecessor[intermediateNode] = node
        
        for node, intermediateNode, weight in allEdges: 
            if distanceToNode[intermediateNode] > distanceToNode[node] + weight:
                    raise ValueError("There exists a negative cycle in the loop")
        
        return distanceToNode

class MinimumSpanningTrees:
    
    def __init__(self):
        ... 
    @execution_time
    def kruskal(self, graph, *args, **kwargs):
        
        setOfClusters = {str(node):[node] for node in range(len(graph))}
        minimumSpanningTree = []
        sortedEdges = []

        for i in range(len(graph)):
            for j in range(len(graph)):
                sortedEdges.append([graph[i][j], (i, j)])
        
        sortedEdges = sorted(sortedEdges, key = lambda weight: weight[0], reverse=True)

        while len(minimumSpanningTree) < len(graph) - 1:

            _, indices = sortedEdges.pop()
            u, v = min(indices), max(indices)
            isCycle = False

            if setOfClusters[str(u)] != setOfClusters[str(v)]:
                for index in minimumSpanningTree:
                    if index[0] == u:
                        isCycle = True
                        break

                if isCycle: continue

                minimumSpanningTree.append((u, v))
                setOfClusters[str(u)] = {*setOfClusters[str(v)].copy(), *setOfClusters[str(u)].copy()}    # Merge the two clusters
        
        return minimumSpanningTree

    @execution_time
    def prim_jarnik(self, graph, startNode = 0, *args, **kwargs):

        cluster = []
        cluster.append(startNode)
        minimumSpanningTree = []

        while len(cluster) < len(graph) - 1:

            edgesGoingFromInsideToOutside = [[insideVertice, outsideVertice, weight] \
                                            for insideVertice in cluster   \
                                            for outsideVertice, weight in enumerate(graph[insideVertice])  \
                                            if outsideVertice not in cluster]

            smallestEdge = sorted(edgesGoingFromInsideToOutside, key = lambda vertice: vertice[2])
            insideVertice, outsideVertice, weight = smallestEdge[0]
            cluster.append(outsideVertice)
            minimumSpanningTree.append((insideVertice, outsideVertice))

        return minimumSpanningTree
            

