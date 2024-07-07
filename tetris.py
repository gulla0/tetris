import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Define colors and constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GRID_WIDTH = 10
GRID_HEIGHT = 20
INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT = 400, 700

# Define the shapes of the pieces
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# Set up the display
screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT))
pygame.display.set_caption("Tetris AI")
fullscreen = False

# Game board array and variables
board = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
current_piece = None
current_position = (0, 0)
score = 0
game_over = False
last_horizontal_move_time = pygame.time.get_ticks()
horizontal_move_delay = 100  # milliseconds delay for continuous horizontal movement

def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT))

def calculate_dimensions():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    cell_size = min(screen_width // GRID_WIDTH, screen_height // GRID_HEIGHT)
    grid_origin = ((screen_width - GRID_WIDTH * cell_size) // 2,
                   (screen_height - GRID_HEIGHT * cell_size) // 2)
    return cell_size, grid_origin

def spawn_piece():
    global current_piece, current_position, game_over
    piece_type = random.choice(list(TETROMINOS.keys()))
    current_piece = np.array(TETROMINOS[piece_type], dtype=int)
    start_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    current_position = (0, start_x)
    if not can_move(0, 0):
        game_over = True

def rotate_piece():
    global current_piece
    if not game_over:
        new_piece = np.rot90(current_piece)
        if can_move(0, 0, piece=new_piece):
            current_piece = new_piece

def can_move(dx, dy, piece=None):
    if piece is None:
        piece = current_piece
    new_y, new_x = current_position[0] + dy, current_position[1] + dx
    for y in range(piece.shape[0]):
        for x in range(piece.shape[1]):
            if piece[y, x] == 1:
                if new_x + x < 0 or new_x + x >= GRID_WIDTH or new_y + y >= GRID_HEIGHT:
                    return False
                if board[new_y + y, new_x + x] == 1:
                    return False
    return True

def move_piece(dx, dy):
    global current_position
    if not game_over and can_move(dx, dy):
        current_position = (current_position[0] + dy, current_position[1] + dx)

def fix_piece():
    global board, score
    if not game_over:
        for y in range(current_piece.shape[0]):
            for x in range(current_piece.shape[1]):
                if current_piece[y, x] == 1:
                    board[current_position[0] + y, current_position[1] + x] = 1
        lines_cleared = clear_lines()
        score += 100 * lines_cleared
        spawn_piece()

def clear_lines():
    global board
    new_board = np.zeros_like(board)
    new_row = GRID_HEIGHT - 1
    lines_cleared = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(board[y, :] == 1):
            lines_cleared += 1
            continue
        new_board[new_row, :] = board[y, :]
        new_row -= 1
    board = new_board
    return lines_cleared

def draw_board():
    cell_size, grid_origin = calculate_dimensions()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if board[y, x] == 0 else GREEN
            rect = pygame.Rect(grid_origin[0] + x * cell_size, grid_origin[1] + y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

def draw_piece():
    cell_size, grid_origin = calculate_dimensions()
    if current_piece is not None:
        piece, (py, px) = current_piece, current_position
        for y in range(piece.shape[0]):
            for x in range(piece.shape[1]):
                if piece[y, x] == 1:
                    rect = pygame.Rect(grid_origin[0] + (px + x) * cell_size, grid_origin[1] + (py + y) * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, CYAN, rect)

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def draw_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render('Game Over!', True, RED)
    text_rect = text.get_rect(center=(INITIAL_SCREEN_WIDTH // 2, INITIAL_SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)

    font_score = pygame.font.Font(None, 48)
    score_text = font_score.render(f'Final Score: {score}', True, WHITE)
    score_text_rect = score_text.get_rect(center=(INITIAL_SCREEN_WIDTH // 2, INITIAL_SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_text_rect)

    font_small = pygame.font.Font(None, 48)
    replay_text = font_small.render('Press R to Replay or Q to Quit', True, WHITE)
    replay_text_rect = replay_text.get_rect(center=(INITIAL_SCREEN_WIDTH // 2, INITIAL_SCREEN_HEIGHT // 2 + 100))
    screen.blit(replay_text, replay_text_rect)


def game_loop():
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
            pygame.display.flip()  # Ensure the game over message is updated on the screen

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
                    spawn_piece()  # Respawn a new piece to restart the game
                elif event.key == pygame.K_q and game_over:
                    running = False  # Quit the game
                elif not game_over:
                    if event.key == pygame.K_UP:
                        rotate_piece()
                    if event.key == pygame.K_f:
                        toggle_fullscreen()

        if not game_over:
            # Handle smooth continuous movement for down key
            if keys[pygame.K_DOWN] and can_move(0, 1):
                move_piece(0, 1)

            # Automatic piece dropping
            if current_time - last_drop_time > drop_speed:
                if can_move(0, 1):
                    move_piece(0, 1)
                else:
                    fix_piece()
                last_drop_time = current_time

            # Handle smooth continuous movement for left and right keys
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
        clock.tick(30)  # Adjust for smoother gameplay

    pygame.quit()

game_loop()










