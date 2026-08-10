import copy
import random

SIZE = 9
EMPTY = 0

DIFFICULTY_CLUES = {
    'easy': 40,
    'medium': 32,
    'hard': 26,
}

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    # Remove cells while ensuring the resulting puzzle has exactly one solution.
    to_remove = SIZE * SIZE - clues
    removed = 0

    # Helper: try removing cells in random order and only keep removal
    # when the puzzle still has exactly one solution.
    positions = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    # Keep attempting passes until we've removed enough or no progress
    # can be made (to avoid infinite loops).
    while removed < to_remove:
        random.shuffle(positions)
        progress = False
        for row, col in positions:
            if removed >= to_remove:
                break
            if board[row][col] == EMPTY:
                continue
            backup = board[row][col]
            board[row][col] = EMPTY
            sols = count_solutions(board)
            if sols == 1:
                removed += 1
                progress = True
            else:
                board[row][col] = backup
        if not progress:
            # No further unique-preserving removals possible
            break

def get_clues_for_difficulty(difficulty):
    if difficulty is None:
        raise ValueError('Difficulty must be provided')
    if not isinstance(difficulty, str):
        raise TypeError('Difficulty must be a string')
    normalized = difficulty.strip().lower()
    if normalized not in DIFFICULTY_CLUES:
        raise ValueError(
            f"Unknown difficulty '{difficulty}'. Valid options are: {', '.join(DIFFICULTY_CLUES)}"
        )
    return DIFFICULTY_CLUES[normalized]


def generate_puzzle(clues=35, difficulty=None):
    if difficulty is not None:
        clues = get_clues_for_difficulty(difficulty)
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution


def count_solutions(board, limit=2):
    """
    Count the number of solutions for the given Sudoku `board` using
    backtracking. Stop early when `limit` solutions are found.

    Returns an integer: 0, 1, or >=2 (bounded by limit).
    """
    b = deep_copy(board)
    solutions = 0

    def find_empty(cell_board):
        for r in range(SIZE):
            for c in range(SIZE):
                if cell_board[r][c] == EMPTY:
                    return r, c
        return None

    def backtrack():
        nonlocal solutions
        if solutions >= limit:
            return
        empty = find_empty(b)
        if not empty:
            solutions += 1
            return
        r, c = empty
        for num in range(1, SIZE + 1):
            if is_safe(b, r, c, num):
                b[r][c] = num
                backtrack()
                b[r][c] = EMPTY
                if solutions >= limit:
                    return

    backtrack()
    return solutions
