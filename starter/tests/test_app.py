import random
import app as sudoku_app_module


def client():
    return sudoku_app_module.app.test_client()


def test_index_route():
    res = client().get('/')
    assert res.status_code == 200
    # basic sanity: HTML returned
    assert b'<' in res.data


def test_new_game_route_sets_current_and_returns_puzzle():
    random.seed(0)
    res = client().get('/new?clues=28')
    assert res.status_code == 200
    data = res.get_json()
    puzzle = data.get('puzzle')
    assert puzzle is not None
    assert len(puzzle) == sudoku_app_module.sudoku_logic.SIZE
    # CURRENT should be populated
    assert sudoku_app_module.CURRENT['puzzle'] == puzzle
    assert sudoku_app_module.CURRENT['solution'] is not None
    non_empty = sum(1 for row in puzzle for v in row if v != sudoku_app_module.sudoku_logic.EMPTY)
    assert non_empty == 28


def test_new_game_route_with_difficulty_sets_expected_clues():
    random.seed(0)
    res = client().get('/new?difficulty=easy')
    assert res.status_code == 200
    data = res.get_json()
    puzzle = data.get('puzzle')
    assert puzzle is not None
    assert len(puzzle) == sudoku_app_module.sudoku_logic.SIZE
    non_empty = sum(1 for row in puzzle for v in row if v != sudoku_app_module.sudoku_logic.EMPTY)
    assert non_empty == sudoku_app_module.sudoku_logic.DIFFICULTY_CLUES['easy']


def test_check_solution_success_and_failure():
    random.seed(3)
    client().get('/new?clues=35')
    solution = sudoku_app_module.CURRENT['solution']
    # correct board => no incorrect cells
    res_ok = client().post('/check', json={'board': solution})
    assert res_ok.status_code == 200
    assert res_ok.get_json()['incorrect'] == []
    # modify one cell => that cell reported incorrect
    bad = [row.copy() for row in solution]
    bad[0][0] = (bad[0][0] % 9) + 1
    res_bad = client().post('/check', json={'board': bad})
    assert res_bad.status_code == 200
    incorrect = res_bad.get_json()['incorrect']
    assert [0, 0] in incorrect


def test_check_no_game_in_progress():
    sudoku_app_module.CURRENT['solution'] = None
    empty_board = sudoku_app_module.sudoku_logic.create_empty_board()
    res = client().post('/check', json={'board': empty_board})
    assert res.status_code == 400
    assert 'error' in res.get_json()
