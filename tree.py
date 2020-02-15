import random

class Node:

    def __init__(self, board, parent):
        self.board = board
        self.children = []
        self.parent = parent
        self.visitCount = 0
        self.score = 0
    
    def addChild(self, node):
        self.children.append(node)

    def getRandomChild(self):
        return random.choice(self.children)
    
class Tree:

    def __init__(self):
        self.root = Node(None, None)