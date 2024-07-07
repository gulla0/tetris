# Tetris Game

## Overview

This Tetris game is implemented using Python and Pygame. The game features classic Tetris mechanics, including different shaped pieces (tetrominos), rotation, and line clearing. The game can be played in fullscreen mode and tracks the player's score.

## Setup

1. **Install Pygame**:
   Ensure you have Pygame installed. If not, install it using pip:
   ```sh
   pip install pygame
   ```

2. **Run the Game**:
   Execute the script to start the game:
   ```sh
   python tetris_game.py
   ```

## Game Components

### Constants

- **Colors**:
  ```python
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREEN = (0, 255, 0)
  CYAN = (0, 255, 255)
  RED = (255, 0, 0)
  ```

- **Grid Dimensions**:
  ```python
  GRID_WIDTH = 10
  GRID_HEIGHT = 20
  INITIAL_SCREEN_WIDTH = 400
  INITIAL_SCREEN_HEIGHT = 700
  ```

- **Tetrominos Shapes**:
  ```python
  TETROMINOS = {
      'I': [[1, 1, 1, 1]],
      'O': [[1, 1], [1, 1]],
      'T': [[0, 1, 0], [1, 1, 1]],
      'S': [[0, 1, 1], [1, 1, 0]],
      'Z': [[1, 1, 0], [0, 1, 1]],
      'J': [[1, 0, 0], [1, 1, 1]],
      'L': [[0, 0, 1], [1, 1, 1]]
  }
  ```

### Variables

- **Display**:
  ```python
  screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT))
  pygame.display.set_caption("Tetris AI")
  fullscreen = False
  ```

- **Game State**:
  ```python
  board = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
  current_piece = None
  current_position = (0, 0)
  score = 0
  game_over = False
  last_horizontal_move_time = pygame.time.get_ticks()
  horizontal_move_delay = 100  # milliseconds delay for continuous horizontal movement
  ```

## Functions

### `toggle_fullscreen()`

Toggle between fullscreen and windowed mode.

### `calculate_dimensions()`

Calculate the cell size and grid origin based on the current screen dimensions.

### `spawn_piece()`

Spawn a new random piece at the top of the grid. Ends the game if there is no space for the new piece.

### `rotate_piece()`

Rotate the current piece if there is space for the new orientation.

### `can_move(dx, dy, piece=None)`

Check if the current piece can move by `(dx, dy)` without colliding with the board edges or existing pieces.

### `move_piece(dx, dy)`

Move the current piece by `(dx, dy)` if possible.

### `fix_piece()`

Fix the current piece to the board and clear any full lines. Spawn a new piece afterwards.

### `clear_lines()`

Clear any full lines on the board and shift the above lines down. Return the number of lines cleared.

### `draw_board()`

Draw the game board, with empty cells in white and filled cells in green.

### `draw_piece()`

Draw the current piece in cyan at its current position.

### `draw_score()`

Display the current score on the screen.

### `draw_game_over()`

Display the game over message and the final score.

## Game Loop

The main loop of the game handles user inputs, automatic piece dropping, screen updates, and game state transitions.

```python
def game_loop():
    # Initial setup
    global screen, game_over, score, board, fullscreen, last_horizontal_move_time
    running = True
    clock = pygame.time.Clock()
    last_drop_time = pygame.time.get_ticks()
    last_horizontal_move_time = pygame.time.get_ticks()
    drop_speed = 500  # time in ms between automatic piece drops

    spawn_piece()

    while running:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if game_over:
            draw_game_over()
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    game_over = False
                    board = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
                    score = 0
                    last_drop_time = pygame.time.get_ticks()
                    last_horizontal_move_time = pygame.time.get_ticks()
                    spawn_piece()
                elif event.key == pygame.K_q and game_over:
                    running = False
                elif not game_over:
                    if event.key == pygame.K_UP:
                        rotate_piece()
                    if event.key == pygame.K_f:
                        toggle_fullscreen()

        if not game_over:
            if keys[pygame.K_DOWN] and can_move(0, 1):
                move_piece(0, 1)

            if current_time - last_drop_time > drop_speed:
                if can_move(0, 1):
                    move_piece(0, 1)
                else:
                    fix_piece()
                last_drop_time = current_time

            if current_time - last_horizontal_move_time > horizontal_move_delay:
                if keys[pygame.K_LEFT] and can_move(-1, 0):
                    move_piece(-1, 0)
                if keys[pygame.K_RIGHT] and can_move(1, 0):
                    move_piece(1, 0)
                last_horizontal_move_time = current_time

            screen.fill(BLACK)
            draw_board()
            draw_piece()
            draw_score()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

game_loop()
```

## Controls

- **Arrow Keys**: Move the piece left, right, or down.
- **Up Arrow Key**: Rotate the piece.
- **F Key**: Toggle fullscreen mode.
- **R Key**: Restart the game after game over.
- **Q Key**: Quit the game after game over.

## Features

- **Random Tetrominos**: Pieces are randomly selected from the predefined shapes.
- **Piece Rotation**: Pieces can be rotated using the up arrow key.
- **Line Clearing**: Complete lines are cleared, and the score is updated.
- **Fullscreen Mode**: Toggle fullscreen mode using the 'F' key.
- **Score Display**: The current score is displayed on the screen.
- **Game Over**: A game over message and the final score are displayed when the game ends.
```

