# Tetris Game

This repository contains a simple Tetris implementation built with [pygame](https://www.pygame.org/). The game opens a window and can be played with arrow keys.

## Controls
- **Left / Right**: move the falling piece
- **Up**: rotate
- **Down**: drop faster

The score increases by 10 for every cleared line. When the pieces reach the top, a game over message is shown and the game exits after a short pause.

To run the game:
```bash
python3 tetris.py
```

On headless systems you can run with a dummy video driver:
```bash
SDL_VIDEODRIVER=dummy python3 tetris.py
```
