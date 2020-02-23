import time
import copy
import random
from tree import Tree
from tree import Node

class MCTS:

    def find_next_move(self, board, player):
        tree = Tree(board, player)
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

            playout = self.simulate(explore_node)
            self.backpropagate(explore_node, playout)

        return root.get_highest_child.board

    def select(self, node):
        selected = node
        while (len(selected.children) > 0):
            selected = selected.get_best_ucb()
        return selected

    def expand(self, node):
        for i in range(19):
            for j in range(19):
                if not node.board.invalid_inter(j, i, node.player):
                    new_board = copy.deepcopy(node.board)
                    new_board.update_board(j, i, node.player)
                    n = Node(new_board, node, 3-node.player)
                    node.add_child(n)
        new_board = copy.deepcopy(node.board)
        new_board.passes += 1
        n = Node(new_board, node, 3-node.player)
        node.add_child(n)

    def simulate(self, node):
        curr_node = node
        while curr_node.board.has_neutral_territory():
            possible_moves = []
            for i in range(19):
                for j in range(19):
                    if not curr_node.board.invalid_inter(j, i, curr_node.player):
                        possible_moves.append([j, i])
            rand_move = random.choice(possible_moves)
            new_board = copy.deepcopy(curr_node.board)
            new_board.update_board(rand_move[0], rand_move[1], curr_node.player)
            curr_node = Node(new_board, curr_node, 3-curr_node.player)
        result = curr_node.board.get_score()
        if result[0] > result[1]:
            return 1
        elif result[1] > result[0]:
            return 2
        else:
            return 3

    def backpropagate(self, node, result):
        temp = node
        while temp != None:
            temp.visit_count += 1
            if temp.player == result:
                temp.score += 10
            temp = temp.parent