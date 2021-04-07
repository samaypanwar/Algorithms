import os
os.chdir("SortingAlgorithms/")

from sorting import Sort
import numpy as np
import yaml

if __name__ == "__main__":

    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    file.close()
    
    try:
        MAX_SIZE = config.get("MAX_SIZE")
    except: raise ValueError('Max size of random array not defined')

    sort = Sort()
    randomArray = list(np.random.randint(100000, size=MAX_SIZE))
    sortingAlgorithms = [algo for algo in dir(Sort) if not algo.startswith("_")]

    for algo in sortingAlgorithms:
        eval("sort." + algo + "(randomArray)")
