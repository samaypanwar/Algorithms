import random
import numpy as np
import time
import functools



class Sort:

    def _execution_time(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            startTime = time.perf_counter()
            function(*args, **kwargs)
            endTime = time.perf_counter()
            print(f'Execution Time of {function.__name__} : {(endTime-startTime):.3f} seconds')
        return wrapper
    
    @_execution_time
    def insertion_sort(self, array):
        """ The worst-case complexity of such an algorithm is O(n^2)"""

        for key in range(1, len(array)):                    # For each key value
            for previousIndex in range(len(array[:key])):   # Check if the previous elements of the
                                                            # array are smaller than the key value
                if array[key] < array[previousIndex]:       # If not then switch the key with the previous value pair
                    array[key], array[previousIndex] = array[previousIndex], array[key]
                    
        return array

    @_execution_time
    def bubble_sort(self, array):
        """ The worst-case complexity of such an algorithm is O(n^2)"""
        
        for _ in range(len(array)):                         # Have to change the pointer |len(array)| times

            pointer = 0                                     # Start from the first element each time
            sortedLength = 1                                # So that we do not have to iterate through the sorted end of the list
            while pointer < len(array) - sortedLength:
                
                if array[pointer] > array[pointer + 1]:     # If the next element is greater then swap indices
                    array[pointer], array[pointer + 1] = array[pointer + 1], array[pointer]

                pointer += 1                                # Move onto next index
            sortedLength +=1

        return array

    @_execution_time
    def selection_sort(self, array):
        """ The worst-case complexity of such an algorithm is O(n^2)"""

        divider = 0                                         # To keep track of what has already been sorted
                                                            # So that we do not have to run through the end 
        while divider < len(array):                         # While the entire array is not the sorted array

            minimumIndex = divider                          # Start from the index that is yet to be sorted

            for element in range(divider, len(array)):      # Find the minimum element from the remaining elements
                if array[element] < array[minimumIndex]:    
                    minimumIndex = element
            
            array[minimumIndex], array[divider] = array[divider], array[minimumIndex] # Swap indices
            divider += 1                                    # Add one more element to your sorted subarray

        return array

    
    def merge_sort(self, array):
        """ The worst-case complexity of such an algorithm is O(nlog(n))"""

        if len(array) <= 1:  return array           # If the length of the input array is not greater
                                                    # than one then simply return the array

        mid = len(array) // 2                       # Divide the array into two halves and recursively
                                                    # call the algorithms on both halves
        leftArray = array[:mid]
        rightArray = array[mid:]

        sortedLeft, sortedRight = self.merge_sort(leftArray), self.merge_sort(rightArray)
        sortedArray = []                            # Create an empty array to add the sorted elements to

        leftIndex = 0                               # Create two pointers pertaining to both arrays
        rightIndex = 0      
        # While not all of the elements have been added to the sortedArray of both subarrays
        while leftIndex < len(sortedLeft) and rightIndex < len(sortedRight): 
           
            if sortedLeft[leftIndex] < sortedRight[rightIndex]: 
                sortedArray.append(sortedLeft[leftIndex])  
                leftIndex += 1                      # Change the left pointer to the next index
            else:
                sortedArray.append(sortedRight[rightIndex])
                rightIndex += 1                     # Change the right pointer to the next index

        # The cases below arise if we run through one of the subarrays but one is still left

        # While all the elements of left array have not been run through
        while leftIndex < len(sortedLeft):
            sortedArray.append(sortedLeft[leftIndex])
            leftIndex += 1

        # While all the elements of right array have not been run through
        while rightIndex < len(sortedRight):
            sortedArray.append(sortedRight[rightIndex])
            rightIndex += 1

        return sortedArray                  
        
   
    def quick_sort(self, array):
        """ The worst-case complexity of such an algorithm is O(nlog(n))"""
        
        if not array: return array                          # If the array is empty then return it
        
        pivotIndex = random.choice(range(0, len(array)))    # Choose a random pivot value to sort the array
        rightArray = [element for element in array if element > array[pivotIndex]]
        leftArray = [element for element in array if element < array[pivotIndex]]
        # Add the left array to the pivot to the right array after quicksorting both subarrays
        sortedArray = self.quick_sort(leftArray) + [array[pivotIndex]] + self.quick_sort(rightArray)

        return sortedArray

    @_execution_time
    def heap_sort(self, array):
        
        def add_to_heap(heap, element):                     # First we create a min-heap from the array
            """ This function is needed to create a minimum heap from the input array 
            where the children are always bigger than the parent node keys
            """
            heap.append(element)                            # Add the new element to the leftmost point in the tree
            parentIndex = (len(heap) - 2) // 2              # The parent of a child at index n is located at n//2 position
            childIndex = len(heap) - 1

            while heap[parentIndex] > heap[childIndex] and childIndex > 0:                  # While our parent element is bigger than our child element and our child index is positive
                heap[parentIndex], heap[childIndex] = heap[childIndex], heap[parentIndex]   # Since python has negative indexing as well
                childIndex = parentIndex                                                    # We swap the child and the parent and change the childIndex
                parentIndex = (childIndex-1) // 2                                           # Finding the new parent of the child

        def remove_minimum_from_heap(heap):
            """ Since we have a minimum heap, we want to take out the minimum element,
            i.e the root of the tree and then swap the leftmost node with the root """

            if not heap: return None                        # If the heap is empty then there is no minimum element

            minimumElement = heap[0]                        # The root node is the smallest element of the tree
            lastElement = heap.pop()                        # Swap the leftmost element with the root node
            heap[0] = lastElement
            elementIndex = 0

            def smallest_successor(heap, elementIndex):     # To find if the children of a given elementIndex exist and find the smallest one's index
                firstChild, secondChild = heap[2 * elementIndex + 1], heap[2 * elementIndex + 2]
                minimumChildIndex = (2 * elementIndex + 1 if firstChild < secondChild 
                                    else 2 * elementIndex + 2)
                return minimumChildIndex

            try:                                            # Incase one of the children does not exist and a error is thrown
                minimumChildIndex = smallest_successor(heap, elementIndex)
            except: return minimumElement
            
            while heap[elementIndex] > heap[minimumChildIndex]: # While the parent is bigger than its smalled child, swap

                heap[elementIndex], heap[minimumChildIndex] = heap[minimumChildIndex], heap[elementIndex]
                elementIndex = minimumChildIndex
                try:
                    smallest_successor(heap, elementIndex)
                except:
                    break

            return minimumElement

        heap = []                                           # Empty list to create a heap
        sortedArray = []                                    # Empty list to add our minimum elements to
        for element in array:
            add_to_heap(heap, element)                      # Firs create a heap out of the unsorted array
        
        for node in heap:
            minimumElement = remove_minimum_from_heap(heap) # Then iteratively find the minimum element and append it to the sortedArray
            sortedArray.append(minimumElement)

        return sortedArray
