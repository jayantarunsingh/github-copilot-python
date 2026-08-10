// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let gameComplete = false;

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        if (gameComplete) {
          e.target.value = '';
          return;
        }
        let val = e.target.value.replace(/[^1-9]/g, '');
        if (val.length > 1) {
          val = val.charAt(0);
        }
        e.target.value = val;
        e.target.className = 'sudoku-cell';
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function updateTimerDisplay() {
  const minutes = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
  const seconds = String(elapsedSeconds % 60).padStart(2, '0');
  document.getElementById('timer').innerText = `Time: ${minutes}:${seconds}`;
}

function resetTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function startTimer() {
  stopTimer();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function setMessage(text, color = '#333') {
  const msg = document.getElementById('message');
  msg.style.color = color;
  msg.innerText = text;
}

function getBoardState() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function hasEmptyCells(board) {
  return board.some(row => row.some(cell => cell === 0));
}

function disableBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (const inp of inputs) {
    inp.disabled = true;
  }
}

function clearIncorrectHighlights() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (const inp of inputs) {
    if (!inp.disabled) {
      inp.className = 'sudoku-cell';
    }
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className = 'sudoku-cell prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.className = 'sudoku-cell';
      }
    }
  }
}

function updateHints() {
  document.getElementById('hints-used').innerText = `Hints: ${hintsUsed}`;
}

async function newGame() {
  gameComplete = false;
  hintsUsed = 0;
  updateHints();
  setMessage('');
  resetTimer();
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  startTimer();
}

async function checkSolution() {
  if (gameComplete) {
    return;
  }
  const board = getBoardState();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    setMessage(data.error, '#d32f2f');
    return;
  }
  clearIncorrectHighlights();
  const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    if (!hasEmptyCells(board)) {
      setMessage('Congratulations! You solved it!', '#388e3c');
      stopTimer();
      disableBoard();
      gameComplete = true;
      return;
    }
    setMessage('So far so good! Keep going.', '#1976d2');
  } else {
    setMessage('Some cells are incorrect.', '#d32f2f');
  }
}

async function requestHint() {
  if (gameComplete) {
    return;
  }
  const board = getBoardState();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    setMessage(data.error, '#d32f2f');
    return;
  }
  const index = data.row * SIZE + data.col;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const inp = inputs[index];
  inp.value = data.value;
  inp.disabled = true;
  inp.className = 'sudoku-cell prefilled';
  hintsUsed += 1;
  updateHints();
  setMessage('Hint applied.', '#1976d2');
  const nextBoard = getBoardState();
  if (!hasEmptyCells(nextBoard)) {
    await checkSolution();
  }
}

window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-button').addEventListener('click', requestHint);
  newGame();
});
