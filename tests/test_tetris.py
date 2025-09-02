from tetris import Board, TETROMINOES

def test_clear_lines():
    board = Board()
    board.grid[-1] = ['I'] * board.width
    cleared = board.clear_lines()
    assert cleared == 1
    assert board.grid[0] == [0] * board.width

def test_rotation_and_move():
    board = Board()
    board.current_shape = 'I'
    board.current = TETROMINOES['I']
    board.x = 0
    board.y = 0
    board.rotation = 0
    assert board.valid(board.x, board.y, board.rotation)
    board.rotate()
    assert board.rotation == 1
    board.move(1)
    assert board.x == 1
