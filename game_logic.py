import numpy

class Board:

    grid = numpy.zeros((19, 19))
    black_strings = []
    white_strings = []

    def update_board(self, x, y, player):
        if x >= 0 and x < 19 and y >= 0 and y < 19 and (player == 1 or player == 2):
            self.grid[y][x] = player
            self.update_strings(x, y, player)
    
    def inter_occupied(self, x, y):
        if x >= 0 and x < 19 and y >= 0 and y < 19:
            return self.grid[y][x] != 0
        return True 
    
    def update_strings(self, x, y, player):
        connected = []
        if player == 2:
            for i in range(len(self.black_strings)):
                for j in range(len(self.black_strings[i])):
                    if (self.black_strings[i][j][0] == x and abs(self.black_strings[i][j][1] - y) == 1) or (self.black_strings[i][j][1] == y and abs(self.black_strings[i][j][0] - x) == 1):
                        connected.append(i)
                        break
            connected_string = []
            for i in range(len(connected) - 1, -1, -1):
                connected_string += self.black_strings.pop(connected[i])
            connected_string += [[x, y]]
            self.black_strings.append(connected_string)
        elif player == 1:
            for i in range(len(self.white_strings)):
                for j in range(len(self.white_strings[i])):
                    if (self.white_strings[i][j][0] == x and abs(self.white_strings[i][j][1] - y) == 1) or (self.white_strings[i][j][1] == y and abs(self.white_strings[i][j][0] - x) == 1):
                        connected.append(i)
                        break
            connected_string = []
            for i in range(len(connected) - 1, -1, -1):
                connected_string += self.white_strings.pop(connected[i])
            connected_string += [[x, y]]
            self.white_strings.append(connected_string)

    def is_string_captured(self, index, player):
        stack = []
        visited = []
        string_copy = None
        if player == 2:
            string_copy = self.black_strings[index].copy()
        else:
            string_copy = self.white_strings[index].copy()
        stack.append(string_copy[0])
        while len(stack) > 0:
            rem = stack.pop()
            visited.append(rem)
            if rem[0]+1<19 and [rem[0]+1, rem[1]] not in visited:
                if self.grid[rem[1]][rem[0]+1] == 0:
                    return False
                elif self.grid[rem[1]][rem[0]+1] == player:
                    stack.append([rem[0]+1, rem[1]])
            if rem[1]+1<19 and [rem[0], rem[1]+1] not in visited:
                if self.grid[rem[1]+1][rem[0]] == 0:
                    return False
                elif self.grid[rem[1]+1][rem[0]] == player:
                    stack.append([rem[0], rem[1]+1])
            if rem[0]-1>=0 and [rem[0]-1, rem[1]] not in visited:
                if self.grid[rem[1]][rem[0]-1] == 0:
                    return False
                elif self.grid[rem[1]][rem[0]-1] == player:
                    stack.append([rem[0]-1, rem[1]])
            if rem[1]-1>=0 and [rem[0], rem[1]-1] not in visited:
                if self.grid[rem[1]-1][rem[0]] == 0:
                    return False
                elif self.grid[rem[1]-1][rem[0]] == player:
                    stack.append([rem[0], rem[1]-1])
        return True