import random
import pygame

pygame.init()

# Game settings (Defaulted as "Expert")
game_width = 30 # Grid width
game_height = 16 # Grid height
game_mines = 99 # Number of mines
game_cell_size = 32 # Width/height of cells

# Display settings
display_width = game_width * game_cell_size
display_height = game_height * game_cell_size
display_window = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Minesweeper")

grid = [] # Grid of cells

class Cell:
  # Class constructor
  def __init__(self, x, y, type):
    self.x = x
    self.y = y
    self.clicked = False # Bool for if user clicked cell
    self.flag = False # Bool for if user flagged cell
    self.type = type # Value of cell, -1 is a mine


  # Initialization functions
  def update_mine_count(self):
    if self.type != -1:
      for i in range(-1, 2):
        if self.x + i >= 0 and self.x + i < game_width:
          for j in range(-1, 2):
            if self.y + j >= 0 and self.y + j < game_height:
              if grid[self.y + j][self.x + i].type == -1:
                self.type += 1


  def draw_cell(self):
    pass


# Grid generation
def generate_grid():
  # Generate mine locations
  mines = []
  while len(mines) < game_mines:
    x = random.randint(0, game_width - 1)
    y = random.randint(0, game_height - 1)
    if (x, y) not in mines: mines.append((x, y))

  # Generate board with mines
  for j in range(game_height):
    row = []
    for i in range(game_width):
      if (i, j) in mines: row.append(Cell(i, j, -1))
      else: row.append (Cell(i, j, 0))
    grid.append(row)

  # Update all non-mine spaces
  for row in grid:
    for cell in row:
      cell.update_mine_count()


# Print grid
def print_grid():
  for row in grid:
    line_str = ""
    for cell in row:
      if cell.type == -1: line_str += "X "
      else: line_str += str(cell.type) + " "
    print(line_str)


# Main game loop
def gameloop():
  playing = True
  generate_grid()

  while playing:
    input("")
    playing = False


gameloop()

# Quit once gameloop ends
pygame.quit()
quit()