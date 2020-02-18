import time
import copy
from tree import Tree
from tree import Node

class MCTS:

    def find_next_move(self, board):
        tree = Tree(board)
        root = tree.root

        timeout = time.time()+10
        while True:
            if time.time() > timeout:
                break

            end_node = self.select(root)

            if end_node.board.passes < 2:
                self.expand(end_node)

            explore_node = end_node
            if len(explore_node.children) > 0:
                explore_node = end_node.get_random_child()

            #simulate

            #backpropagate

        return 0

    def select(self, node):
        selected = node
        while (len(selected.children) > 0):
            selected = selected.get_best_ucb()
        return selected

    def expand(self, node):
        for i in range(19):
            for j in range(19):
                if not node.board.invalid_inter(j, i, 1):
                    new_board = copy.deepcopy(node.board)
                    new_board.update_board(j, i, 1)
                    n = Node(new_board, node)
                    node.add_child(n)
        new_board = copy.deepcopy(node.board)
        new_board.passes += 1
        n = Node(new_board, node)
        node.add_child(n)

    def simulate(self):
        return 0

    def backpropagate(self):
        return 0