import pygame

pygame.init()

# Game Settings (Defaulted as "Expert")
game_width = 30 # Grid width
game_height = 16 # Grid height
game_mines = 99 # Number of mines
game_cell_size = 32 # Width/height of cells

# Display Settings
display_width = game_width * game_cell_size
display_height = game_height * game_cell_size
display_window = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Minesweeper")

