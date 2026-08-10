# Flask Sudoku

## Project Overview

Flask Sudoku is a browser-based Sudoku game built with Python and Flask. The application generates Sudoku puzzles with easy, medium, and hard difficulty levels, ensures puzzles have a unique solution, and provides interactive gameplay with hints, validation, a timer, and a top 10 scoreboard.

## Features

- Easy, Medium, Hard difficulty
- Unique Sudoku solution generation
- Prefilled / locked cells for the starting puzzle
- Real-time input validation for cell entries
- Check Solution button to identify incorrect entries
- Hint button to fill one empty cell from the solution
- Timer to track how long the current game has been played
- Completion detection when the puzzle is solved correctly
- Top 10 scoreboard for completed games
- Player name input for scoreboard entries
- Browser localStorage persistence for scoreboard and dark mode preference
- Dark Mode support
- Alternating 3x3 box styling for better visual separation
- Responsive design for smaller screens

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- pytest

## Project Structure

- `app.py` — Flask application and API routes for new game, solution checks, and hints
- `sudoku_logic.py` — Sudoku puzzle generation, unique-solution enforcement, and solver utilities
- `templates/index.html` — main front-end page
- `static/main.js` — client-side game UI, timer, hint handling, localStorage, scoreboard, and dark mode
- `static/styles.css` — styling, layout, dark mode, alternating boxes, and responsive behavior
- `requirements.txt` — Python dependencies
- `tests/` — pytest test suite for app routes and Sudoku logic

## Setup Instructions (Windows PowerShell)

1. Open PowerShell in the project root directory:

```powershell
cd C:\Users\singh\github-copilot-python\starter
```

2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Flask Application

With the virtual environment active, start the app with:

```powershell
python app.py
```

Then open the application in your browser at:

```text
http://127.0.0.1:5000
```

## Running Tests

Run the test suite from the project root with:

```powershell
pytest
```

## Browser Usage Notes

- The game opens in the browser and loads a new Sudoku puzzle on start.
- Use the difficulty selector, player name input, and controls for New Game, Check Solution, and Hint.
- The scoreboard updates when a puzzle is completed correctly.
- Scoreboard data and dark mode preference are stored in browser `localStorage` so they persist between page reloads.

## Testing

Baseline tests cover the Flask routes and Sudoku generator logic, including:

- Index route rendering
- New game route returning puzzles and setting current game state
- Difficulty-based clue counts for easy, medium, and hard puzzles
- Unique solution generation validation
- Check solution route behavior for correct and incorrect boards
- Hint route behavior for valid games and error cases

Feature tests validate user-facing behaviors such as:

- Puzzle generation with difficulty levels
- Unique-solution enforcement
- Scoreboard persistence in browser localStorage
- Dark mode preference persistence in browser localStorage

## GitHub Copilot

GitHub Copilot was used throughout development for inspection, testing, refactoring, feature development, and debugging. Copilot helped identify implementation details, validate behavior, and keep documentation aligned with the completed project.
