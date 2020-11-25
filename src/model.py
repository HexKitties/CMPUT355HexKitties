import globvar
import copy
from collections import deque
import monte_carlo
import pickle
import os


class HexModel():

    def __init__(self, radius=40, size=(5, 5), color=(128, 128, 128), players_color=((255, 0, 0), (0, 0, 255)), mode=1, waiting_time=1, load=True):

        self.radius = radius
        self.size = size
        self.rows = size
        self.cols = size
        self.default_color = color
        self.players = players_color
        self.player_turn = 0
        self.board = self.init_board()
        self.history = []
        self.modes = {0: "REAL PLAYER", 1: "AI PLAYER"}
        self.current_mode = mode
        self.waiting_time = waiting_time
        self.win_path = []
        self.load = load

        self.monte_carlo = monte_carlo.MonteCarlo(self)
        self.load_Monte_Carlo_Obj()
        # print(self.monte_carlo.wins)

        self.setup()

    def setup(self):
        '''
        This function will calculate the set of coordinates eg. (0, 0) for the boundaries,
        which are the top and bottom rows, rightmost and leftmost columns. It will also
        setup a dictionary that stores all the neighboring coordinates. Both of these
        attributes are helpful for checking winning state and looking for winning path.
        '''
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

    def clear_win_path(self):
        # design for new game clear path
        self.win_path = []
        pass

    def init_board(self):
        '''
        This function will create the corresponding hex board using the size attirbute
        of the class object. The board is initiated with -1 for all positions in the
        board. Note that -1 represents empty position, 0 and 1 represent the first or
        second player's chess on that position.

        return empty_brd: a 2D list with all position initiated as value -1
        '''
        empty_brd = []
        for i in range(self.size[0]):
            temp = []
            for i in range(self.size[1]):
                temp.append(-1)
            empty_brd.append(temp)
        return empty_brd

    def get_current_mode(self):
        '''
        This function returns the current playing mode (REAL PLAYER or AI PLAYER).

        return self.current_mode: either 0 (REAL PLAYER) or 1 (AI PLAYER)
        '''
        return self.current_mode

    def move(self):
        '''
        This function generate the next move
        '''
        # print(self.waiting_time)
        _, next_move = self.monte_carlo.get_move(self.waiting_time)
        print("next_move: ", next_move)
        self.place_chess(next_move)

    def place_chess(self, chess_pos):
        '''
        This function will take the chess_pos as argument and add it in to the current
        chess board board. If the position of the new chess is empty, then it will be
        added successfully and return True where the chess position will be added into the history for
        undo functionality. Otherwise, chess will not be added and it will return False.

        return True or False
        '''
        if self.board[chess_pos[0]][chess_pos[1]] == -1:  # chess position is empty
            self.board[chess_pos[0]][chess_pos[1]] = self.player_turn

            self.player_turn = (self.player_turn + 1) % 2
            self.history.append(chess_pos)
            return True
        return False

    def place_chess2(self, chess_pos, board):
        player = (self.last_player(board) + 1) % 2
        board[chess_pos[0]][chess_pos[1]] = player
        return board

    def str_rep(self):
        return ''.join([str(elem) for elem in self.board])

    def new_game(self):
        '''
        This function will create a new game, or reset the attributes of the hex board,
        for example clearing the board, history, winning path, and setup the other settings.
        '''
        self.board = self.init_board()
        self.setup()
        self.clear_win_path()
        self.history = []
        self.current_mode = 1
        self.player_turn = 0

    def switch_mode(self):
        '''
        This function will change the mode:
        REAL PLAYER --> AI PLAYER
        or
        AI PLAYER ---> REAL PLAYER
        '''
        self.current_mode = (self.current_mode + 1) % 2

    def undo(self):
        '''
        This function will delete the last chess placed on the board if the current
        mode is REAL PLAYER mode, or, it will delete the last two chess placed on the
        board so that the last chess placed by the user and the program are both removed
        from the history list.

        return True if successfully undo. False if failed.
        '''
        if self.current_mode == 0:  # real player mode
            if len(self.history) > 0:
                last_pos = self.history.pop()
                self.board[last_pos[0]][last_pos[1]] = -1
                self.player_turn = (self.player_turn + 1) % 2
                return True
        else:  # AI player mode
            if len(self.history) > 1:
                last_pos = self.history.pop()
                self.board[last_pos[0]][last_pos[1]] = -1
                self.player_turn = (self.player_turn + 1) % 2
                last_pos = self.history.pop()
                self.board[last_pos[0]][last_pos[1]] = -1
                self.player_turn = (self.player_turn + 1) % 2
                return True
        return False

    def notify_update(self, mouse_pos, text):
        '''
        This function will update the screen by passing all the required values
        to the view as parameter. By calling this function, the view will show the latest
        board, buttons, or messages.
        '''
        globvar.hex_view.display(self.radius, self.size, self.default_color, self.board, mouse_pos, text)

    def legal_moves(self, board):
        temp = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if board[i][j] == -1:
                    temp.append((i, j))
        return temp

    def current_player(self):
        '''
        This function return the turn of current player:
        return 0 (first player: red by default)
               1 (second player: blue by default)
        '''
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

    def opponent(self, player):
        # return the opponent of the given player
        if player == 1:
            return 0
        elif player == 0:
            return 1

    def get_winner(self, board):
        '''
        This function will get the winner according to the board, return 2 if nobody win yet
        the arugment board is the object current runing board, the array
        return 0, 1 represent the player number
        '''
        # design for getting winner, main thought/algorithm from code provided by course website, but written by ourself
        set1, set2 = (self.TOP_ROW, self.BTM_ROW)
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

    def winning_path(self, board, winner):
        '''
        This function will receive board position and winner(represent by number) to find a winning PATH ,return a
        list of array containing a winning path
        '''
        print(self.board)
        if winner == 0:
            set1 = copy.deepcopy(deque(self.TOP_ROW))
            set2 = self.BTM_ROW
        else:
            set1 = copy.deepcopy(deque(self.LFT_COL))
            set2 = self.RGT_COL
        winning_path = []
        last_one = None
        find = False
        Parent = dict()
        seen = set()
        while not find:
            Q = deque([])
            Parent = dict()
            for i in set1:
                if board[i[0]][i[1]] == winner and i not in seen:
                    Q.append(i)
                    seen.add(i)
                    Parent[i] = i
                    break
            while len(Q) > 0:
                parent = Q.pop()
                for i in self.nbrs[parent]:
                    if board[i[0]][i[1]] == winner and i not in seen:
                        if i in set1:
                            set1.remove(i)
                        Q.append(i)
                        seen.add(i)
                        Parent[i] = parent
                        if i in set2:
                            find = True
                            last_one = i
                            Q = deque([])
                            break
        winning_path.append(last_one)
        while Parent[last_one] != last_one:
            last_one = Parent[last_one]
            winning_path.append(last_one)

        # simplify the path
        if winner == 0:
            set1 = self.TOP_ROW
        else:
            set1 = self.LFT_COL
        if winning_path[1] in set1:
            extra = winning_path[0]
            winning_path.remove(extra)
        if winning_path[len(winning_path)-2] in set2:
            extra = winning_path[len(winning_path) - 1]
            winning_path.remove(extra)
        return winning_path

    # a simple way to tell if there is a win-link for the player, which slightly reduces the search space.
    def win_link(self, move, player, board):
        count = 0
        for i in self.nbrs[move]:
            if board[i[0]][i[1]] == -1:
                b = copy.deepcopy(board)
                b[i[0]][i[1]] = player
                winner = self.get_winner(b)
                if winner != 2:
                    count += 1
        if count >= 2:
            return True
        else:
            return False

    def dump_Monte_Carlo_obj(self):
        if self.load:
            cur_path = os.path.dirname(__file__)
            path = os.path.relpath('../data/MonteCarlo%s'%(self.size,), cur_path)
            MonteCarlo_out = open(path, "wb")
            pickle.dump(self.monte_carlo.plays, MonteCarlo_out)
            pickle.dump(self.monte_carlo.wins, MonteCarlo_out)
            MonteCarlo_out.close()

    def load_Monte_Carlo_Obj(self):
        if self.load:
            cur_path = os.path.dirname(__file__)
            path = os.path.relpath('../data/MonteCarlo%s'%(self.size,), cur_path)
            try:
                MonteCarlo_in = open(path, "rb+")
                self.monte_carlo.plays = pickle.load(MonteCarlo_in)
                self.monte_carlo.wins = pickle.load(MonteCarlo_in)
            except:
                f = open(path, "w+")
                f.close()