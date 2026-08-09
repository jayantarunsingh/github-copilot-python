import random
import sudoku_logic
import pytest


def count_non_empty(board):
    return sum(1 for r in board for v in r if v != sudoku_logic.EMPTY)


def test_create_empty_board():
    b = sudoku_logic.create_empty_board()
    assert len(b) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in b)
    assert all(v == sudoku_logic.EMPTY for row in b for v in row)


def test_generate_puzzle_and_solution_shapes_and_counts():
    random.seed(0)
    puzzle, solution = sudoku_logic.generate_puzzle(clues=30)
    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    # solution must be fully filled
    assert all(v != sudoku_logic.EMPTY for row in solution for v in row)
    # puzzle must have exactly requested clues
    assert count_non_empty(puzzle) == 30


def _is_valid_solution(sol):
    SIZE = sudoku_logic.SIZE
    numbers = set(range(1, SIZE + 1))
    # rows
    for row in sol:
        if set(row) != numbers:
            return False
    # cols
    for c in range(SIZE):
        col = [sol[r][c] for r in range(SIZE)]
        if set(col) != numbers:
            return False
    # 3x3 boxes
    for br in range(0, SIZE, 3):
        for bc in range(0, SIZE, 3):
            box = [sol[br + r][bc + c] for r in range(3) for c in range(3)]
            if set(box) != numbers:
                return False
    return True


def test_fill_board_produces_valid_solution():
    random.seed(1)
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board) is True
    assert _is_valid_solution(board)


def test_remove_cells_reduces_to_clues():
    random.seed(2)
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)
    sudoku_logic.remove_cells(board, clues=25)
    assert count_non_empty(board) == 25
