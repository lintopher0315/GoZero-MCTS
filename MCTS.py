import time
import copy
import random
import time
from queue import Empty
from tree import Tree
from tree import Node

class MCTS:

    def find_next_move(self, board, player):
        tree = Tree(board, player)
        root = tree.root
        num_sim = 0

        timeout = time.time()+20

        while True:
            if time.time() > timeout:
                break

            end_node = self.select(root)

            if end_node.board.passes < 2:
                if (len(end_node.children) == 0):
                    #print("expand")
                    self.expand(end_node)
                #print("length: " + str(len(end_node.children)))

            explore_node = end_node
            if len(explore_node.children) > 0:
                explore_node = end_node.get_random_child()

            playout = self.simulate(explore_node)
            #print("playout: " + str(playout))
            self.backpropagate(explore_node, playout)
            num_sim += 1

        print("Simulations: "+str(num_sim))
        return root.get_highest_child().board

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

    def pre_result(self, score):
        if score[0] > score[1]+3:
            return 1
        elif score[1] > score[0]+3:
            return 2
        else:
            return 3

    def simulate(self, node):
        count = 0
        curr_node = copy.deepcopy(node.board)
        p = node.player

        result = self.pre_result(curr_node.get_score())
        if result != 3:
            return result

        while count < 100 and (curr_node.has_neutral_territory() or len(curr_node.pos_history) < 2):
            if count%20 == 0:
                result = self.pre_result(curr_node.get_score())
                if result != 3:
                    return result

            possible_moves = []
            
            for i in range(19):
                for j in range(19):
                    if len(possible_moves)==0 or random.random()>0.75:
                        if not curr_node.invalid_inter(j, i, p):
                            possible_moves.append([j, i])

            if len(possible_moves) == 0:
                break
            count += 1
            rand_move = random.choice(possible_moves)
            curr_node.update_board(rand_move[0], rand_move[1], p)
            p = 3-p
            #curr_node = Node(new_board, curr_node, 3-curr_node.player)
        result = curr_node.get_score()
        #print("count: " + str(count) + " playout: " + str(result))
        if result[0] > result[1]:
            return 1
        elif result[1] > result[0]:
            return 2
        else:
            return 3

    def backpropagate(self, node, result):
        temp = node
        while temp != None:
            #print("back player: " + str(temp.player))
            temp.visit_count += 1
            if 3-temp.player == result:
                temp.score += 10
            temp = temp.parent
