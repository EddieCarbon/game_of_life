import numpy as np
import pygame
from Extensions.Colors import Colors
from Services.FileManager import FileManager
import threading


class SingletonGrid(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Grid(metaclass=SingletonGrid):

    # Initializing grid
    def __init__(self, width, height, screen, n_cells_x, n_cells_y):
        self.width = width
        self.height = height
        self.n_cells_x = n_cells_x
        self.n_cells_y = n_cells_y
        self.cell_width = width // n_cells_x
        self.cell_height = height // n_cells_y
        self.screen = screen
        self.game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

    def draw_game(self, pause):
        self._draw_grid()
        self._draw_cells()

    # Calculating next generation
    def next_generation(self, pause):
        game = self.game_state
        cells_x = self.n_cells_x
        cells_y = self.n_cells_y
        new_state = np.copy(self.game_state)

        if pause is False:
            for y in range(self.n_cells_y):
                for x in range(self.n_cells_x):
                    n_neighbors = game[(x - 1) % cells_x, (y - 1) % cells_y] + \
                                  game[x % cells_x,       (y - 1) % cells_y] + \
                                  game[(x + 1) % cells_x, (y - 1) % cells_y] + \
                                  game[(x - 1) % cells_x,       y % cells_y] + \
                                  game[(x + 1) % cells_x,       y % cells_y] + \
                                  game[(x - 1) % cells_x, (y + 1) % cells_y] + \
                                  game[x % cells_x,       (y + 1) % cells_y] + \
                                  game[(x + 1) % cells_x, (y + 1) % cells_y]

                    if game[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                        new_state[x, y] = 0
                    elif game[x, y] == 0 and n_neighbors == 3:
                        new_state[x, y] = 1

        self.game_state = new_state

    # Drawing grid
    def _draw_grid(self):
        for y in range(0, self.height, self.cell_height):
            for x in range(0, self.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, Colors.GRAY.value, cell, 1)

    # Drawing cells
    def _draw_cells(self):
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, Colors.DARKBLUE.value, cell)

    # Saving game state to file
    def save_game_state(self):
        try:
            FileManager.save_array("save.npy", self.game_state)
            print("Game state saved successfully.")
        except Exception as e:
            print(f"Error saving game state: {e}")

    # Loading game state from file
    def load_game_state(self):
        try:
            loaded_state = FileManager.load_array("save.npy")
            if loaded_state.shape == self.game_state.shape:
                self.game_state = loaded_state
                print("Game state loaded successfully.")
            else:
                print("Loaded game state shape does not match current game state shape.")
        except Exception as e:
            print(f"Error loading game state: {e}")
