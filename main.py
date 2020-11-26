# Import and initialize the pygame library
import pygame
import pickle
import time
from model import HexModel
from controller import HexController
from view import HexView
import globvar
import monte_carlo

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 800])
pygame.display.flip()
globvar.init()

for i in range(20):
    MonteCarlo_in = open('MonteCarlo(6, 6)', "rb+")
    a = pickle.load(MonteCarlo_in)
    b = pickle.load(MonteCarlo_in)
    MonteCarlo_in.close()

    globvar.hex_brd = HexModel(a, b)
    globvar.hex_ctrl = HexController()
    wood = (193, 154, 107)
    grey = (200, 200, 200)
    globvar.hex_view = HexView(screen, grey)
    while globvar.hex_brd.get_winner(globvar.hex_brd.board) == 2:
        globvar.hex_brd.move()

    # Run until the user asks to quit

    # Done! Time to quit.

    MonteCarlo_out = open("MonteCarlo(6, 6)", "wb")
    pickle.dump(a, MonteCarlo_out)
    pickle.dump(b, MonteCarlo_out)
    MonteCarlo_out.close()


running = True
while running:
    running = globvar.hex_ctrl.interaction()
    # Flip the display
    pygame.display.flip()

pygame.quit()
