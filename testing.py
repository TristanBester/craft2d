import numpy as np
import pygame

pygame.init()
font = pygame.font.Font(None, 20)


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

N_ROWS = 10
N_COLS = 10

CELL_WIDTH = WINDOW_WIDTH / N_COLS
CELL_HEIGHT = WINDOW_HEIGHT / N_ROWS
CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)


# ### UI ###
# # screen size
# w = 320
# h = 240

# tile size

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)


# setup screen
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid World")

grass_image = pygame.transform.scale(pygame.image.load("grass.png"), CELL_SIZE)
tree_image = pygame.transform.scale(pygame.image.load("tree.png"), CELL_SIZE)

# setup timer
clock = pygame.time.Clock()
# tick
SPEED = 10

# agent position
x = 0
y = WINDOW_HEIGHT - CELL_HEIGHT

# game state
off_screen = False
arrived = False
score = 0

### Game Loop/Progress
# Run until the player quit
playing = True
while playing:
    # Player events: mouse click, keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        # get the player action
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= CELL_WIDTH
            elif event.key == pygame.K_RIGHT:
                x += CELL_WIDTH
            elif event.key == pygame.K_UP:
                y -= CELL_HEIGHT
            elif event.key == pygame.K_DOWN:
                y += CELL_HEIGHT

        # # move off the screen
        # if x < 0 or x > w - BLOCK_SIZE or y < 0 or y > h - BLOCK_SIZE:
        #     off_screen = True

        # # arrives the destination
        # if x ==  - BLOCK_SIZE and y == 0:
        #     arrived = True
        #     score = 100

    window.fill((0, 255, 0))

    for r in np.arange(0, N_ROWS * CELL_HEIGHT, CELL_HEIGHT):
        for c in np.arange(0, N_COLS * CELL_WIDTH, CELL_WIDTH):
            window.blit(grass_image, (c, r))

    # # Draw a agent in the left bottom, a target on the top right
    pygame.draw.rect(window, RED, pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT))
    # pygame.draw.rect(
    #     screen, BLUE, pygame.Rect(w - BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE)
    # )

    # screen.blit(grass_image, (0, 0))
    window.blit(tree_image, (0, 0))

    # display the score
    text = font.render("Score: " + str(score), True, BLACK)
    window.blit(text, [0, 0])

    # Flip the display
    pygame.display.flip()
    clock.tick(SPEED)

    # if off_screen == True or arrived == True:
    #     break

pygame.quit()
