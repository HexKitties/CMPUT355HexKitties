import pygame
import globvar

class HexController():
    def __init__(self):
        self.mouse_pos = (-1, -1)
        self.pos_on_board = None
        self.on_button = (False, None)
        self.buttons = {"newgame": 0, "exit": 1, "playermode": 2, "undo": 3}

    def interaction(self):
    	# Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                globvar.hex_brd.notify_update(self.mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:

                    if self.pos_on_board != None:
                        chess_status = globvar.hex_brd.place_chess(self.pos_on_board)
                        globvar.hex_brd.notify_update(self.mouse_pos)
                        if chess_status == False:
                            self.wrong_chess('please place chess on empty position')
                            pass
                    elif (self.pos_on_board) == None:
                        self.wrong_chess('Do not place chess out of board ')
                    if self.on_button[0]:
                        button = self.buttons[self.on_button[1]]
                        if not self.press_button(button):
                            return False
                        globvar.hex_brd.notify_update(self.mouse_pos)
                    
        return True

    def wrong_chess(self,text):

        # if (self.pos_on_board) == None:
            # print("haha")
        globvar.hex_brd.notify_wrongly(text)


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