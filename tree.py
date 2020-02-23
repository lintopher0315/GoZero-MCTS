import random
import sys
import math

class Node:

    def __init__(self, board, parent, player):
        self.board = board
        self.children = []
        self.parent = parent
        self.visit_count = 0
        self.score = 0
        self.player = player
    
    def add_child(self, node):
        self.children.append(node)

    def get_random_child(self):
        return random.choice(self.children)

    def get_highest_child(self):
        val = 0
        index = 0
        for i in range(len(self.children)):
            if self.children[i].score > val:
                val = self.children[i].score
                index = i
        return self.children[index]

    def ucb_value(self, parent_visit, win_score, visit):
        if visit == 0:
            return sys.maxsize
        return (win_score/visit)+1.41*math.sqrt(math.log(parent_visit)/visit)

    def get_best_ucb(self):
        max_val = 0
        index = 0
        for i in range(len(self.children)):
            val = self.children[i].ucb_value(self.visit_count, self.children[i].score, self.children[i].visit_count)
            if val > max_val:
                max_val = val
                index = i
        return self.children[index]
    
class Tree:

    def __init__(self, board, player):
        self.root = Node(board, None, player)