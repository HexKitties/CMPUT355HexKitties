import pygame
import globvar
import monte_carlo


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
                # globvar.hex_brd.dump_Monte_Carlo_obj()
                return False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:

                    if self.pos_on_board != None:
                        chess_status = globvar.hex_brd.place_chess(self.pos_on_board)
                        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
                        if globvar.hex_brd.current_mode == 1:
                            globvar.hex_brd.move()
                        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
                        if chess_status == False and not self.on_button[0]:
                            self.show_message('please place chess on empty position')
                            pass
                    elif not self.on_button[0]:
                        self.show_message('Do not place chess out of board')
                    if self.on_button[0]:
                        button = self.buttons[self.on_button[1]]
                        if not self.press_button(button):
                            return False
                        globvar.hex_brd.notify_update(self.mouse_pos, self.text)
            if event.type == self.STOPMSG:
                pygame.time.set_timer(self.STOPMSG, 0)
                self.print_message = False
                self.text = None

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
        elif button == 1:
            return False
        elif button == 2:
            globvar.hex_brd.switch_mode()
        elif button == 3:
            globvar.hex_brd.undo()
        return True

