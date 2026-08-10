import random
import pytest
import sudoku_logic


def count_non_empty(board):
    return sum(1 for r in board for v in r if v != sudoku_logic.EMPTY)


@pytest.mark.parametrize(
    'difficulty,expected_clues',
    [
        ('easy', 40),
        ('medium', 32),
        ('hard', 26),
    ],
)
def test_generate_puzzle_difficulty_clue_counts(difficulty, expected_clues):
    random.seed(42)
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)
    assert count_non_empty(puzzle) == expected_clues
    assert sudoku_logic.count_solutions(puzzle) == 1
    assert all(v != sudoku_logic.EMPTY for row in solution for v in row)
