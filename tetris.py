import pygame
import random
from dataclasses import dataclass

# Game configuration
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
PLAYERS = 2
FPS = 60

# Define the shapes of the single tetrominoes
SHAPES = {
    'S': [['.....',
           '..XX.',
           '.XX..',
           '.....',
           '.....'],
          ['.....',
           '..X..',
           '..XX.',
           '...X.',
           '.....']],
    'Z': [['.....',
           '.XX..',
           '..XX.',
           '.....',
           '.....'],
          ['.....',
           '..X..',
           '.XX..',
           '.X...',
           '.....']],
    'I': [['..X..',
           '..X..',
           '..X..',
           '..X..',
           '.....'],
          ['.....',
           'XXXX.',
           '.....',
           '.....',
           '.....']],
    'O': [['.....',
           '.XX..',
           '.XX..',
           '.....',
           '.....']],
    'J': [['.....',
           '.X...',
           '.XXX.',
           '.....',
           '.....'],
          ['.....',
           '..XX.',
           '..X..',
           '..X..',
           '.....'],
          ['.....',
           '.....',
           '.XXX.',
           '...X.',
           '.....'],
          ['.....',
           '..X..',
           '..X..',
           '.XX..',
           '.....']],
    'L': [['.....',
           '...X.',
           '.XXX.',
           '.....',
           '.....'],
          ['.....',
           '..X..',
           '..X..',
           '..XX.',
           '.....'],
          ['.....',
           '.....',
           '.XXX.',
           '.X...',
           '.....'],
          ['.....',
           '.XX..',
           '..X..',
           '..X..',
           '.....']],
    'T': [['.....',
           '..X..',
           '.XXX.',
           '.....',
           '.....'],
          ['.....',
           '..X..',
           '..XX.',
           '..X..',
           '.....'],
          ['.....',
           '.....',
           '.XXX.',
           '..X..',
           '.....'],
          ['.....',
           '..X..',
           '.XX..',
           '..X..',
           '.....']]
}

COLORS = {
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'J': (255, 165, 0),
    'L': (0, 0, 255),
    'T': (160, 32, 240)
}

@dataclass
class Piece:
    x: int
    y: int
    shape: str
    rotation: int = 0

    def image(self):
        return SHAPES[self.shape][self.rotation % len(SHAPES[self.shape])]

    def cells(self):
        cells = []
        image = self.image()
        for i, row in enumerate(image):
            for j, cell in enumerate(row):
                if cell == 'X':
                    cells.append((self.x + j - 2, self.y + i - 2))
        return cells

class Board:
    def __init__(self):
        self.grid = [[(0,0,0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.locked = {}
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0

    def get_new_piece(self):
        shape = random.choice(list(SHAPES.keys()))
        return Piece(BOARD_WIDTH // 2, 0, shape)

    def valid_space(self, piece):
        for x, y in piece.cells():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and (x, y) in self.locked:
                return False
        return True

    def rotate(self):
        piece = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape, self.current_piece.rotation + 1)
        if self.valid_space(piece):
            self.current_piece.rotation += 1

    def move(self, dx):
        piece = Piece(self.current_piece.x + dx, self.current_piece.y, self.current_piece.shape, self.current_piece.rotation)
        if self.valid_space(piece):
            self.current_piece.x += dx

    def drop(self):
        piece = Piece(self.current_piece.x, self.current_piece.y + 1, self.current_piece.shape, self.current_piece.rotation)
        if self.valid_space(piece):
            self.current_piece.y += 1
        else:
            for x, y in self.current_piece.cells():
                if y < 0:
                    raise ValueError('Game over')
                self.locked[(x, y)] = COLORS[self.current_piece.shape]
            self.clear_rows()
            self.current_piece = self.next_piece
            self.next_piece = self.get_new_piece()

    def hard_drop(self):
        try:
            while True:
                self.drop()
        except ValueError:
            raise
        except:
            pass

    def clear_rows(self):
        rows_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all((x, y) in self.locked for x in range(BOARD_WIDTH)):
                rows_to_clear.append(y)
        for y in rows_to_clear:
            for x in range(BOARD_WIDTH):
                del self.locked[(x, y)]
        if rows_to_clear:
            self.score += (len(rows_to_clear) ** 2) * 100
            for key in sorted(list(self.locked), key=lambda k: k[1])[::-1]:
                x, y = key
                shift = sum(1 for row in rows_to_clear if y < row)
                if shift > 0:
                    self.locked[(x, y + shift)] = self.locked.pop(key)

    def draw_grid(self, surface, offset_x):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                rect = pygame.Rect(offset_x + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, (40,40,40), rect, 1)

    def draw_locked(self, surface, offset_x):
        for (x, y), color in self.locked.items():
            rect = pygame.Rect(offset_x + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            surface.fill(color, rect)

    def draw_piece(self, surface, piece, offset_x):
        for x, y in piece.cells():
            if y >= 0:
                rect = pygame.Rect(offset_x + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                surface.fill(COLORS[piece.shape], rect)

class Game:
    def __init__(self):
        pygame.init()
        width = PLAYERS * BOARD_WIDTH * BLOCK_SIZE + (PLAYERS+1)*BLOCK_SIZE
        height = BOARD_HEIGHT * BLOCK_SIZE
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Multris - Local Multiplayer Tetris')
        self.boards = [Board() for _ in range(PLAYERS)]
        self.clock = pygame.time.Clock()

    def run(self):
        fall_time = [0 for _ in range(PLAYERS)]
        fall_speed = 0.5
        running = True
        while running:
            dt = self.clock.get_rawtime()/1000
            self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Player 1 controls - arrow keys
                    if event.key == pygame.K_UP:
                        self.boards[0].rotate()
                    if event.key == pygame.K_LEFT:
                        self.boards[0].move(-1)
                    if event.key == pygame.K_RIGHT:
                        self.boards[0].move(1)
                    if event.key == pygame.K_DOWN:
                        self.boards[0].drop()
                    if event.key == pygame.K_RCTRL or event.key == pygame.K_RETURN:
                        self.boards[0].hard_drop()

                    # Player 2 controls - WASD
                    if PLAYERS > 1:
                        if event.key == pygame.K_w:
                            self.boards[1].rotate()
                        if event.key == pygame.K_a:
                            self.boards[1].move(-1)
                        if event.key == pygame.K_d:
                            self.boards[1].move(1)
                        if event.key == pygame.K_s:
                            self.boards[1].drop()
                        if event.key == pygame.K_SPACE:
                            self.boards[1].hard_drop()

            for i, board in enumerate(self.boards):
                fall_time[i] += dt
                if fall_time[i] > fall_speed:
                    try:
                        board.drop()
                    except ValueError:
                        running = False
                    fall_time[i] = 0

            self.window.fill((0,0,0))
            for i, board in enumerate(self.boards):
                offset_x = BLOCK_SIZE + i*(BOARD_WIDTH*BLOCK_SIZE + BLOCK_SIZE)
                board.draw_locked(self.window, offset_x)
                board.draw_piece(self.window, board.current_piece, offset_x)
                board.draw_grid(self.window, offset_x)
                # Score display
                font = pygame.font.SysFont('Arial', 18)
                label = font.render(f'Score: {board.score}', True, (255,255,255))
                self.window.blit(label, (offset_x, 5))

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    Game().run()
