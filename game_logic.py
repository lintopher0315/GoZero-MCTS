import numpy

class Board:

    grid = numpy.zeros((19, 19))

    def update_board(self, x, y, player):
        if x >= 0 and x < 19 and y >= 0 and y < 19 and (player == 1 or player == 2):
            self.grid[y][x] = player
    
    def inter_occupied(self, x, y):
        if x >= 0 and x < 19 and y >= 0 and y < 19:
            return self.grid[y][x] != 0
        return True 