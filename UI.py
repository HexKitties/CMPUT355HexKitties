# Import and initialize the pygame library
import pygame

from model import HexModel
from controller import HexController
from view import HexView
import globvar

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 800])

globvar.init()
globvar.hex_brd = HexModel()
globvar.hex_ctrl = HexController()
globvar.hex_view = HexView(screen, (232, 235, 239))

# Run until the user asks to quit
running = True
while running:
    running = globvar.hex_ctrl.interaction()
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

