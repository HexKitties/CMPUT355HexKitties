import globvar

class HexModel():
    def __init__(self, radius=40, size=(8, 8), color=(128,128,128), start_pos = (120, 120)):
        self.radius = radius
        self.size = size
        self.default_color = color
        self.start_pos = start_pos
        self.chess_pos = self.init_board()
        self.history = []

    def init_board(self):
    	empty_brd = []
    	for i in range(self.size[0]):
    		temp = []
    		for i in range(self.size[1]):
    			temp.append(0)
    		empty_brd.append(temp)
    	return empty_brd

    def place_chess(self, current_mouse):
        if self.chess_pos[current_mouse[0]][current_mouse[1]] == 0:
            self.chess_pos[current_mouse[0]][current_mouse[1]] = 1
            self.history.append(current_mouse)
            return True
        return False

    def notify_update(self, mouse_pos):
        globvar.hex_view.draw_board(self.radius, self.size, self.default_color, self.chess_pos, self.start_pos, mouse_pos)