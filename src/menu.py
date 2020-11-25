import pygame
import globvar

class Menu():

	def __init__(self, screen, bgr_color):
		self.screen = screen
		self.bgr_color = bgr_color
		self.size = screen.get_size()
		self.brd_size = globvar.hex_brd.size
		self.level = 0
		self.boardsize_button = pygame.Rect(self.size[0] * 1 / 2 - 150/2, self.size[1] * 1 / 7, 150, 50)
		self.levels_button = pygame.Rect(self.size[0] * 1 / 2 - 150/2, self.size[1] * 2 / 7, 150, 50)
		self.start_button = pygame.Rect(self.size[0] * 1 / 2 - 150/2, self.size[1] * 3 / 7, 150, 50)
		self.cont_button = pygame.Rect(self.size[0] * 1 / 2 - 150/2, self.size[1] * 4 / 7, 150, 50)
		self.quit_button = pygame.Rect(self.size[0] * 1 / 2 - 150/2, self.size[1] * 5 / 7, 150, 50)

	def draw_menu(self, mouse_pos):
		# Fill the background with white
		self.screen.fill(self.bgr_color)
		globvar.hex_ctrl.on_button = (False, None)
		self.draw_level(mouse_pos)
		self.draw_board_size(mouse_pos)
		self.draw_button(mouse_pos, self.start_button, "start".upper())
		if len(globvar.hex_brd.history) > 0:
			self.draw_button(mouse_pos, self.cont_button, "continue".upper())
		self.draw_button(mouse_pos, self.quit_button, "quit".upper())

	def draw_level(self, mouse_pos):
		level = "easy" if self.level == 0 else "hard"
		text = "level: " + str(level)
		self.draw_button(mouse_pos, self.levels_button, text.upper())

	def draw_board_size(self, mouse_pos):
		current_brd_size = globvar.hex_brd.size
		text = "size: " + str(current_brd_size[0]) + " x " + str(current_brd_size[1])
		self.draw_button(mouse_pos, self.boardsize_button, text.upper())

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
