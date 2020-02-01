import remi.gui as gui
from remi import start, App
from game_logic import Board

class Go(App):

    board = Board()
    player = 2

    def __init__(self, *args):
        super(Go, self).__init__(*args)

    def main(self):
        container = gui.Container(width=441, height=441)
        container.style['background-image'] = "url('https://senseis.xmp.net/diagrams/29/ad217a381dbb8bc75d8420f6aec40af5.png')"
        container.onmousedown.do(self.on_place_piece)
        return container
    
    def on_place_piece(self, widget, x, y):
        new_pos = self.calculate_closest_point(int(x), int(y))

        if not self.board.inter_occupied((new_pos[0]-4)//23, (new_pos[1]-4)//23):
            self.board.update_board((new_pos[0]-4)//23, (new_pos[1]-4)//23, self.player)
            self.piece = gui.Container(width=20, height=20)
            if self.player == 1:
                self.piece.style['background-image'] = "url('https://i.imgur.com/IAU4S7D.png')"
            elif self.player == 2:
                self.piece.style['background-image'] = "url('https://i.imgur.com/iW25PZP.png')"
            self.piece.style['background-repeat'] = 'no-repeat'
            self.piece.style['background-size'] = '20px 20px'
            self.piece.style['background-color'] = 'transparent'
            self.piece.style['position'] = 'absolute'
            self.piece.style['left'] = str(new_pos[0]) + 'px'
            self.piece.style['top'] = str(new_pos[1]) + 'px'

            self.player = 3 - self.player
            widget.append(self.piece)

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
            return [low_x+4, high_y+4]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_lower_right:
            return [high_x+4, high_y+4]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_upper_left:
            return [low_x+4, low_y+4]
        else:
            return [high_x+4, low_y+4]
        
start(Go)