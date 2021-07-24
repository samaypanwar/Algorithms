
import numpy as np
from collections import Counter

class NewNode:
    def __init__(self, key):
        self.key = key
        self.leftChild = None
        self.rightChild = None
        self.height = -1

class Tree(NewNode):

    def binary_search_tree(self, list, *args, **kwargs):
        # Then try to find/delete/add elements to tree

        def search_element_in_bst(self, element, rootNode):

            currentNode = rootNode

            while currentNode is not None:

                if currentNode.key == element:
                    print(f"{element} exists in the tree")
                    return True
                
                elif currentNode.key > element:
                    currentNode = currentNode.leftChild
                
                elif currentNode.key < element:
                    currentNode = currentNode.rightChild
            
            else: raise ValueError(f'{element} does not exist in the BST')

        def add_element_to_bst(self, value, Node):

            if Node is None:
                return NewNode(value)

            elif value < Node.key:
                Node.leftChild = add_element_to_bst(value, Node.leftChild)

            elif value > Node.key:
                Node.rightChild = add_element_to_bst(value, Node.rightChild)

            return Node

        def inorder_traversal(Node):
            if Node is not None:
                inorder_traversal(Node.leftChild)
                print(Node.key)
                inorder_traversal(Node.rightChild)
            
        def remove_element_from_bst(self, value, rootNode):
            
            def _minimum_value_node(Node):

                while Node.leftChild is not None:
                    Node = Node.leftChild

                return Node
            
            if rootNode is None:
                return rootNode
            
            if rootNode.key > value:
                rootNode.leftChild = remove_element_from_bst(value, rootNode.leftChild)

            elif rootNode.key < value:
                rootNode.rightChild = remove_element_from_bst(value, rootNode.rightChild)

            else:
                if rootNode.rightChild is None:
                    temp = rootNode.leftChild
                    rootNode = None
                    return temp
                
                elif rootNode.leftChild is None:
                    temp = rootNode.rightChild
                    rootNode = None
                    return temp
                
                else:
                    temp = _minimum_value_node(rootNode)
                    rootNode.key = temp.key
                    rootNode.rightChild = remove_element_from_bst(temp.key, rootNode.rightChild)
        
    def huffman_encoding(self, string, *args, **kwargs):
        
        frequencyDict = Counter(string)
        sortedIndex = sorted(range(len(frequencyDict)), key = lambda value: list(frequencyDict.values())[value])
        priorityQueue = sorted(list(frequencyDict.items()), key= lambda x: sortedIndex)
        
    def avl(self, *args, **kwargs):
        ...
