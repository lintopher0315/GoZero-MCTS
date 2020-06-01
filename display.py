import remi.gui as gui
import copy
from remi import start, App
from game_logic import Board
from MCTS import MCTS

class BetaGo(App):

    board = Board()
    ai = MCTS()
    player = 2
    images = []
    passes = 0
    in_game = True
    white_score = gui.Label("")
    black_score = gui.Label("")
    move_num = 1

    def __init__(self, *args):
        super(BetaGo, self).__init__(*args, static_file_path = {'my_res':'./res/'})

    def main(self):
        full = gui.Container(width=700, height=700, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        full.style['box-shadow'] = "none"

        screen = gui.Container(width=441, height=700)
        screen.style['box-shadow'] = "none"

        title_container = gui.Container(width='100%', height=50, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        black_icon = gui.Container(width=40, height=40)
        black_icon.style['background-image'] = "url('/my_res:black_stone.png')"
        black_icon.style['background-repeat'] = 'no-repeat'
        black_icon.style['background-size'] = '40px 40px'
        black_icon.style['background-color'] = 'transparent'
        black_icon.style['position'] = 'absolute'
        black_icon.style['top'] = "5px"
        black_icon.style['left'] = "5px"
        black_title = gui.Label("You")
        black_title.style['font-family'] = "Courier New"
        black_title.style['position'] = 'absolute'
        black_title.style['font-size'] = "32px"
        black_title.style['padding-top'] = "7px"
        black_title.style['padding-left'] = "50px"
        white_title = gui.Label("BetaGo")
        white_title.style['font-family'] = "Courier New"
        white_title.style['position'] = 'absolute'
        white_title.style['font-size'] = "32px"
        white_title.style['top'] = "7px"
        white_title.style['left'] = "275px"
        white_icon = gui.Container(width=50, height=50)
        white_icon.style['background-image'] = "url('/my_res:white_stone.png')"
        white_icon.style['background-repeat'] = 'no-repeat'
        white_icon.style['background-size'] = '40px 40px'
        white_icon.style['background-color'] = 'transparent'
        white_icon.style['position'] = 'absolute'
        white_icon.style['top'] = "5px"
        white_icon.style['left'] = "396px"
        self.black_score.style['font-family'] = 'Courier New'
        self.black_score.style['color'] = '#ff0066'
        self.black_score.style['font-style'] = 'italic'
        self.black_score.style['position'] = 'absolute'
        self.black_score.style['font-size'] = '22px'
        self.black_score.style['top'] = '13px'
        self.black_score.style['left'] = '128px'
        #self.black_score.style['visibility'] = 'Courier New'
        self.white_score.style['font-family'] = 'Courier New'
        self.white_score.style['color'] = '#ff0066'
        self.white_score.style['font-style'] = 'italic'
        self.white_score.style['position'] = 'absolute'
        self.white_score.style['font-size'] = '22px'
        self.white_score.style['top'] = '13px'
        self.white_score.style['left'] = '225px'
        title_container.append(black_icon)
        title_container.append(black_title)
        title_container.append(self.black_score)
        title_container.append(self.white_score)
        title_container.append(white_title)
        title_container.append(white_icon)

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
                self.piece.style['top'] = str(52+23*i) + 'px'
                self.images.append(self.piece)
                container.append(self.piece)
        container.onmousedown.do(self.on_place_piece)
        pass_button = gui.Button('Pass')
        pass_button.onclick.do(self.pass_turn)
        new_game_button = gui.Button('New Game')
        new_game_button.onclick.do(self.new_game)

        self.list_view = gui.ListView(selectable=False, width=100, height=441)
        self.list_view.style['border'] = "1px groove gray"
        self.list_view.style['margin-top'] = '50px'
        self.list_view.style['margin-left'] = '25px'

        screen.append(title_container)
        screen.append(container)
        screen.append(pass_button)
        screen.append(new_game_button)

        full.append([screen, self.list_view])

        return full
    
    def update_view(self):
        for i in range(19):
            for j in range(19):
                if self.board.grid[i][j] == 2:
                    self.images[j+i*19].style['background-image'] = "url('/my_res:black_stone.png')"
                elif self.board.grid[i][j] == 1:
                    self.images[j+i*19].style['background-image'] = "url('/my_res:white_stone.png')"
                else:
                    self.images[j+i*19].style['background-image'] = "none"

    def on_place_piece(self, widget, x, y): # make sure you cant click on board when MCTS is thinking
        if self.in_game:
            new_pos = self.calculate_closest_point(int(x), int(y))

            if not self.board.invalid_inter((new_pos[0]-2)//23, (new_pos[1]-2)//23, self.player):
                self.board.update_board((new_pos[0]-2)//23, (new_pos[1]-2)//23, self.player)
                side = 'BW'
                if self.player == 1:
                    side = 'WB'
                self.list_view.append(str(self.move_num)+'. '+side[0]+'['+chr((new_pos[0]-2)//23+97)+chr((new_pos[1]-2)//23+97)+']')
                self.update_view()
                self.player = 3 - self.player
                self.passes = 0
                self.move_num += 1

                b = self.ai.find_next_move(copy.deepcopy(self.board), self.player)
                coord = b.move_history[len(b.move_history)-1]
                self.list_view.append(str(self.move_num)+'. '+side[1]+'['+chr(coord[0]+97)+chr(coord[1]+97)+']')
                '''
                for i in range(19):
                    for j in range(19):
                        if self.board.grid[i][j] != b.grid[i][j]:
                            self.list_view.append(str(self.move_num)+'. '+side[1]+'['+chr(j+97)+chr(i+97)+']')
                '''
                self.board = copy.deepcopy(b)
                self.update_view()
                self.move_num += 1

                self.player = 3 - self.player

    def calculate_closest_point(self, x, y):
        coord_x = x - 14
        coord_y = y - 64
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
            return [low_x+2, high_y+52]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_lower_right:
            return [high_x+2, high_y+52]
        elif min(man_lower_left, man_lower_right, man_upper_left, man_upper_right) == man_upper_left:
            return [low_x+2, low_y+52]
        else:
            return [high_x+2, low_y+52]

    def pass_turn(self, widget):
        self.player = 3 - self.player
        self.passes += 1
        self.board.passes += 1
        if self.passes == 2:
            self.in_game = False
            score = self.board.get_score()
            self.white_score.text = str(score[0])
            self.black_score.text = str(score[1])
        b = self.ai.find_next_move(copy.deepcopy(self.board), self.player)
        self.board = copy.deepcopy(b)
        self.update_view()

        self.player = 3 - self.player

    def new_game(self, widget):
        self.board.clear_board()
        for image in self.images:
            image.style['background-image'] = "none"
        self.passes = 0
        self.in_game = True
        self.player = 2
        self.white_score.text = ""
        self.black_score.text = ""
        self.move_num = 1
        self.list_view.empty()
        
start(BetaGo)