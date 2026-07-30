# Tic-Tac-Toe

A desktop Tic-Tac-Toe game in Python with Tkinter: two-player mode, a computer opponent with three
difficulty levels, and a running score that survives restarts.

## Run it

Standard library only — Tkinter ships with Python.

```bash
python main.py
```

## Features

- **Two modes** — player vs player, or player vs computer with a choice of playing X or O.
- **Three difficulty levels** for the computer opponent (easy / medium / hard).
- **Persistent scoreboard** — wins for X, wins for O, and draws are stored in `scores.json` and
  reloaded on launch, with a reset button. Corrupt or missing score files fall back to zeros
  instead of crashing.
- **Winning line highlight** — the three winning cells change colour when a game ends.
- **Dark UI theme** with disabled-state styling on played cells.

## Tests

```bash
python -m pytest test_tictactoe.py
```

Covers win detection across rows, columns and diagonals, and draw detection.

## Files

```
main.py               # game logic + Tkinter UI
test_tictactoe.py     # unit tests for win/draw detection
scores.json           # persisted scoreboard (created on first run)
```
