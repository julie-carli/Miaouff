const questions = [
    { question: "Quel est l'animal le plus rapide ?", options: ['Guépard', 'Lion', 'Aigle', 'Chien'], answer: 'Guépard' },
    { question: "Quel est l'animal national de l'Australie ?", options: ['Koala', 'Kangourou', 'Émeu', 'Dingo'], answer: 'Kangourou' },
    { question: "Quel est le cri du chien ?", options: ['Miaou', 'Aboie', 'Rugir', 'Bêler'], answer: 'Aboie' },
    { question: "Combien de pattes a un chat ?", options: ['2', '4', '6', '8'], answer: '4' },
    { question: "Quel animal vit dans une ruche ?", options: ['Abeille', 'Papillon', 'Cicada', 'Moustique'], answer: 'Abeille' },
    { question: "Quel est le petit du cheval ?", options: ['Poulain', 'Veau', 'Agneau', 'Chiot'], answer: 'Poulain' },
    { question: "Quel est le plus grand mammifère terrestre ?", options: ['Girafe', 'Éléphant', 'Baleine', 'Rhinocéros'], answer: 'Éléphant' },
    { question: "Quel animal a une trompe ?", options: ['Elephant', 'Chameau', 'Koala', 'Ours'], answer: 'Elephant' },
    { question: "Quel animal est surnommé le roi de la jungle ?", options: ['Lion', 'Tigre', 'Jaguar', 'Panthère'], answer: 'Lion' },
    { question: "Quel animal est connu pour sa lenteur ?", options: ['Tortue', 'Paresseux', 'Koala', 'Écureuil'], answer: 'Tortue' }
];

let currentQuestionIndex = 0;
let score = 0;
let timeLeft = 60;
let timer;
let isGameActive = false;
let canCheckAnswer = true;

function startGame() {
    currentQuestionIndex = 0;
    score = 0;
    timeLeft = 60;
    isGameActive = true;
    canCheckAnswer = true;
    document.querySelector('#restart').style.display = 'none';
    document.querySelector('#score').textContent = score;
    document.querySelector('#timer').textContent = timeLeft;
    loadNextQuestion();
    startTimer();
}

function loadNextQuestion() {
    if (currentQuestionIndex >= questions.length || timeLeft <= 0) {
        endGame();
        return;
    }

    const currentQuestion = questions[currentQuestionIndex];
    document.querySelector('#question').textContent = currentQuestion.question;

    const shuffledOptions = shuffleArray(currentQuestion.options);

    const optionsButtons = document.querySelectorAll('.rapido-option');
    optionsButtons.forEach((button, index) => {
        button.textContent = shuffledOptions[index];
        button.onclick = () => checkAnswer(shuffledOptions[index], currentQuestion.answer);
    });

    currentQuestionIndex++;
}

function shuffleArray(array) {
    let shuffledArray = array.slice();
    for (let i = shuffledArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
    }
    return shuffledArray;
}

function startTimer() {
    timer = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            document.querySelector('#timer').textContent = timeLeft;
        } else {
            clearInterval(timer);
            endGame();
        }
    }, 1000);
}

function checkAnswer(answer, correctAnswer) {
    if (!canCheckAnswer) return;
    
    if (answer === correctAnswer) {
        score++;
        document.querySelector('#score').textContent = score;
    }

    loadNextQuestion();
}

function endGame() {
    isGameActive = false;
    canCheckAnswer = false;
    clearInterval(timer);
    document.querySelector('#restart').style.display = 'block';
}

startGame();
