# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic
# To create & start using python venv:
#       python -m venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 15th of December 2023
# Mail with:
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them.


import pygame
from Services.Grid import Grid
from Extensions.Colors import Colors
from Core.Text import TextFactory

# Initialize Pygame
pygame.init()

# Setting caption
pygame.display.set_caption("GAME OF LIFE")

# Screen dimensions
width, height = 1080, 720
size = (width, height)
screen = pygame.display.set_mode(size)

# Initialize clock
clock = pygame.time.Clock()
fps = 10

# Grid dimensions
n_cells_x, n_cells_y = 60, 40

# Create grid instance
grid = Grid(width, height, screen, n_cells_x, n_cells_y)

# Create text instance
text_factory = TextFactory()
navigation_info_text = text_factory.create_shape("NavigationInfoText", width // 2, 700, screen)

pause = False
running = True
while running:
    clock.tick(fps)

    screen.fill(Colors.WHITE.value)
    grid.draw_game(pause)
    navigation_info_text.draw()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // grid.cell_width, event.pos[1] // grid.cell_height
            grid.game_state[x, y] = not grid.game_state[x, y]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_s:
                # Save game state using the singleton instance
                grid.save_game_state()
            if event.key == pygame.K_l:
                # Load game state using the singleton instance
                grid.load_game_state()

    grid.next_generation(pause)

pygame.quit()
