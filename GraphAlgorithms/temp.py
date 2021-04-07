from random import shuffle, randrange
import random
import math
MAZE_SIZE = 5
from collections import deque
from icecream import ic
import os
os.chdir("GraphAlgorithms/")
from utils import make_maze, print_maze

def DFS_search(g, start_node, end_node):

    visitedAlready = {}   # Makes a dictionary of all the nodes we've already visited
    visitedAlready[start_node] = True
    pathToNode = [start_node] 

    while len(pathToNode) > 0:  # While the call stack is not empty

        node = pathToNode[-1]   # Take the last element of the stack 

        if node == end_node:    # If the last element of the stack equals the end_node then return the path till now
            return pathToNode

        noFurtherNodes = True   # Assume that the current node has no further unexplored nodes

        for adjacentVertice in g[node]: # For all the adjacent vertices of the current node
            if adjacentVertice not in visitedAlready:   # If the adjacent vertice has not already been visited
                pathToNode.append(adjacentVertice)      # We append the vertice to the stack/path
                visitedAlready[adjacentVertice] = True  # We also mark the new vertice as visited
                noFurtherNodes = False                  # Our initial assumption of no further unexplored nodes is false
                break                                   # Stop searching for unexplored adjacent vertices of current node

        if noFurtherNodes == True:                      # If our assumption holds true, then we remove the top element of the stack
            pathToNode.pop()


def BFS_search(graph, startNode, endNode, *args, **kwargs):

                              # Default value for us to start our BFS
        
        if endNode:      # If the value for an endNode is provided then find the shortest path


            if startNode == endNode:        # Base case
                return [startNode]

            callQueue = deque([startNode])  # Make a queue for FIFO order as compared to stack for DFS
            parentOfCurrentNode = {}        # We create a dictionary to keep track of the parent of each node
            parentOfCurrentNode[startNode] = startNode

            # Create a function to unravel the dictionary to get the shortest path
            def get_previous_path(parentOfCurrentNode, endNode, startNode):
                path = [endNode]
                previousNode = endNode
                
                while previousNode != startNode:    # While the parent node is not the startNode
                    previousNode = parentOfCurrentNode[previousNode]    # Find the parent of the currentNode
                    path.insert(0, previousNode)                        # And insert the parent into the start of the path
                return path # Return the shortest path

            while callQueue:                # While the callQueue is not empty
                
                currentNode = callQueue.popleft()       # Take the first node in the queue

                for adjacentNode in graph[currentNode]: # For all the neighbouring nodes of the currentNode
                    
                    if adjacentNode not in parentOfCurrentNode: # If adjacentNode has not already been seen
                        parentOfCurrentNode[adjacentNode] = currentNode # Note down the parent of the neighbour

                        if adjacentNode == endNode:     # If the adjacentNode is equal to the endNode
                            # We unravel the path to the startNode by iteratively finding the parents of each node in the path to the endNode
                            return get_previous_path(parentOfCurrentNode, adjacentNode, startNode)

                        else: callQueue.append(adjacentNode)    # Else we add the neighbouring node to our queue


s, g = make_maze()
players = [0, MAZE_SIZE * MAZE_SIZE - 1]
print(g)

print("\n\n ******** PERFORMING DFS ********")
path_DFS = DFS_search(g, players[0], players[1])
print_maze(g, path_DFS, players)
print("Path length for DFS is %i" % (len(path_DFS) - 1))

print("\n\n ******** PERFORMING BFS ********")
path_BFS = BFS_search(g, players[0], players[1])
print_maze(g, path_BFS, players)
print("Path length for BFS is %i" % (len(path_BFS) - 1))
