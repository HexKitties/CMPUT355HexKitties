import pygame
from math import cos, sin
import globvar

class HexView():
    def __init__(self, screen, bgr_color):
        self.screen = screen
        self.bgr_color = bgr_color

    # https://stackoverflow.com/questions/29064259/drawing-pentagon-hexagon-in-pygame
    def draw_ngon(self, radius, color, n, position):
        pi2 = 2 * 3.14
        return pygame.draw.lines(self.screen,
              color,
              True,
              [(sin(i / n * pi2) * radius + position[0], cos(i / n * pi2) * radius + position[1]) for i in range(0, n)], 5)

    def draw_circle(self, radius, pos, is_chess):
        temp = pos
        temp_rad = int(radius * 0.6)
        if is_chess:
            pygame.draw.circle(self.screen, (0, 0, 255), temp, temp_rad)
        else:
        	pygame.draw.circle(self.screen, (0, 0, 255), temp, temp_rad, 3)

    def check_mouse(self, radius, mouse_pos, center_pos):
    	return (mouse_pos[0]-center_pos[0])**2 + (mouse_pos[1] - center_pos[1])**2 < (radius * 0.8)**2

    def draw_board(self, radius, size, default_color, chess_pos, pos, mouse_pos):
    	# Fill the background with white
        self.screen.fill(self.bgr_color)

        for i in range(size[0]):
            for j in range(size[1]):
                color = default_color
                temp_pos = (int(pos[0] + j * 2 * sin((120 / 180) * 3.14) * radius), pos[1])
                
                # check mouse pos in hex grid
                if chess_pos[i][j] != 0:
                    self.draw_circle(radius, temp_pos, True)
                if self.check_mouse(radius, mouse_pos, temp_pos):
                    self.draw_circle(radius, temp_pos, False)
                    globvar.hex_ctrl.pos_on_board = (i, j)
                if (i == 0 and j == 0) or (i == size[0] - 1 and j == size[1] - 1) \
                    or (i == 0 and j == size[1] - 1) or (i == size[0] - 1 and j == 0):
                	color = (0, 0, 0)
                elif i == 0 or i == size[0] - 1:
                    color = (255, 0, 0)
                elif j == 0 or j == size[1] - 1:
                    color = (0, 0, 255)  # blue
                self.draw_ngon(radius, color, 6, temp_pos)

            d_x = sin((60 / 180) * 3.14) * radius
            d_y = cos((60 / 180) * 3.14) * radius + radius
            pos = (int(pos[0] + d_x),\
             int(pos[1] + d_y))

    def get_pos(self, radius, size, pos, mouse_pos):
        for i in range(size[0]):
            for j in range(size[1]):
                temp_pos = (pos[0], int(pos[1] + j * 2 * sin((120 / 180) * 3.14) * radius))
                if self.check_mouse(radius, mouse_pos, temp_pos):
                    return (i, j)
            d_x = sin((60 / 180) * 3.14) * radius
            d_y = cos((60 / 180) * 3.14) * radius + radius
            pos = (int(pos[0] + d_y),\
             int(pos[1] + d_x))

