import time
from itertools import product

import numpy as np
import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Craft2D"

PLAYER_IMGS_PATH = [
    "resources/agent/agent-right.png",
    "resources/agent/agent-left.png",
    "resources/agent/agent-up.png",
    "resources/agent/agent-down.png",
]
BACKGROUND_IMG_PATH = "resources/terrain/grass.png"
TREE_IMG_PATH = "resources/objects/tree.png"
WOOD_IMG_PATH = "resources/objects/wood.png"
STONE_IMG_PATH = "resources/objects/stone.png"
GRASS_IMG_PATH = "resources/objects/grass.png"
CRAFTING_TABLE_IMG_PATH = "resources/objects/crafting-table.png"
STICKS_IMG_PATH = "resources/objects/sticks.png"
ROPE_IMG_PATH = "resources/objects/rope.png"
BRIDGE_IMG_PATH = "resources/objects/bridge.png"
WEAPON_BASIC_IMG_PATH = "resources/objects/weapon-basic.png"


class Renderer:
    def __init__(self, n_rows, n_cols, env_objects, inv_objects):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.env_objects = env_objects
        self.inv_objects = inv_objects

        self.cell_size = (
            WINDOW_WIDTH / (self.n_cols + 2),  # +2 for inventory
            WINDOW_HEIGHT / self.n_rows,
        )

        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()

        self.background_image = self._load_image(BACKGROUND_IMG_PATH)
        self.player_images = self._load_images(PLAYER_IMGS_PATH)
        self.tree_image = self._load_image(TREE_IMG_PATH)
        self.wood_image = self._load_image(WOOD_IMG_PATH)
        self.stone_image = self._load_image(STONE_IMG_PATH)
        self.grass_image = self._load_image(GRASS_IMG_PATH)
        self.crafting_table_image = self._load_image(CRAFTING_TABLE_IMG_PATH)
        self.sticks_image = self._load_image(STICKS_IMG_PATH)
        self.rope_image = self._load_image(ROPE_IMG_PATH)
        self.bridge_image = self._load_image(BRIDGE_IMG_PATH)
        self.weapon_basic_image = self._load_image(WEAPON_BASIC_IMG_PATH)

    def render(self, grid, inventory, agent_position, direction):
        self.window.fill((0, 0, 0))
        self._render_background()
        self._render_env_objects(grid)
        self._render_player(agent_position, direction)
        self._render_inventory(inventory)
        self._handle_events()

    def _render_background(self):
        for r, c in product(range(self.n_rows), range(self.n_cols)):
            self._render_cell(self.background_image, r, c)

    def _render_env_objects(self, grid):
        for r, c in product(range(self.n_rows), range(self.n_cols)):
            if np.max(grid[r, c]) == 0:
                # Environmet cell is empty
                continue

            object_type = np.argmax(grid[r, c])
            object_name = self.env_objects[object_type]

            if object_name == "tree":
                self._render_cell(self.tree_image, r, c)
            elif object_name == "stone":
                self._render_cell(self.stone_image, r, c)
            elif object_name == "grass":
                self._render_cell(self.grass_image, r, c)
            elif object_name == "crafting-table":
                self._render_cell(self.crafting_table_image, r, c)

    def _render_player(self, agent_position, direction):
        self._render_cell(
            image=self.player_images[np.argmax(direction)],
            row=agent_position[0],
            col=agent_position[1],
        )

    def _render_inventory(self, inventory):
        for idx, count in enumerate(inventory):
            object_name = self.inv_objects[idx]

            if object_name == "wood":
                self._render_cell(image=self.wood_image, row=idx, col=self.n_cols)
                self._render_text(text="Wood", row=idx, col=self.n_cols, loc="top")
            elif object_name == "stone":
                self._render_cell(image=self.stone_image, row=idx, col=self.n_cols)
                self._render_text(text="Stone", row=idx, col=self.n_cols, loc="top")
            elif object_name == "grass":
                self._render_cell(image=self.grass_image, row=idx, col=self.n_cols)
                self._render_text(text="Grass", row=idx, col=self.n_cols, loc="top")
            elif object_name == "sticks":
                self._render_cell(image=self.sticks_image, row=idx, col=self.n_cols)
                self._render_text(text="Sticks", row=idx, col=self.n_cols, loc="top")
            elif object_name == "rope":
                self._render_cell(image=self.rope_image, row=idx, col=self.n_cols)
                self._render_text(text="Rope", row=idx, col=self.n_cols, loc="top")
            elif object_name == "bridge":
                self._render_cell(image=self.bridge_image, row=idx, col=self.n_cols)
                self._render_text(text="Bridge", row=idx, col=self.n_cols, loc="top")
            elif object_name == "weapon-basic":
                self._render_cell(
                    image=self.weapon_basic_image, row=idx, col=self.n_cols
                )
                self._render_text(text="Weapon", row=idx, col=self.n_cols, loc="top")

            self._render_text(
                text="X " + str(int(count)), row=idx, col=self.n_cols + 1, size=20
            )

    def _handle_events(self):
        self.clock.tick(60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def _render_text(self, text, row, col, size=20, loc="center"):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, (255, 255, 255))

        if loc == "center":
            pos = (
                col * self.cell_size[0] + self.cell_size[0] / 2 - text.get_width() / 2,
                row * self.cell_size[1] + self.cell_size[1] / 2 - text.get_height() / 2,
            )
        elif loc == "top":
            pos = (
                col * self.cell_size[0] + self.cell_size[0] / 2 - text.get_width() / 2,
                row * self.cell_size[1],
            )

        self.window.blit(text, pos)

    def _render_cell(self, image, row, col):
        self.window.blit(
            image,
            (
                col * self.cell_size[0],
                row * self.cell_size[1],
            ),
        )

    def _load_image(self, path):
        return pygame.transform.scale(
            pygame.image.load(path),
            self.cell_size,
        )

    def _load_images(self, paths):
        images = []
        for path in paths:
            images.append(self._load_image(path))
        return images


