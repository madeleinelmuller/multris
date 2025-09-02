# multris

A local multiplayer Tetris implemented in Python using Pygame. Two players battle on separate boards in the same window.

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

Install dependencies:

```bash
pip install pygame
```

## Running the game

```bash
python main.py
```

### Controls

**Player 1**

- Move: Left/Right arrows
- Rotate: Up arrow
- Soft drop: Down arrow
- Hard drop: Space

**Player 2**

- Move: A/D
- Rotate: W
- Soft drop: S
- Hard drop: Shift

## Tests

The core game logic is tested with `pytest`.

```bash
pytest
```
