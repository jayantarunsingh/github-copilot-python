import random
import sudoku_logic


def test_generated_puzzle_has_unique_solution_seed0():
    random.seed(0)
    puzzle, solution = sudoku_logic.generate_puzzle(clues=30)
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_generated_puzzle_has_unique_solution_seed1():
    random.seed(1)
    puzzle, _ = sudoku_logic.generate_puzzle(clues=28)
    assert sudoku_logic.count_solutions(puzzle) == 1
