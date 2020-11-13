# Import and initialize the pygame library
import pygame
from hexboard import HexBoard

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 800])

brd = HexBoard(screen, (120, 102))
mouse_pos = (0, 0)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
            	brd.place_chess()

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw hex board
    brd.draw_board(mouse_pos)
        

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

