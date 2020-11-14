import pygame
from math import cos, sin
import globvar

class HexView():
    def __init__(self, screen, bgr_color, start_pos = (120, 120)):
        self.screen = screen
        self.bgr_color = bgr_color
        self.start_pos = start_pos
        self.size = screen.get_size()
        self.undo_button = pygame.Rect(self.size[0] * 4 / 5, self.size[1] * 4 / 5, 150, 50)

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

    def draw_button(self, mouse_pos):
        purple = (128, 0, 128)
        blue = (36, 160, 237)
        if self.undo_button.collidepoint(mouse_pos):
            globvar.hex_ctrl.on_button = True
            pygame.draw.rect(self.screen, purple, self.undo_button)
        else:
            globvar.hex_ctrl.on_button = False
            pygame.draw.rect(self.screen, blue, self.undo_button)

        smallText = pygame.font.SysFont("comicsansms", 20)
        text = smallText.render("undo", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = self.undo_button.center
        self.screen.blit(text, textRect)

    def check_mouse(self, radius, mouse_pos, center_pos):
    	return (mouse_pos[0]-center_pos[0])**2 + (mouse_pos[1] - center_pos[1])**2 < (radius * 0.8)**2

    def display(self, radius, size, default_color, chess_pos, mouse_pos):
    	# Fill the background with white
        self.screen.fill(self.bgr_color)
        self.draw_button(mouse_pos)
        pos = self.start_pos
        in_brd = False

        for i in range(size[0]):
            for j in range(size[1]):
                box_color = default_color
                temp_pos = (int(pos[0] + j * 2 * sin((120 / 180) * 3.14) * radius), pos[1])

                if chess_pos[i][j] != -1:
                    chess_color = globvar.hex_brd.players[chess_pos[i][j]]
                    self.draw_circle(radius, temp_pos, chess_color, True)
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
                    box_color = (255, 0, 0)
                elif j == 0 or j == size[1] - 1:
                    box_color = (0, 0, 255)  # blue
                self.draw_ngon(radius, box_color, 6, temp_pos)

            d_x = sin((60 / 180) * 3.14) * radius
            d_y = cos((60 / 180) * 3.14) * radius + radius
            pos = (int(pos[0] + d_x),\
             int(pos[1] + d_y))

        if not in_brd:
        	globvar.hex_ctrl.pos_on_board = None

    # def get_pos(self, radius, size, pos, mouse_pos):
    #     for i in range(size[0]):
    #         for j in range(size[1]):
    #             temp_pos = (pos[0], int(pos[1] + j * 2 * sin((120 / 180) * 3.14) * radius))
    #             if self.check_mouse(radius, mouse_pos, temp_pos):
    #                 return (i, j)
    #         d_x = sin((60 / 180) * 3.14) * radius
    #         d_y = cos((60 / 180) * 3.14) * radius + radius
    #         pos = (int(pos[0] + d_y),\
    #          int(pos[1] + d_x))

