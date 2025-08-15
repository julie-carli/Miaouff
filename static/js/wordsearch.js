const words = ["CHIEN", "CHAT", "LAPIN", "OISEAU", "PANDA", "TIGRE", "ZEBRE"];
const gridSize = 10;
let grid = [];
let selectedCells = [];
let foundWords = [];
let isMouseDown = false;
let startCell = null;

function createGrid() {
    grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(''));
    selectedCells = [];
    foundWords = [];
    document.getElementById("win-message").style.display = "none";
    placeWords();
    fillEmptyCells();
    renderGrid();
    updateWordList();
}

let highlightColor = "rgba(255, 255, 0, 0.5)";

function renderColorPalette() {
    const palette = document.querySelector('.wordsearch-colors');
    palette.innerHTML = ''; 

    const colors = {
        yellow: "rgba(255, 255, 0, 0.5)",
        blue: "rgba(0, 0, 255, 0.5)",
        green: "rgba(0, 255, 0, 0.5)",
        red: "rgba(255, 0, 0, 0.5)",
        cyan: "rgba(0, 255, 255, 0.5)",
        magenta: "rgba(255, 0, 255, 0.5)"
    };
    
    Object.entries(colors).forEach(([colorName, rgbaValue]) => {
        const colorBox = document.createElement('div');
        colorBox.classList.add('color-box');
        colorBox.style.backgroundColor = rgbaValue;

        if (rgbaValue === highlightColor) {
            colorBox.classList.add('selected-color');
        }

        colorBox.addEventListener('click', () => {
            document.querySelectorAll('.color-box').forEach(box => box.classList.remove('selected-color'));
            colorBox.classList.add('selected-color');
            highlightColor = rgbaValue; 
        });

        palette.appendChild(colorBox);
    });
}

function placeWords() {
    words.forEach(word => {
        let placed = false, attempts = 0;
        while (!placed && attempts < 20) {
            const directions = ["H", "V", "D1", "D2"];
            const direction = directions[Math.floor(Math.random() * directions.length)];
            const row = Math.floor(Math.random() * gridSize);
            const col = Math.floor(Math.random() * gridSize);
            if (canPlaceWord(word, row, col, direction)) {
                placeWord(word, row, col, direction);
                placed = true;
            }
            attempts++;
        }
    });
}

function canPlaceWord(word, row, col, dir) {
    if (dir === "H" && col + word.length > gridSize) return false;
    if (dir === "V" && row + word.length > gridSize) return false;
    if (dir === "D1" && (row + word.length > gridSize || col + word.length > gridSize)) return false;
    if (dir === "D2" && (row + word.length > gridSize || col - word.length < 0)) return false;

    return ![...word].some((_, i) => {
        if (dir === "H") return grid[row][col + i];
        if (dir === "V") return grid[row + i][col];
        if (dir === "D1") return grid[row + i][col + i];
        if (dir === "D2") return grid[row + i][col - i];
    });
}

function placeWord(word, row, col, dir) {
    for (let i = 0; i < word.length; i++) {
        if (dir === "H") grid[row][col + i] = word[i];
        if (dir === "V") grid[row + i][col] = word[i];
        if (dir === "D1") grid[row + i][col + i] = word[i];
        if (dir === "D2") grid[row + i][col - i] = word[i];
    }
}

function fillEmptyCells() {
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            if (!grid[row][col]) {
                grid[row][col] = String.fromCharCode(65 + Math.floor(Math.random() * 26)); 
            }
        }
    }
}

function renderGrid() {
    const gridContainer = document.querySelector('.wordsearch-grid');
    gridContainer.innerHTML = '';
    gridContainer.style.gridTemplateColumns = `repeat(${gridSize}, 40px)`;

    grid.flat().forEach((letter, index) => {
        const cell = document.createElement('div');
        cell.classList.add('wordsearch-cell');
        cell.textContent = letter;
        cell.dataset.index = index;
        gridContainer.appendChild(cell);
    });

    addSelectionEvents();
}

function addSelectionEvents() {
    const cells = document.querySelectorAll('.wordsearch-cell');
    
    cells.forEach(cell => {
        cell.addEventListener('mousedown', (e) => {
            isMouseDown = true;
            startCell = e.target;
            selectedCells = [e.target];
            e.target.style.backgroundColor = highlightColor;
            e.preventDefault();
        });

        cell.addEventListener('mouseover', (e) => {
            if (isMouseDown && startCell) {
                highlightPath(startCell, e.target);
            }
        });
    });

    document.addEventListener('mouseup', () => {
        if (isMouseDown) checkWord();
        isMouseDown = false;
    });
}

function highlightPath(start, end) {
    const grid = document.querySelector('.wordsearch-grid');
    const cells = Array.from(grid.children);
    const startIdx = Number(start.dataset.index);
    const endIdx = Number(end.dataset.index);

    selectedCells.forEach(cell => {
        cell.style.backgroundColor = "";
    });

    selectedCells = [];

    const dx = Math.sign((endIdx % gridSize) - (startIdx % gridSize));
    const dy = Math.sign(Math.floor(endIdx / gridSize) - Math.floor(startIdx / gridSize));

    let x = startIdx % gridSize, y = Math.floor(startIdx / gridSize);
    while (x !== (endIdx % gridSize) + dx || y !== Math.floor(endIdx / gridSize) + dy) {
        if (x < 0 || y < 0 || x >= gridSize || y >= gridSize) break;

        const index = y * gridSize + x;
        const cell = cells[index];

        if (cell) {
            selectedCells.push(cell);
            cell.style.backgroundColor = highlightColor;
        }

        x += dx;
        y += dy;
    }
}

function checkWin() {
    if (foundWords.length === words.length) {
        const winMessage = document.getElementById("win-message");
        winMessage.textContent = "🎉 Bravo, tu as gagné ! 🎉";
        winMessage.style.display = "block";
    }
}

function checkWord() {
    let word = selectedCells.map(cell => cell.textContent).join('');
    let reverseWord = word.split('').reverse().join('');

    if (words.includes(word) || words.includes(reverseWord)) {
        selectedCells.forEach(cell => {
            cell.classList.add('wordsearch-found');
            cell.style.backgroundColor = highlightColor;
        });

        foundWords.push(word);
        updateWordList();
        checkWin(); 
    } else {
        selectedCells.forEach(cell => cell.style.backgroundColor = "");
    }
}

function updateWordList() {
    const wordList = document.querySelector('.wordsearch-wordlist');
    wordList.innerHTML = '';
    words.forEach(word => {
        const li = document.createElement('li');
        li.textContent = word;
        if (foundWords.includes(word)) {
            li.style.textDecoration = "line-through";
            li.style.color = "gray";
        }
        wordList.appendChild(li);
    });
}

document.querySelector('.wordsearch-restart').addEventListener('click', createGrid);
createGrid();
renderColorPalette();
