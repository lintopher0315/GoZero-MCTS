import time
import copy
import random
import multiprocessing
from multiprocessing.managers import BaseManager
from tree import Tree
from tree import Node

class MCTS:

    def __init__(self):
        self.root = None    # maybe dont need these
        self.lock = multiprocessing.Lock()

    def tree_process(self, t, id):
        timeout = time.time()+20

        while True:
            if time.time() > timeout:
                break

            end_node = self.select(t.root)

            if end_node.board.passes < 2:
                with self.lock:
                    if (len(end_node.children) == 0):
                        #print("expand")
                        self.expand(end_node)
                    #print("length: " + str(len(end_node.children)))

            explore_node = end_node
            if len(explore_node.children) > 0:
                explore_node = end_node.get_random_child()

            playout = self.simulate(explore_node)
            #print("playout: " + str(playout))
            with self.lock:
                self.backpropagate(explore_node, playout)
            print("Process: "+str(id))

    def find_next_move(self, board, player):
        tree = Tree(board, player)
        self.root = tree.root
        self.num_sim = 0

        #q = multiprocessing.Queue()
        #q.put(self.root)

        BaseManager.register('Tree', Tree)
        manager = BaseManager()
        manager.start()
        t = manager.Tree()
        t.root = self.root
        print(self.root)

        processes = []
        for i in range(10):
            p = multiprocessing.Process(target=self.tree_process, args=(t,i,))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()

        self.root = t.root
        return self.root.get_highest_child().board

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

    def simulate(self, node): #instead of adding all possible moves for each step, only add half
        count = 0
        curr_node = node.board
        p = node.player
        #print(curr_node.has_neutral_territory());
        while count < 100 and (curr_node.has_neutral_territory() or len(curr_node.pos_history) < 2):
            possible_moves = []
            for i in range(19):
                for j in range(19):
                    if len(possible_moves)==0 or random.random()>0.5:
                        if not curr_node.invalid_inter(j, i, p):
                            #print(j, i)
                            possible_moves.append([j, i])
            if len(possible_moves) == 0:
                break
            count += 1
            rand_move = random.choice(possible_moves)
            new_board = copy.deepcopy(curr_node)
            new_board.update_board(rand_move[0], rand_move[1], p)
            curr_node = new_board
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