class Environment:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    USE = 4

    RESOURCE_COUNTS = {
        "tree": 2,
        "stone": 1,
        "grass": 1,
    }
    ENVIRONMENT_OBJECTS = (
        "tree",
        "stone",
        "grass",
        "crafting-table",
    )
    INVENTORY_OBJECTS = (
        "wood",
        "stone",
        "grass",
        "sticks",
        "rope",
        "bridge",
        "weapon-basic",
    )

    def __init__(self):
        self.n_rows = 10
        self.n_cols = 10  # 2 extra columns for the inventory

        self.n_env_objects = len(self.ENVIRONMENT_OBJECTS)
        self.n_inv_objects = len(self.INVENTORY_OBJECTS)

        # Object order specified in ENVIRONMENT_OBJECTS
        self.grid = np.zeros((self.n_rows, self.n_cols, self.n_env_objects))
        # Object order specified in INVENTORY_OBJECTS
        self.inventory = np.zeros((self.n_inv_objects,))

        self.renderer = Renderer(
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            env_objects=self.ENVIRONMENT_OBJECTS,
            inv_objects=self.INVENTORY_OBJECTS,
        )

    def _generate_positions(self):
        row = np.random.randint(0, self.n_rows - 1)
        col = np.random.randint(0, self.n_cols - 1)
        return row, col

    def reset(self):
        # Agent position occupied
        used_positions = [(0, 0)]

        for i, object_name in enumerate(self.ENVIRONMENT_OBJECTS):
            # Determine how many of each object to place
            if object_name in self.RESOURCE_COUNTS:
                count = self.RESOURCE_COUNTS[object_name]
            else:
                count = 1

            # Place objects
            for _ in range(count):
                row, col = self._generate_positions()
                while (row, col) in used_positions:
                    row, col = self._generate_positions()
                used_positions.append((row, col))
                self.grid[row, col, i] = 1

        self.agent_position = (0, 0)
        self.direction = np.zeros((4,))

    def step(self, action):
        if action == self.USE:
            self._handle_use_action()
        else:
            self._update_agent_position(action)
            self._update_agent_direction(action)

    def render(self):
        self.renderer.render(
            grid=self.grid,
            inventory=self.inventory,
            agent_position=self.agent_position,
            direction=self.direction,
        )

    def _handle_use_action(self):
        interaction_row = self.agent_position[0]
        interaction_col = self.agent_position[1]

        if self.direction[0] == 1:
            interaction_col += 1 if interaction_col + 1 < self.n_cols else 0
        elif self.direction[1] == 1:
            interaction_col -= 1 if interaction_col - 1 >= 0 else 0
        elif self.direction[2] == 1:
            interaction_row -= 1 if interaction_row - 1 >= 0 else 0
        elif self.direction[3] == 1:
            interaction_row += 1 if interaction_row + 1 < self.n_rows else 0

        print("Interacting with: ", interaction_row, interaction_col)

        if np.max(self.grid[interaction_row, interaction_col]) == 0:
            # Interaction cell is empty
            return

        # Get object type
        object_type = np.argmax(self.grid[interaction_row, interaction_col])
        object_name = self.ENVIRONMENT_OBJECTS[object_type]

        # Add object to inventory
        if object_name == "tree":
            self.inventory[0] += 1
            self.grid[interaction_row, interaction_col, object_type] = 0
        elif object_name == "stone":
            self.inventory[1] += 1
            self.grid[interaction_row, interaction_col, object_type] = 0
        elif object_name == "grass":
            self.inventory[2] += 1
            self.grid[interaction_row, interaction_col, object_type] = 0
        elif object_name == "crafting-table":
            if self.inventory[3] > 0 and self.inventory[1] >= 1:
                # Weapon
                self.inventory[6] += 1
                self.inventory[3] -= 1
                self.inventory[1] -= 1
            elif self.inventory[3] > 0 and self.inventory[4] >= 1:
                # Bridge
                self.inventory[5] += 1
                self.inventory[3] -= 1
                self.inventory[4] -= 1
            elif self.inventory[0] > 0:
                # Sticks
                self.inventory[0] -= 1
                self.inventory[3] += 1
            elif self.inventory[2] > 0:
                # Rope
                self.inventory[2] -= 1
                self.inventory[4] += 1

    def _update_agent_position(self, action):
        self.last_position = self.agent_position
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

        # Update position if no collision
        if np.max(self.grid[n_row, n_col]) == 0:
            self.agent_position = (n_row, n_col)

    def _update_agent_direction(self, action):
        last_direction = self.direction
        self.direction = np.zeros((4,))

        if action == self.RIGHT:
            self.direction[0] = 1
        elif action == self.LEFT:
            self.direction[1] = 1
        elif action == self.UP:
            self.direction[2] = 1
        elif action == self.DOWN:
            self.direction[3] = 1
        elif action == self.USE:
            self.direction = last_direction


if __name__ == "__main__":
    env = Environment()
    env.reset()

    while True:
        a = np.random.choice([0, 1, 2, 3])
        # time.sleep(1)
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
