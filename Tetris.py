import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],                            # I
    [[1, 1, 1], [0, 1, 0]],                    # T
    [[1, 1, 1], [1, 0, 0]],                    # L
    [[1, 1, 1], [0, 0, 1]],                    # J
    [[1, 1], [1, 1]],                          # O
    [[1, 1, 0], [0, 1, 1]],                    # Z
    [[0, 1, 1], [1, 1, 0]],                    # S
]

SHAPES_COLORS = [CYAN, PURPLE, YELLOW, GREEN, BLUE, ORANGE, RED]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_tetromino(tetromino, x, y):
    shape = SHAPES[tetromino['shape']]
    color = SHAPES_COLORS[tetromino['shape']]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(screen, color, pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BLACK, pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def check_collision(board, tetromino, offset):
    shape = SHAPES[tetromino['shape']]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if row + tetromino['y'] + offset[1] >= GRID_HEIGHT or col + tetromino['x'] + offset[0] < 0 or col + tetromino['x'] + offset[0] >= GRID_WIDTH or board[row + tetromino['y'] + offset[1]][col + tetromino['x'] + offset[0]]:
                    return True
    return False

def merge_tetromino(board, tetromino):
    shape = SHAPES[tetromino['shape']]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                board[row + tetromino['y']][col + tetromino['x']] = tetromino['shape']

def clear_lines(board):
    lines_to_clear = [row for row in range(GRID_HEIGHT) if all(board[row])]
    for line in lines_to_clear:
        del board[line]
        board.insert(0, [0] * GRID_WIDTH)

def new_tetromino():
    return {
        'shape': random.randint(0, len(SHAPES) - 1),
        'x': GRID_WIDTH // 2 - 1,
        'y': 0,
    }

def draw_board(board):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if board[row][col]:
                pygame.draw.rect(screen, SHAPES_COLORS[board[row][col]], pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BLACK, pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def main():
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    tetromino = new_tetromino()
    game_over = False
    timer = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not check_collision(board, tetromino, (-1, 0)):
            tetromino['x'] -= 1
        if keys[pygame.K_RIGHT] and not check_collision(board, tetromino, (1, 0)):
            tetromino['x'] += 1
        if keys[pygame.K_DOWN] and not check_collision(board, tetromino, (0, 1)):
            tetromino['y'] += 1

        # Move the tetromino down every 500ms
        current_time = pygame.time.get_ticks()
        if current_time - timer > 500:
            if not check_collision(board, tetromino, (0, 1)):
                tetromino['y'] += 1
            else:
                merge_tetromino(board, tetromino)
                clear_lines(board)
                tetromino = new_tetromino()
                if check_collision(board, tetromino, (0, 0)):
                    game_over = True
            timer = current_time

        screen.fill(BLACK)
        draw_grid()
        draw_tetromino(tetromino, tetromino['x'], tetromino['y'])
        draw_board(board)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
