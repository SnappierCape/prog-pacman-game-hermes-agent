# 🎮 Pac-Man Game

A playable arcade-style Pac-Man game built with Python and Pygame.

## Features
- Classic maze-based gameplay
- Player-controlled Pac-Man character
- Ghost AI with distinct behaviors
- Dots and power pellets system
- Score tracking and levels
- Retro-style UI with sound effects (planned)

## Tech Stack
- **Language:** Python 3.12+
- **Game Engine:** Pygame v2.x
- **Dependency Manager:** [UV](https://github.com/astral-sh/uv)
- **Architecture:** Modular, entity-system design pattern

---

## Project Structure
```
projects/pacman_game/
├── README.md               # This file
├── pyproject.toml          # UV project configuration (dependencies + metadata)
└── src/                    # Source code root
    ├── main.py             # Entry point: runs the game loop
    ├── config.py           # Constants, tuning parameters, colors, sizing
    │
    ├── entities/           # All living objects in the game
    │   ├── __init__.py
    │   ├── pacman.py       # Pac-Man player logic (movement, mouth animation)
    │   └── ghosts.py       # Ghost AI logic (chase, scatter, frightened modes)
    │
    ├── game/               # Core game state management
    │   ├── __init__.py
    │   ├── level_loader.py  # Loads and validates maze layouts from data files
    │   ├── collisions.py    # Collision detection between entities + static world
    │   └── state_machine.py # Finite State Machine (title → playing → game_over)
    │
    └── ui/                 # Everything visual
        ├── __init__.py
        ├── renderer.py      # Surface drawing, sprite rendering, HUD layout
        └── inputs.py        # Keyboard/mouse input processing

```

## Getting Started

### Prerequisites
- Python 3.12+ installed
- UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation & Run

```bash
cd /projects/pacman_game

# Create virtual environment + install dependencies
uv venv
source .venv/bin/activate
uv pip install -e .

# Launch the game
python src/main.py
```

## Controls
| Key       | Action         |
|-----------|----------------|
| Arrow Keys| Move Pac-Man   |
| Space     | Pause / Resume |
| R         | Restart Level  |
| ESC       | Quit Game      |

---

## Development Guidelines
1. All entities inherit from a base `Entity` class in `entities/`.
2. The game loop lives in `main.py` and delegates to FSM states.
3 UI rendering uses Pygame surfaces composed per-frame, not external assets.  
4. Keep logic pure: no pygame calls inside non-ui modules where possible.

## License
MIT © 2026
