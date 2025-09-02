import pygame
from tetris import Board, COLORS

BLOCK_SIZE = 30
MARGIN = 5
BOARD_WIDTH = Board.width * BLOCK_SIZE
BOARD_HEIGHT = Board.height * BLOCK_SIZE

WINDOW_WIDTH = BOARD_WIDTH * 2 + MARGIN * 3
WINDOW_HEIGHT = BOARD_HEIGHT + MARGIN * 2

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Multris')
clock = pygame.time.Clock()

board1 = Board()
board2 = Board()

fall_speed = 0.5
fall_time1 = 0
fall_time2 = 0

running = True
while running:
    dt = clock.tick(60) / 1000
    fall_time1 += dt
    fall_time2 += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Player 1 controls
            if event.key == pygame.K_LEFT:
                board1.move(-1)
            elif event.key == pygame.K_RIGHT:
                board1.move(1)
            elif event.key == pygame.K_UP:
                board1.rotate()
            elif event.key == pygame.K_DOWN:
                board1.drop()
            elif event.key == pygame.K_SPACE:
                board1.hard_drop()

            # Player 2 controls
            elif event.key == pygame.K_a:
                board2.move(-1)
            elif event.key == pygame.K_d:
                board2.move(1)
            elif event.key == pygame.K_w:
                board2.rotate()
            elif event.key == pygame.K_s:
                board2.drop()
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                board2.hard_drop()

    if fall_time1 > fall_speed:
        board1.drop()
        fall_time1 = 0
    if fall_time2 > fall_speed:
        board2.drop()
        fall_time2 = 0

    window.fill((0, 0, 0))

    def draw_board(board, offset_x):
        for y in range(Board.height):
            for x in range(Board.width):
                cell = board.grid[y][x]
                color = COLORS.get(cell, (40, 40, 40)) if cell else (40, 40, 40)
                pygame.draw.rect(
                    window,
                    color,
                    (offset_x + x * BLOCK_SIZE, MARGIN + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )
                pygame.draw.rect(
                    window,
                    (0, 0, 0),
                    (offset_x + x * BLOCK_SIZE, MARGIN + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )
        for px, py in board.shape_coords():
            pygame.draw.rect(
                window,
                COLORS[board.current_shape],
                (offset_x + px * BLOCK_SIZE, MARGIN + py * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )

    draw_board(board1, MARGIN)
    draw_board(board2, BOARD_WIDTH + MARGIN * 2)

    pygame.display.flip()

pygame.quit()
