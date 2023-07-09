import time

import numpy as np
import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Craft2D"


class Environment:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    USE = 4

    def __init__(self):
        self.n_rows = 10
        self.n_cols = 10
        # tree - 0, stone - 1, grass - 2
        self.n_objects = 3

        self.grid = np.zeros((self.n_rows, self.n_cols, self.n_objects))

        # pygame utils
        self.window = None
        self.clock = None
        self.cell_size = (
            WINDOW_WIDTH / self.n_cols,
            WINDOW_HEIGHT / self.n_rows,
        )
        self.background_image = None
        self.player_image = None
        self.tree_image = None
        self.stone_image = None
        self.grass_image = None

    def _generate_positions(self):
        row = np.random.randint(0, self.n_rows)
        col = np.random.randint(0, self.n_cols)
        return row, col

    def reset(self):
        used_positions = []

        for i in range(self.n_objects):
            row, col = self._generate_positions()
            while (row, col) in used_positions:
                row, col = self._generate_positions()
            used_positions.append((row, col))
            self.grid[row, col, i] = 1

        self.agent_position = (0, 0)
        self.direction = np.zeros((4,))

    def _update_agent_position(self, action):
        row, col = self.agent_position

        if action == self.RIGHT:
            n_row = row
            n_col = col + 1 if col + 1 < self.n_cols else col
        elif action == self.LEFT:
            n_row = row
            n_col = col - 1 if col - 1 >= 0 else col
        elif action == self.UP:
            n_row = row - 1 if row - 1 >= 0 else row
            n_col = col
        elif action == self.DOWN:
            n_row = row + 1 if row + 1 < self.n_rows else row
            n_col = col

        self.agent_position = (n_row, n_col)

    def _update_agent_direction(self, action):
        self.direction = np.zeros((4,))

        if action == self.RIGHT:
            self.direction[0] = 1
        elif action == self.LEFT:
            self.direction[1] = 1
        elif action == self.UP:
            self.direction[2] = 1
        elif action == self.DOWN:
            self.direction[3] = 1

    def step(self, action):
        self.last_position = self.agent_position
        self._update_agent_position(action)
        self._update_agent_direction(action)

    def render(self):
        if self.window is None:
            pygame.init()
            pygame.display.set_caption(WINDOW_TITLE)
            self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        if self.clock is None:
            self.clock = pygame.time.Clock()
        if self.background_image is None:
            self.background_image = pygame.transform.scale(
                pygame.image.load("resources/terrain/grass.png"),
                self.cell_size,
            )
        if self.player_image is None:
            self.player_images = []
            self.player_images.append(
                pygame.transform.scale(
                    pygame.image.load("resources/agent/agent-right.png"),
                    self.cell_size,
                )
            )
            self.player_images.append(
                pygame.transform.scale(
                    pygame.image.load("resources/agent/agent-left.png"),
                    self.cell_size,
                )
            )
            self.player_images.append(
                pygame.transform.scale(
                    pygame.image.load("resources/agent/agent-up.png"),
                    self.cell_size,
                )
            )
            self.player_images.append(
                pygame.transform.scale(
                    pygame.image.load("resources/agent/agent-down.png"),
                    self.cell_size,
                )
            )
        if self.tree_image is None:
            self.tree_image = pygame.transform.scale(
                pygame.image.load("resources/objects/tree.png"),
                self.cell_size,
            )
        if self.stone_image is None:
            self.stone_image = pygame.transform.scale(
                pygame.image.load("resources/objects/stone.png"),
                self.cell_size,
            )
        if self.grass_image is None:
            self.grass_image = pygame.transform.scale(
                pygame.image.load("resources/objects/grass.png"),
                self.cell_size,
            )

        for row in range(self.n_rows):
            for col in range(self.n_cols):
                self.window.blit(
                    self.background_image,
                    (
                        col * self.cell_size[0],
                        row * self.cell_size[1],
                    ),
                )

                # Empty cell
                if np.max(self.grid[row, col]) == 0:
                    continue
                else:
                    # Use helper funnctions though to draw
                    if self.grid[row, col, 0] == 1:
                        self.window.blit(
                            self.tree_image,
                            (
                                col * self.cell_size[0],
                                row * self.cell_size[1],
                            ),
                        )
                    elif self.grid[row, col, 1] == 1:
                        self.window.blit(
                            self.stone_image,
                            (
                                col * self.cell_size[0],
                                row * self.cell_size[1],
                            ),
                        )
                    elif self.grid[row, col, 2] == 1:
                        self.window.blit(
                            self.grass_image,
                            (
                                col * self.cell_size[0],
                                row * self.cell_size[1],
                            ),
                        )

        self.window.blit(
            self.player_images[np.argmax(self.direction)],
            (
                self.agent_position[1] * self.cell_size[0],
                self.agent_position[0] * self.cell_size[1],
            ),
        )

        # self.window.fill((0, 0, 0))

        # self.clock.tick(self.metadata["render_fps"])
        self.clock.tick(60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    env = Environment()
    env.reset()

    while True:
        a = np.random.choice([0, 1, 2, 3])
        a = int(input())
        env.step(a)

        env.render()

        # print(a)

    # pygame.init()
    # screen = pygame.display.set_mode((400, 300))
    # done = False

    # # main loop
    # while not done:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done = True

    #     # INDENTATION

    #     # <--|
    #     pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))

    #     # -->|
    #     pygame.display.flip()
