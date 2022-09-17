import random
from re import M
import pygame

pygame.init()

# Game settings (Defaulted as "Expert")
game_width = 30 # Grid width
game_height = 16 # Grid height
game_mines = 99 # Number of mines
game_cell_size = 32 # Width/height of cells
timer = pygame.time.Clock()

# Display settings
border = 20
button_size = 52
header_height = 104
inner_header_spacer = 12
inner_header_height = 64
counter_width = 26
counter_height = 46
display_width = (game_width * game_cell_size) + (2 * border)
display_height = (game_height * game_cell_size) + border + header_height
display_window = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Minesweeper")

# Frame rects
top_left_rect = pygame.Rect(0, 0, display_width, header_height)
top_right_rect = pygame.Rect(display_width - border, 0, border, border)
left_rect = pygame.Rect(0, header_height, border, display_height - header_height)
right_rect = pygame.Rect(display_width - border, header_height, border, display_height - header_height)
bottom_rect = pygame.Rect(0, display_height - border, display_width, border)
bottom_left_rect = pygame.Rect(0, display_height - border, border, border)
bottom_right_rect = pygame.Rect(display_width - border, display_height - border, border, border)

# Mine count rects
mine_hund_rect = pygame.Rect(
  border + inner_header_spacer,
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)
mine_tens_rect = pygame.Rect(
  border + inner_header_spacer + counter_width,
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)
mine_ones_rect = pygame.Rect(
  border + inner_header_spacer + (counter_width * 2),
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)

# Timer rects
timer_hund_rect = pygame.Rect(
  display_width - border - inner_header_spacer - (3 * counter_width),
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)
timer_tens_rect = pygame.Rect(
  display_width - border - inner_header_spacer - (2 * counter_width),
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)
timer_ones_rect = pygame.Rect(
  display_width - border - inner_header_spacer - (1 * counter_width),
  border + (inner_header_height / 2) - (counter_height / 2),
  counter_width,
  counter_height
)


# Import sprites
cell_sprites = {
  "1": pygame.image.load("sprites/cell/1.png"),
  "2": pygame.image.load("sprites/cell/2.png"),
  "3": pygame.image.load("sprites/cell/3.png"),
  "4": pygame.image.load("sprites/cell/4.png"),
  "5": pygame.image.load("sprites/cell/5.png"),
  "6": pygame.image.load("sprites/cell/6.png"),
  "7": pygame.image.load("sprites/cell/7.png"),
  "8": pygame.image.load("sprites/cell/8.png"),
  "default": pygame.image.load("sprites/cell/default.png"),
  "empty": pygame.image.load("sprites/cell/empty.png"),
  "flag": pygame.image.load("sprites/cell/flag.png"),
  "mine_clicked": pygame.image.load("sprites/cell/mine_clicked.png"),
  "mine_false": pygame.image.load("sprites/cell/mine_false.png"),
  "mine": pygame.image.load("sprites/cell/mine.png")
}

frame_sprites = {
  "top_left": pygame.image.load("sprites/frame/top_left.png"),
  "top_right": pygame.image.load("sprites/frame/top_right.png"),
  "left": pygame.image.load("sprites/frame/left.png"),
  "right": pygame.image.load("sprites/frame/right.png"),
  "bottom": pygame.image.load("sprites/frame/bottom.png"),
  "bottom_left": pygame.image.load("sprites/frame/bottom_left.png"),
  "bottom_right": pygame.image.load("sprites/frame/bottom_right.png")
}

face_sprites = {
  "default": pygame.image.load("sprites/face/default.png"),
  "pressed": pygame.image.load("sprites/face/pressed.png"),
  "waiting": pygame.image.load("sprites/face/waiting.png"),
  "sad": pygame.image.load("sprites/face/sad.png")
}

counter_sprites = {
  "0": pygame.image.load("sprites/counter/0.png"),
  "1": pygame.image.load("sprites/counter/1.png"),
  "2": pygame.image.load("sprites/counter/2.png"),
  "3": pygame.image.load("sprites/counter/3.png"),
  "4": pygame.image.load("sprites/counter/4.png"),
  "5": pygame.image.load("sprites/counter/5.png"),
  "6": pygame.image.load("sprites/counter/6.png"),
  "7": pygame.image.load("sprites/counter/7.png"),
  "8": pygame.image.load("sprites/counter/8.png"),
  "9": pygame.image.load("sprites/counter/9.png")
}

# Game state variables
grid = [] # Grid of cells
mines = [] # List of tuples for mine locations
mines_left = game_mines
time = 0

class Button:
  def __init__(self):
    self.state = "default"
    self.rect = pygame.Rect(
      (display_width / 2) - (button_size / 2),
      (inner_header_height / 2) - (button_size / 2) + border,
      button_size,
      button_size
    )

  def draw_button(self):
    display_window.blit(face_sprites[self.state], self.rect)

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
  mines.clear()
  grid.clear()

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
  # Draw to display
  display_window.blit(frame_sprites["top_left"], top_left_rect)
  display_window.blit(frame_sprites["top_right"], top_right_rect)
  display_window.blit(frame_sprites["left"], left_rect)
  display_window.blit(frame_sprites["right"], right_rect)
  display_window.blit(frame_sprites["bottom"], bottom_rect)
  display_window.blit(frame_sprites["bottom_left"], bottom_left_rect)
  display_window.blit(frame_sprites["bottom_right"], bottom_right_rect)

# Draw mine counter
def draw_mine_counter():
  hund = mines_left // 100
  tens = (mines_left - (hund * 100)) // 10
  ones = (mines_left - (hund * 100) - (tens * 10))

  display_window.blit(counter_sprites[str(hund)], mine_hund_rect)
  display_window.blit(counter_sprites[str(tens)], mine_tens_rect)
  display_window.blit(counter_sprites[str(ones)], mine_ones_rect)

# Draw timer
def draw_timer():
  hund = time // 100000
  tens = (time - (hund * 100000)) // 10000
  ones = (time - (hund * 100000) - (tens * 10000)) // 1000
  #print(str(time) + ": " + str(hund) + str(tens) + str(ones))

  display_window.blit(counter_sprites[str(hund)], timer_hund_rect)
  display_window.blit(counter_sprites[str(tens)], timer_tens_rect)
  display_window.blit(counter_sprites[str(ones)], timer_ones_rect)


# Draw grid
def draw_grid():
  for row in grid:
    for cell in row:
      cell.draw_cell()

# Restart game
def restart():
  global mines_left
  global time

  mines_left = game_mines
  time = 0
  generate_grid()
  

# Main game loop
def gameloop():
  global time
  global mines_left
  run = True
  button = Button()
  generate_grid()

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if button.rect.collidepoint(event.pos):
          button.state = "pressed"
        else:
          button.state = "default"
          for row in grid:
            for cell in row:
              if cell.rect.collidepoint(event.pos):
                if event.button == 3: # Right-click
                  if not cell.clicked:
                    if cell.flagged: mines_left += 1
                    else: mines_left -= 1
                    cell.flagged = not cell.flagged
                    
      elif event.type == pygame.MOUSEBUTTONUP:
        if button.rect.collidepoint(event.pos):
          button.state = "default"
          restart()
        else:
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
                
    if time < 999000: # Cap game timer at 999 seconds
      time += timer.get_time()

    draw_frame()
    button.draw_button()
    draw_mine_counter()
    draw_timer()
    draw_grid()
    pygame.display.update()
    
    timer.tick(15)

  # Quit once gameloop ends
  pygame.quit()
  quit()

gameloop()

