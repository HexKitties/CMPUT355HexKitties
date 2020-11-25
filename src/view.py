import pygame
from math import cos, sin
import globvar
import copy

class HexView():
    def __init__(self, screen, bgr_color, start_pos = (120, 120)):
        self.screen = screen
        self.bgr_color = bgr_color
        self.start_pos = start_pos
        self.size = screen.get_size()
        self.newgame_button = pygame.Rect(self.size[0] * 1 / 6, self.size[1] * 4 / 5, 150, 50)
        self.playermode_button = pygame.Rect(self.size[0] * 2 / 6, self.size[1] * 4 / 5, 150, 50)
        self.undo_button = pygame.Rect(self.size[0] * 3 / 6, self.size[1] * 4 / 5, 150, 50)
        self.menu_button = pygame.Rect(self.size[0] * 4 / 6, self.size[1] * 4 / 5, 150, 50)

    # https://stackoverflow.com/questions/29064259/drawing-pentagon-hexagon-in-pygame
    def draw_ngon(self, radius, color, n, position):
        pi2 = 2 * 3.14
        return pygame.draw.lines(self.screen,
              color,
              True,
              [(sin(i / n * pi2) * radius + position[0], cos(i / n * pi2) * radius + position[1]) for i in range(0, n)], 5)

    def draw_circle(self, radius, pos, color, is_chess):
        c_rad = int(radius * 0.6)
        if is_chess:
            pygame.draw.circle(self.screen, color, pos, c_rad)
        else:
        	pygame.draw.circle(self.screen, color, pos, c_rad, 3)

    def draw_wining_circle(self, radius, pos, is_chess):
        c_rad = int(radius * 0.2)
        pygame.draw.circle(self.screen, (192, 192, 192), pos, c_rad)
        # else:
        #     pygame.draw.circle(self.screen, color, pos, c_rad, 3)

    def draw_buttons(self, mouse_pos):
        globvar.hex_ctrl.on_button = (False, None)
        self.draw_button(mouse_pos, self.newgame_button, "newgame")
        self.draw_button(mouse_pos, self.menu_button, "menu")
        self.draw_button(mouse_pos, self.playermode_button, globvar.hex_brd.modes[globvar.hex_brd.current_mode])
        self.draw_button(mouse_pos, self.undo_button, "undo")

    def draw_button(self, mouse_pos, button, text):
        purple = (128, 0, 128)
        blue = (36, 160, 237)
        if button.collidepoint(mouse_pos):
            globvar.hex_ctrl.on_button = (True, text)
            pygame.draw.rect(self.screen, purple, button)
        else:
            pygame.draw.rect(self.screen, blue, button)

        smallText = pygame.font.SysFont("comicsansms", 20)
        text = smallText.render(text.upper(), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = button.center
        self.screen.blit(text, textRect)

    def check_mouse(self, radius, mouse_pos, center_pos):
    	return (mouse_pos[0]-center_pos[0])**2 + (mouse_pos[1] - center_pos[1])**2 < (radius * 0.8)**2

    def display(self, radius, size, default_color, chess_pos, mouse_pos, text):
        # Fill the background with white
        self.screen.fill(self.bgr_color)

        if globvar.hex_ctrl.print_message:
            self.draw_notify(text)
            return
    	
        self.draw_buttons(mouse_pos)
        
        pos = self.start_pos
        in_brd = False

        # sorted win path save time
        current_win_path = copy.deepcopy(globvar.hex_brd.win_path)
        current_win_path.sort()

        for i in range(size[0]):
            for j in range(size[1]):
                box_color = default_color
                temp_pos = (int(pos[0] + j * 2 * sin((120 / 180) * 3.14) * radius), pos[1])
                if chess_pos[i][j] != -1:
                    chess_color = globvar.hex_brd.players[chess_pos[i][j]]
                    self.draw_circle(radius, temp_pos, chess_color, True)

                    if  len(current_win_path) > 0 and (i,j) == current_win_path[0]:
                        self.draw_wining_circle(radius, temp_pos, True )
                        current_win_path.pop(0)
                if self.check_mouse(radius, mouse_pos, temp_pos):
                    in_brd = True
                    if chess_pos[i][j] == -1:
                        chess_color = globvar.hex_brd.players[globvar.hex_brd.player_turn]
                        self.draw_circle(radius, temp_pos, chess_color, False)
                    globvar.hex_ctrl.pos_on_board = (i, j)
                if (i == 0 and j == 0) or (i == size[0] - 1 and j == size[1] - 1) \
                    or (i == 0 and j == size[1] - 1) or (i == size[0] - 1 and j == 0):
                	box_color = (0, 0, 0)
                elif i == 0 or i == size[0] - 1:
                    box_color = globvar.hex_brd.players[0]
                elif j == 0 or j == size[1] - 1:
                    box_color = globvar.hex_brd.players[1]
                self.draw_ngon(radius, box_color, 6, temp_pos)

            d_x = sin((60 / 180) * 3.14) * radius
            d_y = cos((60 / 180) * 3.14) * radius + radius
            pos = (int(pos[0] + d_x),\
             int(pos[1] + d_y))

        if not in_brd:
        	globvar.hex_ctrl.pos_on_board = None

    def draw_notify(self,text):
        # pygame.font.init() # you have to call this at the start,
        #            # if you want to use this module.
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.size[0]/2),(self.size[1]/2))
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

