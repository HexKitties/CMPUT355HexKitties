import globvar
import copy
from collections import deque
import monte_carlo


class HexModel():
    def __init__(self, radius=40, size=(4, 4), color=(128, 128, 128), players_color=((255, 0, 0), (0, 0, 255)), mode=0):

        self.radius = radius
        self.size = size
        self.default_color = color
        self.players = players_color
        self.player_turn = 0
        self.board = self.init_board()
        self.history = []
        self.modes = {0: "REAL PLAYER", 1: "AI PLAYER"}
        self.current_mode = mode
        self.monte = monte_carlo.MonteCarlo(self)

        self.BTM_ROW = set()
        for x in range(self.size[1]):
            self.BTM_ROW.add((self.size[1] - 1, x))
        self.TOP_ROW = set()
        for x in range(self.size[1]):
            self.TOP_ROW.add((0, x))
        self.LFT_COL = set()
        for x in range(self.size[0]):
            self.LFT_COL.add((x, 0))
        self.RGT_COL = set()
        for x in range(self.size[0]):
            self.RGT_COL.add((x, self.size[0] - 1))

        self.nbrs = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                temp = []
                if i > 0:
                    temp.append((i - 1, j))
                if i > 0 and j < self.size[1] - 1:
                    temp.append((i - 1, j + 1))
                if j > 0:
                    temp.append((i, j - 1))
                if j < self.size[1] - 1:
                    temp.append((i, j + 1))
                if i < self.size[0] - 1 and j > 0:
                    temp.append((i + 1, j - 1))
                if i < self.size[0] - 1:
                    temp.append((i + 1, j))
                self.nbrs[(i, j)] = temp

    def init_board(self):
        empty_brd = []
        for i in range(self.size[0]):
            temp = []
            for i in range(self.size[1]):
                temp.append(-1)
            empty_brd.append(temp)
        return empty_brd

    def get_current_mode(self):
        return self.current_mode

    def move(self):
        _, next_move = self.monte.get_move(10)
        self.place_chess(next_move)

    def place_chess(self, chess_pos):
        if self.board[chess_pos[0]][chess_pos[1]] == -1:
            self.board[chess_pos[0]][chess_pos[1]] = self.player_turn
            self.player_turn = (self.player_turn + 1) % 2
            self.history.append(chess_pos)

            check = self.get_winner(self.board)
            if check != 2:
                self.current_mode = 0
                print("winner is", check)
                # self.board = self.init_board()
            return True
        return False

    def place_chess2(self, chess_pos, board):
        player = (self.last_player(board) + 1) % 2
        board[chess_pos[0]][chess_pos[1]] = player
        return board

    def str_rep(self):
        return ''.join([str(elem) for elem in self.board])

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

    def notify_update(self, mouse_pos, text):
        globvar.hex_view.display(self.radius, self.size, self.default_color, self.board, mouse_pos, text)

    def legal_moves(self, board):
        temp = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if board[i][j] == -1:
                    temp.append((i, j))
        return temp

    def current_player(self):
        return self.player_turn

    def last_player(self, board):  # the player that last moved, assume 0 moves first
        count = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if board[i][j] == 1 or board[i][j] == 0:
                    count += 1
        if count % 2 == 0:
            return 1
        else:
            return 0

    def get_winner(self, board):
        set1, set2 = (self.TOP_ROW, self.BTM_ROW)
        # print('has_win', brd, who, set1, set2)
        Q, seen = deque([]), set()
        for c in set1:
            if board[c[0]][c[1]] == 0:
                Q.append(c)
                seen.add(c)
        while len(Q) > 0:
            c = Q.popleft()
            if c in set2:
                return 0
            for d in self.nbrs[c]:
                if board[d[0]][d[1]] == 0 and d not in seen:
                    Q.append(d)
                    seen.add(d)

        set1, set2 = (self.LFT_COL, self.RGT_COL)
        # print('has_win', brd, who, set1, set2)
        Q, seen = deque([]), set()
        for c in set1:
            if board[c[0]][c[1]] == 1:
                Q.append(c)
                seen.add(c)
        while len(Q) > 0:
            c = Q.popleft()
            if c in set2:
                return 1
            for d in self.nbrs[c]:
                if board[d[0]][d[1]] == 1 and d not in seen:
                    Q.append(d)
                    seen.add(d)
        return 2