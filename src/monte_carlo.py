import time
from math import log, sqrt
import model
import random
import copy
import pickle
from collections import defaultdict

'''
main algorithm using MonteCarlo tree search with UCT
Refference:
http://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
'''
class MonteCarlo():
    def __init__(self, board):
        self.board = board
        self.plays = {}
        self.wins = {}
        self.parameter = 1.7
        self.activate = False
        random.seed(time.time())

    # Get next move for the AI
    def get_move(self, max_time):
        player = self.board.current_player()
        print('player:', player)
        blanks = self.board.legal_moves(self.board.board)
        start = time.time()
        while time.time() - start < max_time:
            self.run_simulation()

        # All possible next move
        next_states = []
        for x in blanks:
            state_temp = copy.deepcopy(self.board.board)
            next_states.append((x, self.board.place_chess2(x, state_temp)))

        # Return move with highest win rate
        precent_wins, move = max(
            (self.wins.get((player, self.list_to_str(s)), 0) /
             self.plays.get((player, self.list_to_str(s)), 1),
             p)
            for p, s in next_states
        )
        print("winning prob: ", precent_wins)
        return precent_wins, move

    def get_percentage(self, chess_pos, player):
        blanks = self.board.legal_moves(self.board.board)
        if self.activate:
            self.run_simulation()
        # All possible next move
        next_states = []
        for x in blanks:
            if x == chess_pos:
                state_temp = copy.deepcopy(self.board.board)
                s = self.board.place_chess2(x, state_temp)
                return self.wins.get((player, self.list_to_str(s)), 0) / self.plays.get((player, self.list_to_str(s)), 1)
        return -1


    # Random play simulation
    def run_simulation(self):
        plays = self.plays
        wins = self.wins
        state = copy.deepcopy(self.board.board)
        visited = []
        player = self.board.current_player()
        # player = self.board.last_player(state)

        # Expand the node until new state is discovered
        expand = True
        while True:
            blanks = self.board.legal_moves(state)

            next_states = []
            for x in blanks:
                state_temp = copy.deepcopy(state)
                next_states.append((x, self.board.place_chess2(x, state_temp)))

            # print(next_states[0])

            # If all moves have been expanded, choose a move currently has the highest win rate
            if all(self.plays.get((player, self.list_to_str(s))) for _, s in next_states):
                log_num_simulation = log(sum(self.plays[(player, self.list_to_str(s))] for _, s in next_states))
                value, move, state = max(
                    ((self.wins[(player, self.list_to_str(s))] / self.plays[(player, self.list_to_str(s))]) +
                     self.parameter * sqrt(log_num_simulation / self.plays[(player, self.list_to_str(s))]), p, s)
                    for p, s in next_states
                )
                # print('value:', value, 'move:', move, 'state:', state)
            # Otherwise, choose a random move
            else:
                move, state = random.choice(next_states)

            # New node discovered, initialize its values
            if expand and (player, self.list_to_str(state)) not in self.plays:
                expand = False
                self.plays[(player, self.list_to_str(state))] = 0
                self.wins[player, self.list_to_str(state)] = 0

            # Update visited
            visited.append((player, self.list_to_str(state)))
            player = self.board.last_player(state)
            winner = self.board.get_winner(state)

            # game ends if there is a simple win_link
            if self.board.win_link(move, self.board.last_player(state), state):
                break

            # game ends when a play wins
            if winner != 2:
                break
        # Update statistics for this simulation
        for player, board in visited:

            if (player, board) not in self.plays:
                continue
            self.plays[(player, board)] += 1
            if player == winner:
                self.wins[(player, board)] += 1

    # hash a list to a string
    def list_to_str(self, l):
        temp = ''
        for i in range(len(l)):
            for j in range(len(l[0])):
                temp += str(l[i][j])
        return temp



        

        

