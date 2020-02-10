import remi.gui as gui
from remi import start, App
from game_logic import Board

class BetaGo(App):

    board = Board()
    player = 2
    images = []

    def __init__(self, *args):
        super(BetaGo, self).__init__(*args, static_file_path = {'my_res':'./res/'})

    def main(self):
        screen = gui.Container(width=500, height=700)
        container = gui.Container(width=441, height=441)
        container.style['background-image'] = "url('/my_res:board.png')"
        for i in range(19):
            for j in range(19):
                self.piece = gui.Container(width=22, height=22)
                self.piece.style['background-image'] = "none"
                self.piece.style['background-repeat'] = 'no-repeat'
                self.piece.style['background-size'] = '22px 22px'
                self.piece.style['background-color'] = 'transparent'
                self.piece.style['position'] = 'absolute'
                self.piece.style['left'] = str(2+23*j) + 'px'
                self.piece.style['top'] = str(2+23*i) + 'px'
                self.images.append(self.piece)
                container.append(self.piece)
        container.onmousedown.do(self.on_place_piece)
        pass_button = gui.Button('Pass')
        pass_button.onclick.do(self.pass_turn)
        screen.append(container)
        screen.append(pass_button)
        return screen
    
    def on_place_piece(self, widget, x, y):
        new_pos = self.calculate_closest_point(int(x), int(y))

        if not self.board.invalid_inter((new_pos[0]-2)//23, (new_pos[1]-2)//23, self.player):
            self.board.update_board((new_pos[0]-2)//23, (new_pos[1]-2)//23, self.player)
            for i in range(19):
                for j in range(19):
                    if self.board.grid[i][j] == 2:
                        self.images[j+i*19].style['background-image'] = "url('/my_res:black_stone.png')"
                    elif self.board.grid[i][j] == 1:
                        self.images[j+i*19].style['background-image'] = "url('/my_res:white_stone.png')"
                    else:
                        self.images[j+i*19].style['background-image'] = "none"
            self.player = 3 - self.player

    def calculate_closest_point(self, x, y):
        coord_x = x - 14
        coord_y = y - 14
        rem_x = coord_x % 23
        rem_y = coord_y % 23

        low_x = coord_x - rem_x
        low_y = coord_y - rem_y
        high_x = coord_x
        if coord_x % 23 != 0:
            high_x = coord_x + 23 - rem_x
        high_y = coord_y
        if coord_y % 23 != 0:
            high_y = coord_y + 23 - rem_y
        man_lower_left = abs(low_x - coord_x) + abs(high_y - coord_y)
        man_lower_right = abs(high_x - coord_x) + abs(high_y - coord_y)
        man_upper_left = abs(low_x - coord_x) + abs(low_y - coord_y)
        man_upper_right = abs(high_x - coord_x) + abs(low_y - coord_y)
        if min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_lower_left:
            return [low_x+2, high_y+2]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_lower_right:
            return [high_x+2, high_y+2]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_upper_left:
            return [low_x+2, low_y+2]
        else:
            return [high_x+2, low_y+2]

    def pass_turn(self, widget):
        self.player = 3 - self.player
        
start(BetaGo)