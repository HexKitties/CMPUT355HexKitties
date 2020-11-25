from model import HexModel
import random
import matplotlib.pyplot as plt


class ModelTest(HexModel):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.current_move = None
        self.probability = {i: 0 for i in range(self.rows[0] * self.rows[0] + 1)}

    def random_move(self):
        legal_moves = self.legal_moves(self.board)
        choice = random.choice(legal_moves)
        return choice

    def new_test(self):
        self.new_game()
        self.probability = {i: 0 for i in range(self.rows[0] * self.rows[0] + 1)}

    def simulate(self):
        self.new_test()
        num_move = 0
        while self.get_winner(self.board) == 2:
            num_move += 1
            if self.player[self.current_player()] == "random":
                self.current_move = self.random_move()
            else:
                prediction, self.current_move = self.monte_carlo.get_move(self.waiting_time)
                self.probability[num_move] = prediction
            self.place_chess(self.current_move)
        if self.load:
            self.dump_Monte_Carlo_obj()
        return self.probability, self.get_winner(self.board)



if __name__ == '__main__':
    iterations = 10
    '''
    random versus monte carlo
    '''
    # test = ModelTest(player={0: "random", 1: "mc"})
    # count = 0
    # for i in range(iterations):
    #     p1, winner = test.simulate()
    #     print("winner is:", winner)
    #     if winner == 1:
    #         count += 1
    # print(count/100)

    '''
    # monte carlo versus monte carlo
    '''
    count = 0
    test2 = ModelTest(player={0: "mc", 1: "mc"})
    probability2 = {i: [0, 0] for i in range(test2.rows[0] * test2.rows[0] + 1)}
    for i in range(iterations):
        p2, winner = test2.simulate()
        print("iteration " + str(i) + " winner is:", winner)
        if winner == 0:
            count += 1
        for item in p2.keys():
            if p2[item] != 0:
                probability2[item][0] = probability2[item][0] + 1
                probability2[item][1] = probability2[item][1] + (p2[item] - probability2[item][1]) / probability2[item][0]

    print(count / 100)
    moves = [i for i in range(test2.rows[0] * test2.rows[0] + 1)]
    pro = [probability2[item][1] for item in range(test2.rows[0] * test2.rows[0] + 1)]
    plt.plot(moves, pro)
    plt.xlabel("number of move")
    plt.ylabel("prediction of winning")
    plt.show()
