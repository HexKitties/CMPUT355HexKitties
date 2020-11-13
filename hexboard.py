import pygame
from math import cos, sin
class HexBoard():
    def __init__(self, screen, start_pos, radius=40, size=(8, 8), color=(128,128,128)):
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
              [(sin(i / n * pi2) * self.radius + position[1], cos(i / n * pi2) * self.radius + position[0]) for i in range(0, n)], 5)

    def draw_circle(self, pos, is_chess):
        temp = (pos[1], pos[0])
        temp_rad = int(self.radius * 0.6)
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

    # def draw_base(self):
    #     d_x = sin((60 / 180) * 3.14) * self.radius
    #     d_y = cos((60 / 180) * 3.14) * self.radius + self.radius
    #     p1 = (self.start_pos[0] - 2 * self.radius - d_x, self.start_pos[1] - d_y)
    #     p2 = (self.start_pos[0] + self.size[1] * 2 * d_x - d_x, self.start_pos[1] - d_y)
    #     p3 = (self.start_pos[0] + self.size[0] * d_x - 2 * self.radius, self.start_pos[1] + self.size[0] * d_y)
    #     p4 = (self.start_pos[0] + self.size[0] * d_x + self.size[1] * 2 * d_x, self.start_pos[1] + self.size[0] * d_y)
    #     points = [p1, p2]
    #     pygame.draw.lines(self.screen, (255, 0, 0), True, points, 3)
    #     points = [p3, p4]
    #     pygame.draw.lines(self.screen, (255, 0, 0), True, points, 3)

    #     points = [p1, p3]
    #     pygame.draw.lines(self.screen, (0, 0, 255), True, points, 3)
    #     points = [p2, p4]
    #     pygame.draw.lines(self.screen, (0, 0, 255), True, points, 3)

    def draw_board(self, mouse_pos):
        pos = self.start_pos
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                color = self.default_color
                temp_pos = (pos[0], int(pos[1] + j * 2 * sin((120 / 180) * 3.14) * self.radius))
                
                # check mouse pos in hex grid
                if self.chess_pos[i][j] != 0:
                    self.draw_circle(temp_pos, True)
                if self.check_mouse(mouse_pos, temp_pos):
                    self.draw_circle(temp_pos, False)
                    self.current_mouse = (i, j)
                if (i == 0 and j == 0) or (i == self.size[0] - 1 and j == self.size[1] - 1) \
                    or (i == 0 and j == self.size[1] - 1) or (i == self.size[0] - 1 and j == 0):
                	color = (0, 0, 0)
                elif i == 0 or i == self.size[0] - 1:
                    color = (255, 0, 0)
                elif j == 0 or j == self.size[1] - 1:
                    color = (0, 0, 255)  # blue
                self.draw_ngon(color, 6, temp_pos)

            d_x = sin((60 / 180) * 3.14) * self.radius
            d_y = cos((60 / 180) * 3.14) * self.radius + self.radius
            pos = (int(pos[0] + d_y),\
             int(pos[1] + d_x))

