import pygame
import globvar

import monte_carlo

import logging
import threading
import time


class HexController():
    def __init__(self):
        self.STOPMSG = pygame.USEREVENT + 1
        self.mouse_pos = (-1, -1)
        self.pos_on_board = None
        self.on_button = (False, None)
        self.buttons = {"newgame": 0, "exit": 1, "playermode": 2, "undo": 3}
        self.print_message = False
        self.text = None

    def interaction(self):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.pos_on_board != None:
                        if globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
                            chess_status,winner = globvar.hex_brd.place_chess(self.pos_on_board)
                            if chess_status == False and not self.on_button[0]:
                                self.show_message('please place chess on empty position')
                            else:
                                globvar.hex_brd.notify_update(self.mouse_pos, self.text)
                                check = globvar.hex_brd.get_winner(globvar.hex_brd.board)
                                if check != 2:
                                    # self.current_mode = 0
                                    print("winner is", check)
                                    globvar.hex_ctrl.show_message('Player '+str(check + 1) + ' has won',)
                                    # self.board = self.init_board()
                                    win_path = globvar.hex_brd.winning_path(globvar.hex_brd.board, check)
                                    print("winning path is:", win_path, "\n")
                                    globvar.hex_brd.win_path = win_path


                                elif globvar.hex_brd.current_mode == 1:  # AI player mode
                                    self.run_thread()
                        else:
                            self.show_message(
                                'Player' + str(globvar.hex_brd.get_winner(globvar.hex_brd.board) + 1) + ' has won')
                    elif not self.on_button[0]:
                        if globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
                            self.show_message('Do not place chess out of board')
                    if self.on_button[0]:
                        button = self.buttons[self.on_button[1]]
                        if not self.press_button(button):  # return False if quit button is pressed
                            return False
                        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == self.STOPMSG:
                pygame.time.set_timer(self.STOPMSG, 0)
                self.print_message = False
                self.text = None
                globvar.hex_brd.notify_update(self.mouse_pos, self.text)

        return True

    def show_message(self, text):
        # if (self.pos_on_board) == None:
        # print("haha")
        self.print_message = True
        self.text = text
        pygame.time.set_timer(self.STOPMSG, 1000)
        globvar.hex_brd.notify_update(self.mouse_pos, text)

    def press_button(self, button):
        if button == 0:
            globvar.hex_brd.new_game()
            # globvar.hex_brd.clear_win_path()
        elif button == 1:
            return False
        elif button == 2:
            globvar.hex_brd.switch_mode()
        elif button == 3:
            if globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
                globvar.hex_brd.undo()
            else:
                self.show_message('Cannot Undo, Player'+str(globvar.hex_brd.get_winner(globvar.hex_brd.board)+1) +
                                  ' has won')
        return True

    def run_thread(self):
        # https://realpython.com/intro-to-python-threading/
        format = "%(asctime)s: %(message)s"
        # logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        # logging.info("Main    : before creating thread")
        gen_move = threading.Thread(target=self.move_thread_function, args=(1,))
        print_loading = threading.Thread(target=self.print_thread_function, args=(2,))
        # logging.info("Main    : before running thread")
        print_loading.start()
        gen_move.start()
        # logging.info("Main    : wait for the thread to finish")
        print_loading.join()
        gen_move.join()
        pygame.event.clear()
        # logging.info("Main    : all done")

    def move_thread_function(self, name):
        # https://realpython.com/intro-to-python-threading/
        # logging.info("Thread %s: starting", name)
        print("generating next move ...")
        globvar.hex_brd.move()
        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
        # logging.info("Thread %s: finishing", name)
        print("done\n")

    def print_thread_function(self, name):
        # https://realpython.com/intro-to-python-threading/
        # logging.info("Thread %s: starting", name)
        waiting_time = globvar.hex_brd.waiting_time - 1
        while waiting_time > 0:
            self.show_message("loading . . . " + str(waiting_time) + "s")
            time.sleep(1)
            waiting_time -= 1
        # logging.info("Thread %s: finishing", name)

