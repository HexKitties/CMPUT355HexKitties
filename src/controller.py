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
        self.buttons = {"newgame": 0, "menu": 1, "REAL PLAYER": 2, "AI PLAYER": 2,
         "undo": 3, "LEVEL": 4, "SIZE": 5, "START": 6, "CONTINUE": 7, "WIN %": 8, "QUIT": 9}
        self.print_message = False
        self.text = None
        self.menu = True
        # show winning percentage flag
        self.show_win_p = False

    def interaction(self):
        '''
        This function is the main interaction function, will always return true, unless user
        click quit button, then game will end in the main.py
        '''

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                if self.menu:
                    globvar.menu.draw_menu(self.mouse_pos)
                else:
                    globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.menu:
                        globvar.menu.draw_menu(self.mouse_pos)
                    elif self.pos_on_board != None:
                        win_color = self.win_color()[0]
                        if win_color == "":
                            # nobody wins yet
                            chess_status = globvar.hex_brd.place_chess(self.pos_on_board)
                            if chess_status == False and not self.on_button[0]:
                                # if user tring place on non empty cell
                                self.show_message('please place chess on empty position')
                            else:
                                # keep placed info, and check winner
                                globvar.hex_brd.notify_update(self.mouse_pos, self.text)
                                win_color,winner_num = self.win_color()
                                if win_color != "":
                                    # there is a winner
                                    print("winner is", win_color)
                                    globvar.hex_ctrl.show_message('Player '+win_color+ ' has won')
                                    # self.board = self.init_board()
                                    win_path = globvar.hex_brd.winning_path(globvar.hex_brd.board, winner_num)
                                    print("winning path is:", win_path, "\n")
                                    globvar.hex_brd.win_path = win_path
                                elif globvar.hex_brd.current_mode == 1:  # AI player mode
                                    self.run_thread()
                                    win_color,winner_num = self.win_color()
                                    if win_color != "":
                                        # if there is a winner
                                        print("winner is", win_color)
                                        globvar.hex_ctrl.show_message('Player '+ win_color + ' has won')
                                        print("winner_num ",winner_num)
                                        win_path = globvar.hex_brd.winning_path(globvar.hex_brd.board, winner_num)
                                        print("winning path is:", win_path, "\n")
                                        globvar.hex_brd.win_path = win_path
                        else:
                            # if someone won, user trying place..
                            self.show_message( 'Player ' + win_color + ' has won')
                    elif not self.on_button[0]:
                        if globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
                            self.show_message('Do not place chess out of board')
                    if self.on_button[0]:
                        button = self.buttons[self.on_button[1].split(':')[0]]
                        if self.menu:
                            if not self.press_button(button):  # return False if quit button is pressed
                                return False
                            if self.menu:
                                globvar.menu.draw_menu(self.mouse_pos)
                        else:
                            #button = self.buttons[self.on_button[1]]
                            if not self.press_button(button):  # return False if quit button is pressed
                                return False
                            if not self.menu:
                                globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == self.STOPMSG:
                pygame.time.set_timer(self.STOPMSG, 0)
                self.print_message = False
                self.text = None
                globvar.hex_brd.notify_update(self.mouse_pos, self.text)

        return True

    def win_color(self):
        '''
        This function  will check win color, according to the winer number,
        return winner's color 
        '''
        win_color = ""
        winner_num = globvar.hex_brd.get_winner(globvar.hex_brd.board)
        if (winner_num) == 1:
            win_color = "blue"
        elif winner_num == 0:
            win_color = "red"
        return win_color, winner_num

    def show_message(self, text):
        '''
        This function  will call model to update, and message will lasting for a while
        arguement text is the message want to be showed
        '''
        # design for show message
        self.print_message = True
        self.text = text
        pygame.time.set_timer(self.STOPMSG, 1000)
        globvar.hex_brd.notify_update(self.mouse_pos, text)

    def press_button(self, button):
        '''
        This function will handle the procedure of pressing a button.
        
        return True if not the quit button is pressed
               False if quit button is pressed
        '''
        if button == 0:  # new game button
            globvar.hex_brd.new_game()
        elif button == 1:  # menu button
            self.menu = True
            globvar.menu.draw_menu(self.mouse_pos)
        elif button == 2:  # REAL PLAYER / AI PLAYER mode button
            globvar.hex_brd.switch_mode()
        elif button == 3:  # undo button
            if globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
                globvar.hex_brd.undo()
            else:
                self.show_message('Cannot Undo, Player'+str(globvar.hex_brd.get_winner(globvar.hex_brd.board)+1) +
                                  ' has won')
        elif button == 4:  # LEVEL  (EASY / HARD) button
            globvar.menu.level = (globvar.menu.level + 1) % 2
            if globvar.menu.level == 0:
                globvar.hex_brd.waiting_time = 1
            else:
                globvar.hex_brd.waiting_time = 20
        elif button == 5:  # SIZE (board size: 5x5 / 6x6) button
            globvar.hex_brd.size = (5, 5) if globvar.hex_brd.size == (6, 6) else (6, 6)
            globvar.hex_brd.new_game()
            globvar.hex_brd.dump_Monte_Carlo_obj()
            globvar.hex_brd.load_Monte_Carlo_Obj()
        elif button == 6:  # START (new game) button
            self.menu = False
            globvar.hex_brd.new_game()
            globvar.hex_brd.notify_update(self.mouse_pos, self.text)
        elif button == 7:  # CONTINUE (previous game) button
            self.menu = False
            globvar.hex_brd.notify_update(self.mouse_pos, self.text)
        elif button == 8:  # SIMULATION button
            self.show_win_p = not self.show_win_p
            globvar.hex_brd.monte_carlo.activate = not globvar.hex_brd.monte_carlo.activate
            globvar.hex_brd.current_show = (globvar.hex_brd.current_show + 1) % 2
        else:  # QUIT button
            return False
        return True

    def run_thread(self):
        '''
        This function will run two thread:
            Thread 1: Monte Carlo algorithm move generation process
            Thread 2: Count down message display
        to avoid having the user stuck in the middle of the program without knowing
        what is going on.
        '''
        # https://realpython.com/intro-to-python-threading/
        gen_move = threading.Thread(target=self.move_thread_function, args=(1,))
        print_loading = threading.Thread(target=self.print_thread_function, args=(2,))
        print_loading.start()
        gen_move.start()
        print_loading.join()
        gen_move.join()
        pygame.event.clear()

    def move_thread_function(self, name):
        '''
        This function is the process of the first thread. It will call the move function to
        generate a move for the current board using Monte Carlo algorithm.
        '''
        print("generating next move ...")
        globvar.hex_brd.move()
        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
        print("done\n")

    def print_thread_function(self, name):
        '''
        This functino is the process of the second thread. It will show the
        count down message:  loading ... X sec
        where X is the number of seconds left for waiting. The waiting time depends on
        the current level (1 sec if in EASY mode, 3 sec if in HARD mode).
        '''
        waiting_time = globvar.hex_brd.waiting_time - 1
        while waiting_time > 0:
            self.show_message("loading . . . " + str(waiting_time) + "s")
            time.sleep(1)
            waiting_time -= 1

