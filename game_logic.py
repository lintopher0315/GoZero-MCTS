import numpy

class Board:

    grid = numpy.zeros((19, 19))
    black_strings = []
    white_strings = []

    def update_board(self, x, y, player):
        if x >= 0 and x < 19 and y >= 0 and y < 19 and (player == 1 or player == 2):
            self.grid[y][x] = player
            
            if player == 2:
                self.black_strings = self.update_strings(x, y, player)

                for i in range(len(self.white_strings)-1, -1, -1):
                    if self.is_string_captured(self.white_strings[i], 3-player):
                        self.remove_string(i, 3-player)
            else:
                self.white_strings = self.update_strings(x, y, player)

                for i in range(len(self.black_strings)-1, -1, -1):
                    if self.is_string_captured(self.black_strings[i], 3-player):
                        self.remove_string(i, 3-player)
    
    def invalid_inter(self, x, y, player):
        if x >= 0 and x < 19 and y >= 0 and y < 19:
            return self.grid[y][x] != 0 or self.is_self_capture(x, y, player)
        return True 
    
    def update_strings(self, x, y, player):
        connected = []
        if player == 2:
            black_copy = self.black_strings.copy()
            for i in range(len(self.black_strings)):
                for j in range(len(self.black_strings[i])):
                    if (self.black_strings[i][j][0] == x and abs(self.black_strings[i][j][1] - y) == 1) or (self.black_strings[i][j][1] == y and abs(self.black_strings[i][j][0] - x) == 1):
                        connected.append(i)
                        break
            connected_string = []
            for i in range(len(connected)-1, -1, -1):
                connected_string += black_copy.pop(connected[i])
            connected_string += [[x, y]]
            black_copy.append(connected_string)
            return black_copy
        else:
            white_copy = self.white_strings.copy()
            for i in range(len(self.white_strings)):
                for j in range(len(self.white_strings[i])):
                    if (self.white_strings[i][j][0] == x and abs(self.white_strings[i][j][1] - y) == 1) or (self.white_strings[i][j][1] == y and abs(self.white_strings[i][j][0] - x) == 1):
                        connected.append(i)
                        break
            connected_string = []
            for i in range(len(connected)-1, -1, -1):
                connected_string += white_copy.pop(connected[i])
            connected_string += [[x, y]]
            white_copy.append(connected_string)
            return white_copy

    def is_string_captured(self, string, player):
        stack = []
        visited = []
        stack.append(string[0].copy())
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

    def remove_string(self, index, player):
        coords = None
        if player == 2:
            coords = self.black_strings.pop(index)
        else:
            coords = self.white_strings.pop(index)
        for coord in coords:
            self.grid[coord[1]][coord[0]] = 0

    def is_self_capture(self, x, y, player):
        self.grid[y][x] = player
        if player == 2:
            black_copy = self.update_strings(x, y, player)
            for i in range(len(self.white_strings)-1, -1, -1):
                if self.is_string_captured(self.white_strings[i], 3-player):
                    self.grid[y][x] = 0
                    return False
            for i in range(len(black_copy)-1, -1, -1):
                if self.is_string_captured(black_copy[i], player):
                    self.grid[y][x] = 0
                    return True
        else:
            white_copy = self.update_strings(x, y, player)
            for i in range(len(self.black_strings)-1, -1, -1):
                if self.is_string_captured(self.black_strings[i], 3-player):
                    self.grid[y][x] = 0
                    return False
            for i in range(len(white_copy)-1, -1, -1):
                if self.is_string_captured(white_copy[i], player):
                    self.grid[y][x] = 0
                    return True
        self.grid[y][x] = 0
        return False