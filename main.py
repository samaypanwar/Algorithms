from sorting import Sort
import numpy as np

if __name__ == "__main__":

    MAX_SIZE = 100
    sort = Sort()
    randomArray = list(np.random.randint(100000, size=MAX_SIZE))
    sortingAlgorithms = [algo for algo in dir(Sort) if not algo.startswith("_")]

    for algo in sortingAlgorithms:
        eval("sort." + algo + "(randomArray)")
