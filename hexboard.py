import pygame
from math import cos, sin
class HexBoard():
    def __init__(self, screen, start_pos, radius=50, size=(5, 5), color=(0, 0, 0)):
        self.screen = screen
        self.radius = radius
        self.size = size
        self.default_color = color
        self.start_pos = start_pos
        self.chess_pos = self.init_board()
        self.history = []
        self.current_mouse = None

    def init_board(self):
    	empty_brd = []
    	for i in range(self.size[0]):
    		temp = []
    		for i in range(self.size[1]):
    			temp.append(0)
    		empty_brd.append(temp)
    	return empty_brd

    # https://stackoverflow.com/questions/29064259/drawing-pentagon-hexagon-in-pygame
    def draw_ngon(self, color, n, position):
        pi2 = 2 * 3.14
        return pygame.draw.lines(self.screen,
              color,
              True,
              [(sin(i / n * pi2) * self.radius + position[1], cos(i / n * pi2) * self.radius + position[0]) for i in range(0, n)])

    def draw_circle(self, pos, is_chess):
        temp = (pos[1], pos[0])
        temp_rad = int(self.radius * 0.5)
        if is_chess:
            pygame.draw.circle(self.screen, (0, 0, 255), temp, temp_rad)
        else:
        	pygame.draw.circle(self.screen, (0, 0, 255), temp, temp_rad, 3)

    def check_mouse(self, mouse_pos, center_pos):
    	return (mouse_pos[0]-center_pos[1])**2 + (mouse_pos[1] - center_pos[0])**2 < (self.radius * 0.8)**2

    def place_chess(self):
        if self.chess_pos[self.current_mouse[0]][self.current_mouse[1]] == 0:
            self.chess_pos[self.current_mouse[0]][self.current_mouse[1]] = 1
            self.history.append(self.current_mouse)
            print(self.history)
            return True
        return False

    def draw_board(self, mouse_pos):
        pos = self.start_pos

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                temp_pos = (pos[0], int(pos[1] + j * 2 * sin((120 / 180) * 3.14) * self.radius))
                color = self.default_color
                # check mouse pos in hex grid
                if self.chess_pos[i][j] != 0:
                	self.draw_circle(temp_pos, True)
                if self.check_mouse(mouse_pos, temp_pos):
                	self.draw_circle(temp_pos, False)
                	self.current_mouse = (i, j)
                self.draw_ngon(color, 6, temp_pos)

            pos = (int(pos[0] + cos((60 / 180) * 3.14) * self.radius + self.radius),\
             int(pos[1] + sin((60 / 180) * 3.14) * self.radius))

