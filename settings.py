# Game settings (Defaulted as "Expert")
game_width = 30 # Grid width
game_height = 16 # Grid height
game_mines = 99 # Number of mines
game_cell_size = 32 # Width/height of cells

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