import random

# Tetromino shapes and rotations
TETROMINOES = {
    'I': [
        [(0,1),(1,1),(2,1),(3,1)],
        [(2,0),(2,1),(2,2),(2,3)]
    ],
    'O': [
        [(1,0),(2,0),(1,1),(2,1)]
    ],
    'T': [
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(2,1),(1,2)],
        [(0,1),(1,1),(2,1),(1,2)],
        [(1,0),(0,1),(1,1),(1,2)]
    ],
    'S': [
        [(1,0),(2,0),(0,1),(1,1)],
        [(1,0),(1,1),(2,1),(2,2)]
    ],
    'Z': [
        [(0,0),(1,0),(1,1),(2,1)],
        [(2,0),(1,1),(2,1),(1,2)]
    ],
    'J': [
        [(0,0),(0,1),(1,1),(2,1)],
        [(1,0),(2,0),(1,1),(1,2)],
        [(0,1),(1,1),(2,1),(2,2)],
        [(1,0),(1,1),(0,2),(1,2)]
    ],
    'L': [
        [(2,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(1,2),(2,2)],
        [(0,1),(1,1),(2,1),(0,2)],
        [(0,0),(1,0),(1,1),(1,2)]
    ]
}

COLORS = {
    'I': (0,255,255),
    'O': (255,255,0),
    'T': (128,0,128),
    'S': (0,255,0),
    'Z': (255,0,0),
    'J': (0,0,255),
    'L': (255,165,0)
}

class Board:
    """Represents a single player's Tetris board."""
    width = 10
    height = 20

    def __init__(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.game_over = False
        self.spawn_new_piece()

    def spawn_new_piece(self):
        self.current_shape = random.choice(list(TETROMINOES.keys()))
        self.rotation = 0
        self.current = TETROMINOES[self.current_shape]
        self.x = self.width // 2 - 2
        self.y = 0
        if not self.valid(self.x, self.y, self.rotation):
            self.game_over = True

    def shape_coords(self, x=None, y=None, rotation=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if rotation is None:
            rotation = self.rotation
        return [(x + dx, y + dy) for dx, dy in self.current[rotation]]

    def valid(self, x, y, rotation):
        for px, py in self.shape_coords(x, y, rotation):
            if px < 0 or px >= self.width or py < 0 or py >= self.height:
                return False
            if self.grid[py][px]:
                return False
        return True

    def rotate(self):
        new_rotation = (self.rotation + 1) % len(self.current)
        if self.valid(self.x, self.y, new_rotation):
            self.rotation = new_rotation

    def move(self, dx):
        if self.valid(self.x + dx, self.y, self.rotation):
            self.x += dx

    def drop(self):
        if self.valid(self.x, self.y + 1, self.rotation):
            self.y += 1
            return True
        self.lock_piece()
        return False

    def hard_drop(self):
        while self.drop():
            pass

    def lock_piece(self):
        for px, py in self.shape_coords():
            self.grid[py][px] = self.current_shape
        self.clear_lines()
        self.spawn_new_piece()

    def clear_lines(self):
        new_grid = [row for row in self.grid if 0 in row]
        cleared = self.height - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])
        self.grid = new_grid
        return cleared
