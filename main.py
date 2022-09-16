import random
import pygame

pygame.init()

# Game settings (Defaulted as "Expert")
game_width = 30 # Grid width
game_height = 16 # Grid height
game_mines = 99 # Number of mines
game_cell_size = 32 # Width/height of cells

# Display settings
border = 20
header_height = 104
display_width = (game_width * game_cell_size) + (2 * border)
display_height = (game_height * game_cell_size) + border + header_height
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

frame_sprites = {
  "top_left": pygame.image.load("sprites/frame_top_left.png"),
  "top_right": pygame.image.load("sprites/frame_top_right.png"),
  "left": pygame.image.load("sprites/frame_left.png"),
  "right": pygame.image.load("sprites/frame_right.png"),
  "bottom": pygame.image.load("sprites/frame_bottom.png"),
  "bottom_left": pygame.image.load("sprites/frame_bottom_left.png"),
  "bottom_right": pygame.image.load("sprites/frame_bottom_right.png")
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
      self.x * game_cell_size + border, 
      self.y * game_cell_size + header_height, 
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


  # Reveal single cell
  def reveal_cell(self):
    if not self.clicked and not self.flagged:
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


  # Sweep cells around a clicked cell
  def sweep_cell(self):
    flag_count = 0
    # Check adjacent cells for flags
    for i in range(-1, 2):
        if self.x + i >= 0 and self.x + i < game_width:
          for j in range(-1, 2):
            if self.y + j >= 0 and self.y + j < game_height:
              if grid[self.y + j][self.x + i].flagged:
                flag_count += 1
    
    if flag_count == self.type:
      for i in range(-1, 2):
        if self.x + i >= 0 and self.x + i < game_width:
          for j in range(-1, 2):
            if self.y + j >= 0 and self.y + j < game_height:
              if not grid[self.y + j][self.x + i].clicked:
                if grid[self.y + j][self.x + i].type == -1:
                  grid[self.y + j][self.x + i].mine_clicked = True
                grid[self.y + j][self.x + i].reveal_cell()

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


# Draw frame
def draw_frame():
  # Construct all necessary rects
  top_left_rect = pygame.Rect(0, 0, display_width, header_height)
  top_right_rect = pygame.Rect(display_width - border, 0, border, border)
  left_rect = pygame.Rect(0, header_height, border, display_height - header_height)
  right_rect = pygame.Rect(display_width - border, header_height, border, display_height - header_height)
  bottom_rect = pygame.Rect(0, display_height - border, display_width, border)
  bottom_left_rect = pygame.Rect(0, display_height - border, border, border)
  bottom_right_rect = pygame.Rect(display_width - border, display_height - border, border, border)

  # Draw to display
  display_window.blit(frame_sprites["top_left"], top_left_rect)
  display_window.blit(frame_sprites["top_right"], top_right_rect)
  display_window.blit(frame_sprites["left"], left_rect)
  display_window.blit(frame_sprites["right"], right_rect)
  display_window.blit(frame_sprites["bottom"], bottom_rect)
  display_window.blit(frame_sprites["bottom_left"], bottom_left_rect)
  display_window.blit(frame_sprites["bottom_right"], bottom_right_rect)
  

# Draw grid
def draw_grid():
  for row in grid:
    for cell in row:
      cell.draw_cell()


# Main game loop
def gameloop():
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
              elif event.button == 2: # Middle-click
                if cell.clicked:
                  cell.sweep_cell()
              elif event.button == 3: # Right-click
                if not cell.clicked:
                  cell.flagged = not cell.flagged

    draw_frame()
    draw_grid()
    pygame.display.update()

  # Quit once gameloop ends
  pygame.quit()
  quit()

gameloop()

