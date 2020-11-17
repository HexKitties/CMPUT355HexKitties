import globvar

class HexModel():
    def __init__(self, radius=40, size=(8, 8), color=(128,128,128), players_color = ((255, 0, 0), (0, 0, 255)), mode = 0):
        self.radius = radius
        self.size = size
        self.default_color = color
        self.players = players_color
        self.player_turn = 0
        self.board = self.init_board()
        self.history = []
        self.modes = {0: "REAL PLAYER", 1: "AI PLAYER"}
        self.current_mode = mode

    def init_board(self):
    	empty_brd = []
    	for i in range(self.size[0] ):
    		temp = []
    		for i in range(self.size[1]):
    			temp.append(-1)
    		empty_brd.append(temp)
    	return empty_brd

    def place_chess(self, chess_pos):
        if self.board[chess_pos[0]][chess_pos[1]] == -1:
            self.board[chess_pos[0]][chess_pos[1]] = self.player_turn
            self.player_turn = (self.player_turn + 1) % 2
            self.history.append(chess_pos)
            return True
        return False

    def new_game(self):
        self.board = self.init_board()

    def switch_mode(self):
        self.current_mode = (self.current_mode + 1) % 2

    def undo(self):
    	if len(self.history) != 0:
    		last_pos = self.history.pop()
    		self.board[last_pos[0]][last_pos[1]] = -1
    		self.player_turn = (self.player_turn + 1) % 2
    		return True
    	return False

    def notify_update(self, mouse_pos):
        globvar.hex_view.display(self.radius, self.size, self.default_color, self.board, mouse_pos)

    def notify_wrongly(self,text):
        globvar.hex_view.draw_wrong_notify(text)
