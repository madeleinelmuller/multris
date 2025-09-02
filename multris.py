import pygame
import random

# Game settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30
PLAY_WIDTH = BOARD_WIDTH * BLOCK_SIZE
PLAY_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE
TOP_LEFT_X_P1 = 20
TOP_LEFT_Y = 20
TOP_LEFT_X_P2 = TOP_LEFT_X_P1 + PLAY_WIDTH + 60

# Define shapes
S_SHAPE = [['.....',
            '.....',
            '..00.',
            '.00..',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '...0.',
            '.....']]
Z_SHAPE = [['.....',
            '.....',
            '.00..',
            '..00.',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '.0...',
            '.....']]
I_SHAPE = [['..0..',
            '..0..',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '0000.',
            '.....',
            '.....',
            '.....']]
O_SHAPE = [['.....',
            '.....',
            '.00..',
            '.00..',
            '.....']]
J_SHAPE = [['.....',
            '.0...',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..00.',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '...0.',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '.00..',
            '.....']]
L_SHAPE = [['.....',
            '...0.',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '..00.',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '.0...',
            '.....'],
           ['.....',
            '.00..',
            '..0..',
            '..0..',
            '.....']]
T_SHAPE = [['.....',
            '..0..',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '..0..',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '..0..',
            '.....']]

SHAPES = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE]
COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
          (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    for (x, y), color in locked_positions.items():
        if y > -1:
            grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    positions = [(x - 2, y - 4) for x, y in positions]
    return positions


def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(BOARD_WIDTH) if grid[i][j] == (0,0,0)] for i in range(BOARD_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for (_, y) in positions:
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(SHAPES))


def clear_rows(grid, locked):
    cleared = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            cleared += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
    if cleared > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + cleared)
                locked[newKey] = locked.pop(key)
    return cleared


class Board:
    def __init__(self, top_left_x):
        self.top_left_x = top_left_x
        self.locked_positions = {}
        self.grid = create_grid(self.locked_positions)
        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.fall_time = 0
        self.fall_speed = 0.5
        self.score = 0

    def update(self, dt):
        self.fall_time += dt
        if self.fall_time/1000 > self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not valid_space(self.current_piece, self.grid) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.lock_piece()

    def lock_piece(self):
        positions = convert_shape_format(self.current_piece)
        for pos in positions:
            p = (pos[0], pos[1])
            self.locked_positions[p] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = get_shape()
        self.grid = create_grid(self.locked_positions)
        cleared = clear_rows(self.grid, self.locked_positions)
        if cleared > 0:
            self.score += cleared * 100

    def move(self, dx):
        self.current_piece.x += dx
        if not valid_space(self.current_piece, self.grid):
            self.current_piece.x -= dx

    def soft_drop(self):
        self.current_piece.y += 1
        if not valid_space(self.current_piece, self.grid):
            self.current_piece.y -= 1
            self.lock_piece()

    def rotate(self):
        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
        if not valid_space(self.current_piece, self.grid):
            self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)



def draw_grid(surface, board):
    grid = board.grid
    top_left_x = board.top_left_x
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(surface, (128,128,128), (top_left_x + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw current piece
    formatted = convert_shape_format(board.current_piece)
    for (x, y) in formatted:
        if y > -1:
            pygame.draw.rect(surface, board.current_piece.color, (top_left_x + x*BLOCK_SIZE, TOP_LEFT_Y + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_window(surface, board1, board2):
    surface.fill((0,0,0))
    draw_grid(surface, board1)
    draw_grid(surface, board2)
    pygame.display.update()


def main():
    pygame.init()
    width = TOP_LEFT_X_P2 + PLAY_WIDTH + 20
    height = TOP_LEFT_Y + PLAY_HEIGHT + 20
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Multris')
    board1 = Board(TOP_LEFT_X_P1)
    board2 = Board(TOP_LEFT_X_P2)
    clock = pygame.time.Clock()
    run = True
    while run:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board1.move(-1)
                if event.key == pygame.K_RIGHT:
                    board1.move(1)
                if event.key == pygame.K_DOWN:
                    board1.soft_drop()
                if event.key == pygame.K_UP:
                    board1.rotate()
                if event.key == pygame.K_a:
                    board2.move(-1)
                if event.key == pygame.K_d:
                    board2.move(1)
                if event.key == pygame.K_s:
                    board2.soft_drop()
                if event.key == pygame.K_w:
                    board2.rotate()

        board1.update(dt)
        board2.update(dt)

        if check_lost(board1.locked_positions.keys()) or check_lost(board2.locked_positions.keys()):
            run = False

        board1.grid = create_grid(board1.locked_positions)
        board2.grid = create_grid(board2.locked_positions)

        draw_window(win, board1, board2)
    pygame.quit()


if __name__ == '__main__':
    main()
