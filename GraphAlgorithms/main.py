import os
os.chdir("GraphAlgorithms/")

from graphs import GraphAlgorithms
from utils import make_graph, make_maze, print_graph, print_maze, MAZE_SIZE

if __name__ == '__main__':
    
    maze = make_maze()
    graph = make_graph()
    
    algorithms = GraphAlgorithms()

    mazeAlgorithms = ['DFS', 'BFS']
    
    graphAlgorithms = [algo for algo in dir(algorithms) if not algo.startswith("_")]

    graphAlgorithms.remove('INFINITY')

    for algo in graphAlgorithms:

        if algo in mazeAlgorithms:
            players = [0, MAZE_SIZE * MAZE_SIZE - 1]
            shortestPath = eval("algorithms." + algo + "(maze, players[0], players[1])")
            print_maze(maze, shortestPath, players)
            
        else:
            shortestPath = eval("algorithms." + algo + "(graph)")
