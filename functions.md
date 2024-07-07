# Tetris Game Functions

## `toggle_fullscreen()`
This function toggles the game's display mode between fullscreen and windowed mode.

**Logic:**
- It checks the current display mode stored in the `fullscreen` variable.
- If `fullscreen` is `False`, it sets the screen to fullscreen mode using `pygame.display.set_mode((0, 0), pygame.FULLSCREEN)`.
- If `fullscreen` is `True`, it sets the screen back to windowed mode with the initial dimensions using `pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT))`.
- Finally, it updates the `fullscreen` variable to reflect the new display mode.

## `calculate_dimensions()`
This function calculates the size of each cell in the game grid and the origin point of the grid based on the current screen dimensions.

**Logic:**
- It retrieves the current screen dimensions using `pygame.display.Info()`.
- It calculates the cell size as the minimum of the screen width divided by the grid width and the screen height divided by the grid height to ensure cells fit within the screen.
- It calculates the origin point of the grid to center it on the screen using the formula:
  - `grid_origin_x = (screen_width - GRID_WIDTH * cell_size) // 2`
  - `grid_origin_y = (screen_height - GRID_HEIGHT * cell_size) // 2`
- It returns the calculated cell size and grid origin.

## `spawn_piece()`
This function spawns a new random piece at the top of the grid. If there is no space for the new piece, it ends the game.

**Logic:**
- It selects a random piece type from the `TETROMINOS` dictionary using `random.choice()`.
- It sets `current_piece` to a numpy array of the chosen tetromino shape.
- It calculates the starting x-coordinate to center the piece at the top of the grid using `start_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2`.
- It sets `current_position` to `(0, start_x)`.
- It checks if the piece can be placed at the initial position using `can_move(0, 0)`. If not, it sets `game_over` to `True`.

## `rotate_piece()`
This function rotates the current piece if there is space for the new orientation.

**Logic:**
- It creates a new orientation of the current piece by rotating it 90 degrees counterclockwise using `np.rot90(current_piece)`.
- It checks if the new orientation can fit at the current position without colliding using `can_move(0, 0, piece=new_piece)`.
- If there is space, it updates `current_piece` to the new orientation.

## `can_move(dx, dy, piece=None)`
This function checks if the current piece (or a specified piece) can move by `(dx, dy)` without colliding with the board edges or existing pieces.

**Logic:**
- If no piece is specified, it uses `current_piece`.
- It calculates the new position of the piece by adding the deltas to the current position.
- It iterates through each cell of the piece:
  - For each filled cell, it checks if the new position is within the board boundaries and does not overlap with filled cells on the board.
  - If any cell violates these conditions, it returns `False`.
- If all cells are valid, it returns `True`.

## `move_piece(dx, dy)`
This function moves the current piece by `(dx, dy)` if possible.

**Logic:**
- It checks if the piece can move by the specified deltas using `can_move(dx, dy)`.
- If the movement is possible, it updates `current_position` by adding the deltas to the current coordinates.

## `fix_piece()`
This function fixes the current piece to the board and clears any full lines. It then spawns a new piece.

**Logic:**
- It iterates through each cell of the current piece:
  - For each filled cell, it sets the corresponding cell on the board to `1`.
- It calls `clear_lines()` to remove any full lines and shift the above lines down.
- It increments the score based on the number of lines cleared.
- It spawns a new piece by calling `spawn_piece()`.

## `clear_lines()`
This function clears any full lines on the board and shifts the above lines down.

**Logic:**
- It creates a new empty board.
- It initializes `new_row` to the last row index and `lines_cleared` to 0.
- It iterates through each row of the board from bottom to top:
  - If a row is full (all cells are `1`), it increments `lines_cleared` and skips the row.
  - Otherwise, it copies the row to the new board at the `new_row` index and decrements `new_row`.
- It updates the board to the new board.
- It returns the number of lines cleared.

## `draw_board()`
This function draws the game board on the screen.

**Logic:**
- It calculates the cell size and grid origin using `calculate_dimensions()`.
- It iterates through each cell of the board:
  - For each cell, it determines the color (`WHITE` for empty, `GREEN` for filled).
  - It draws a rectangle at the corresponding position on the screen using `pygame.draw.rect()`.

## `draw_piece()`
This function draws the current piece on the screen at its current position.

**Logic:**
- It calculates the cell size and grid origin using `calculate_dimensions()`.
- It iterates through each cell of the current piece:
  - For each filled cell, it draws a cyan rectangle at the corresponding position on the screen using `pygame.draw.rect()`.

## `draw_score()`
This function displays the current score on the screen.

**Logic:**
- It creates a font object and renders the score text using `font.render()`.
- It draws the score text at a fixed position on the screen using `screen.blit()`.

## `draw_game_over()`
This function displays the game over message and the final score.

**Logic:**
- It creates font objects for the game over message and the final score.
- It renders the game over message and centers it on the screen.
- It renders the final score and centers it below the game over message.
- It renders a replay or quit prompt below the final score.
- It draws all the texts on the screen using `screen.blit()`.
