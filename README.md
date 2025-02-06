# Lord of the Grid

A command-line implementation of the classic Dots and Boxes game. The game allows two players to take turns adding lines between dots on a grid. When a player completes a box, they earn a point and get another turn, and the box is 'signed' with their initial. The game ends when no more lines can be added, and the player with the most points wins.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```sh
   git clone https://gitlab.wethinkco.de/sqangule023/lord-of-the-grid
   cd lord-of-the-grid
   ```

2. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

To start the game, run main.py inside src

## Game Rules

1. Players take turns to add a single horizontal or vertical line between two unjoined adjacent dots.
2. A player who completes the fourth side of a 1x1 box earns one point, signs the block, and takes another turn.
3. The game ends when no more lines can be added.
4. The player with the most points at the end of the game wins.

## Project Structure

```
lord-of-the-grid/
├── src/
│   ├── game.py
│   ├── game_grid.py
|   ├── main.py
│   ├── player.py
│   ├── input_handler.py
│   └── utils.py
├── tests/
│   ├── test_game.py
│   ├── test_game_grid.py
│   ├── test_player.py
│   ├── test_input_handler.py
│   └── test_utils.py
├── requirements.txt
└── README.md
```

### `lord-of-the-grid/game.py`

Handles the main game loop and game-related functions.

### `lord-of-the-grid/game_grid.py`

Manages the grid and its operations.

### `lord-of-the-grid/player.py`

Contains player-related logic.

### `lord-of-the-grid/input_handler.py`

Deals with input validation and processing.

### `lord-of-the-grid/utils.py`

Contains utility functions, such as calculating scores and checking if the game has ended.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push the branch to your fork.
5. Open a pull request with a detailed description of your changes.

Enjoy playing Lord of the Grid! If you encounter any issues or have suggestions, feel free to open an issue.
