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

# Import sprites
cell_sprites = {
  "1": pygame.image.load("sprites/cell_1.png"),
  "2": pygame.image.load("sprites/cell_2.png"),
  "3": pygame.image.load("sprites/cell_3.png"),
  "4": pygame.image.load("sprites/cell_4.png"),
  "5": pygame.image.load("sprites/cell_5.png"),
  "6": pygame.image.load("sprites/cell_6.png"),
  "7": pygame.image.load("sprites/cell_7.png"),
  "8": pygame.image.load("sprites/cell_8.png"),
  "default": pygame.image.load("sprites/cell_default.png"),
  "empty": pygame.image.load("sprites/cell_empty.png"),
  "flag": pygame.image.load("sprites/cell_flag.png"),
  "mine_clicked": pygame.image.load("sprites/cell_mine_clicked.png"),
  "mine_false": pygame.image.load("sprites/cell_mine_false.png"),
  "mine": pygame.image.load("sprites/cell_mine.png")
}

grid = [] # Grid of cells
mines = [] # List of tuples for mine locations

class Cell:
  # Class constructor
  def __init__(self, x, y, type):
    self.x = x
    self.y = y
    self.clicked = False # Bool for if user clicked cell
    self.flagged = False # Bool for if user flagged cell
    self.mine_clicked = False # Bool for if a mine was clicked
    self.type = type # Value of cell, -1 is a mine

    # Drawing variables
    self.rect = pygame.Rect(
      self.x * game_cell_size, 
      self.y * game_cell_size, 
      game_cell_size, 
      game_cell_size
    )


  # Grid initialization function
  def update_mine_count(self):
    if self.type != -1:
      for i in range(-1, 2):
        if self.x + i >= 0 and self.x + i < game_width:
          for j in range(-1, 2):
            if self.y + j >= 0 and self.y + j < game_height:
              if grid[self.y + j][self.x + i].type == -1:
                self.type += 1

  def reveal_cell(self):
    if not self.clicked:
      self.clicked = True
      if self.type == 0: # If cell is a 0, reveal adjacent cells
        for i in range(-1, 2):
          if self.x + i >= 0 and self.x + i < game_width:
            for j in range(-1, 2):
              if self.y + j >= 0 and self.y + j < game_height:
                if not grid[self.y + j][self.x + i].clicked:
                  grid[self.y + j][self.x + i].reveal_cell()
      elif self.type == -1: # If cell is a mine, reveal all other mines
        for mine in mines:
          if not grid[mine[1]][mine[0]].clicked:
            grid[mine[1]][mine[0]].reveal_cell()


  # Draw cell to window
  def draw_cell(self):
    if self.clicked:
      if self.type == -1:
        if self.mine_clicked:
          display_window.blit(cell_sprites["mine_clicked"], self.rect)
        else:
          display_window.blit(cell_sprites["mine"], self.rect)
      elif self.type == 0:
        display_window.blit(cell_sprites["empty"], self.rect)
      elif self.type == 1:
        display_window.blit(cell_sprites["1"], self.rect)
      elif self.type == 2:
        display_window.blit(cell_sprites["2"], self.rect)
      elif self.type == 3:
        display_window.blit(cell_sprites["3"], self.rect)
      elif self.type == 4:
        display_window.blit(cell_sprites["4"], self.rect)
      elif self.type == 5:
        display_window.blit(cell_sprites["5"], self.rect)
      elif self.type == 6:
        display_window.blit(cell_sprites["6"], self.rect)
      elif self.type == 7:
        display_window.blit(cell_sprites["7"], self.rect)
      elif self.type == 8:
        display_window.blit(cell_sprites["8"], self.rect)
    else:
      if self.flagged:
        display_window.blit(cell_sprites["flag"], self.rect)
      else:
        display_window.blit(cell_sprites["default"], self.rect)

# Grid generation
def generate_grid():
  # Generate mine locations
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


# Draw grid
def draw_grid():
  for row in grid:
    for cell in row:
      cell.draw_cell()


# Main game loop
def gameloop():
  game_state = "Play"
  run = True
  generate_grid()

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONUP:
        for row in grid:
          for cell in row:
            if cell.rect.collidepoint(event.pos):
              if event.button == 1: # Left-click
                if not cell.flagged:
                  cell.reveal_cell()
                  if cell.type == -1:
                    cell.mine_clicked = True
                    game_state = "Lose"
              elif event.button == 2: # Middle-click
                
                pass
              elif event.button == 3: # Right-click
                # Toggle 
                if not cell.clicked:
                  cell.flagged = not cell.flagged

    draw_grid()
    pygame.display.update()

  # Quit once gameloop ends
  pygame.quit()
  quit()

gameloop()

