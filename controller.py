import pygame
import globvar

class HexController():
    def __init__(self):
        self.mouse_pos = (-1, -1)
        self.pos_on_board = None

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
                        globvar.hex_brd.place_chess(self.pos_on_board)
                        globvar.hex_brd.notify_update(self.mouse_pos)
        return True