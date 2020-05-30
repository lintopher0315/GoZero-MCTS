import sys
import copy
from game_logic import Board
from MCTS import MCTS

if len(sys.argv) == 1:
    sys.exit()

file = sys.argv[1]
ins = open(file, "r")

for i in ins:
    if i in ['\n', '\r\n']:
        break

board = Board()
ai = MCTS()
next_player = 2

for i in ins:
    if i[0] != ';':
        break
    print(i)
    player = 1
    if i[1] == 'B':
        player = 2
        next_player = 1
    else:
        next_player = 2
    x = i[i.index('[')+1]
    y = i[i.index(']')-1]
    board.grid[ord(y)-97][ord(x)-97] = player

for i in range(19):
    for j in range(19):
        print(board.grid[i][j], end=' ')
    print()

b = ai.find_next_move(copy.deepcopy(board), next_player)
move = ";"
if next_player == 1:
    move += "W["
else:
    move += "B["

print("NEW BOARD\n~~~~~~~~")
for i in range(19):
    for j in range(19):
        if board.grid[i][j] != b.grid[i][j]:
            move += chr(j+97)+chr(i+97)+']'
        print(b.grid[i][j], end=' ')
    print()
print('\n'+move)