import pygame 

# Import sprites
cell_sprites = {
  "0": pygame.image.load("sprites/cell/0.png"),
  "1": pygame.image.load("sprites/cell/1.png"),
  "2": pygame.image.load("sprites/cell/2.png"),
  "3": pygame.image.load("sprites/cell/3.png"),
  "4": pygame.image.load("sprites/cell/4.png"),
  "5": pygame.image.load("sprites/cell/5.png"),
  "6": pygame.image.load("sprites/cell/6.png"),
  "7": pygame.image.load("sprites/cell/7.png"),
  "8": pygame.image.load("sprites/cell/8.png"),
  "default": pygame.image.load("sprites/cell/default.png"),
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
  "sad": pygame.image.load("sprites/face/sad.png"),
  "won": pygame.image.load("sprites/face/won.png")
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