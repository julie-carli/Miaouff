const words = ["chien", "chat", "hamster", "oiseau", "tigre", "lion", "panda", "koala", "lapin", "poisson"];
let wordToGuess = '';
let guessedLetters = [];
let wrongGuesses = 0;
const maxWrongGuesses = 6;

const wordDisplay = document.querySelector('.hangman-word');
const hangmanImage = document.querySelector('.hangman-container img');
const guessesDisplay = document.querySelector('.hangman-guesses');
const letterInput = document.querySelector('.hangman-letter');
const guessButton = document.querySelector('.hangman-guess');
const restartButton = document.querySelector('.hangman-restart');
const messageDisplay = document.createElement('div'); 
messageDisplay.classList.add('hangman-message');
document.querySelector('.hangman-game').appendChild(messageDisplay); 

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function initializeGame() {
    wordToGuess = getRandomWord();
    guessedLetters = [];
    wrongGuesses = 0;
    letterInput.value = '';
    guessesDisplay.textContent = '';
    messageDisplay.textContent = '';
    updateWordDisplay();
    updateHangmanDisplay();
    disableInputs(false);
    restartButton.style.display = "none";
}

function updateWordDisplay() {
    wordDisplay.innerHTML = wordToGuess
        .split('')
        .map(letter => guessedLetters.includes(letter) ? letter : '_')
        .join(' ');
}

function updateHangmanDisplay() {
    hangmanImage.src = `/static/images/${wrongGuesses}-hangman.png`;
}

function checkWin() {
    if (wordToGuess.split('').every(letter => guessedLetters.includes(letter))) {
        messageDisplay.textContent = "🎉 Gagné ! 🎉";
        disableInputs(true);
        restartButton.style.display = "block";
    }
}

function checkLoss() {
    if (wrongGuesses >= maxWrongGuesses) {
        messageDisplay.textContent = `😢 Perdu ! Le mot était : ${wordToGuess}`;
        disableInputs(true);
        restartButton.style.display = "block";
    }
}

function disableInputs(state) {
    letterInput.disabled = state;
    guessButton.disabled = state;
}

guessButton.addEventListener('click', () => {
    const letter = letterInput.value.toLowerCase().trim();

    if (letter && !guessedLetters.includes(letter)) {
        guessedLetters.push(letter);

        if (wordToGuess.includes(letter)) {
            updateWordDisplay();
            checkWin();
        } else {
            wrongGuesses++;
            updateHangmanDisplay();
            checkLoss();
        }
    }
    letterInput.value = '';
});

letterInput.addEventListener('input', function () {
    this.value = this.value.replace(/[^a-zA-Z]/g, '').toLowerCase();
});

restartButton.addEventListener('click', initializeGame);
initializeGame();
