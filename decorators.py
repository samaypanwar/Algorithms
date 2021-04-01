import time 
import functools

def execution_time(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        startTime = time.perf_counter()
        output = function(*args, **kwargs)
        endTime = time.perf_counter()
        print("\n-------------------------------------------------")
        print(f'Execution Time of {function.__name__} : {(endTime-startTime):.3f} seconds')
        print("-------------------------------------------------\n")
        return output
    return wrapper