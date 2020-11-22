import time
from math import log, sqrt
import model
import random
import copy
import pickle
from collections import defaultdict


class MonteCarlo():
    def __init__(self, board):
        self.board: model.HexModel = board
        self.states = []
        self.plays = {}
        self.wins = {}
        self.parameter = 2
        self.dict = {}


    def get_move(self, max_time):
        player = self.board.current_player()
        print('player:', player)
        blanks = self.board.legal_moves(self.board.board)
        start = time.time()
        while time.time() - start < max_time:
            self.run_simulation()

        next_states = []
        for x in blanks:
            state_temp = copy.deepcopy(self.board.board)
            next_states.append((x, self.board.place_chess2(x, state_temp)))


        precent_wins, move = max(
            (self.wins.get((player, self.list_to_str(s)), 0) /
             self.plays.get((player, self.list_to_str(s)), 1),
             p)
            for p, s in next_states
        )
        print(precent_wins)
        print("states")
        print(self.states)
        # print("wins")
        # print(self.wins)
        # print("plays")
        # print(self.plays)
        return precent_wins, move

    def run_simulation(self):
        plays = self.plays
        wins = self.wins
        state = copy.deepcopy(self.board.board)
        visited = []
        player = self.board.current_player()
        # player = self.board.last_player(state)

        expand = True
        while True:
            blanks = self.board.legal_moves(state)

            next_states = []
            for x in blanks:
                state_temp = copy.deepcopy(state)
                next_states.append((x, self.board.place_chess2(x, state_temp)))

            # print(next_states[0])

            if all(plays.get((player, self.list_to_str(s))) for _, s in next_states):
                log_num_simulation = log(sum(plays[(player, self.list_to_str(s))] for _, s in next_states))
                value, move, state = max(
                    ((wins[(player, self.list_to_str(s))] / plays[(player, self.list_to_str(s))]) +
                     self.parameter * sqrt(log_num_simulation / plays[(player, self.list_to_str(s))]), p, s)
                    for p, s in next_states
                )
                # print('value:', value, 'move:', move, 'state:', state)
            else:
                move, state = random.choice(next_states)

            if expand and (player, self.list_to_str(state)) not in self.plays:
                expand = False
                self.plays[(player, self.list_to_str(state))] = 0
                self.wins[player, self.list_to_str(state)] = 0

            visited.append((player, self.list_to_str(state)))
            player = self.board.last_player(state)
            winner = self.board.get_winner(state)
            if winner != 2:
                break
        for player, board in visited:

            if (player, board) not in self.plays:
                continue
            self.plays[(player, board)] += 1
            if player == winner:
                self.wins[(player, board)] += 1

    def list_to_str(self, l):
        temp = ''
        for i in range(len(l)):
            for j in range(len(l[0])):
                temp += str(l[i][j])
        return temp

    def dumpObjectFile(self):
        # self.dict.append(["states"] self.states)
        # self.dict["plays"] = self.plays
        # self.dict["wins"] = self.wins
        #d = defaultdict(list)
        #print("dict:")
        #print(self.dict)
        MonteCarlo_out = open("dict.MonteCarlo", "wb")
        pickle.dump(self, MonteCarlo_out)
        MonteCarlo_out.close()


    def loadObjectFile(self):
        print("loading object!")
        MonteCarlo_in = open("dict.MonteCarlo", "rb")
        MCDict = pickle.load(MonteCarlo_in)
        self.dict = MCDict
        print("dumped wins")
        print(self.dict["wins"])
        

        

