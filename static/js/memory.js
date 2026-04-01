const animals = [
    { name: "Chien", image: "chien.png" },
    { name: "Chat", image: "chat.png" },
    { name: "Chiot", image: "chiot.png" },
    { name: "Chaton", image: "chaton.png" },
    { name: "Oiseau", image: "oiseau.png" },
    { name: "Poisson", image: "poisson.png" }
];

let flippedCards = [];
let matchedCards = [];

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

const grid = document.querySelector('.memory-grid');
const restartButton = document.querySelector('.memory-restart');
const winMessage = document.createElement('div');
winMessage.classList.add('memory-win-message');
winMessage.style.display = 'none';
winMessage.innerHTML = "Gagné ! 🎉🐶🐱";

restartButton.parentNode.insertBefore(winMessage, restartButton);

function createBoard() {
    grid.innerHTML = '';
    winMessage.style.display = 'none';
    flippedCards = [];
    matchedCards = [];
    
    const shuffledAnimals = shuffleArray(animals.concat(animals));

    shuffledAnimals.forEach((animal) => {
        const card = document.createElement('div');
        card.classList.add('memory-card');
        card.setAttribute('data-name', animal.name);

        const front = document.createElement('div');
        front.classList.add('front');

        const back = document.createElement('div');
        back.classList.add('back');
        const img = document.createElement('img');
        img.src = `/static/images/${animal.image}`;
        back.appendChild(img);

        card.appendChild(front);
        card.appendChild(back);
        grid.appendChild(card);

        card.addEventListener('click', () => {
            if (flippedCards.length < 2 && !card.classList.contains('flipped') && !matchedCards.includes(card)) {
                card.classList.add('flipped');
                flippedCards.push(card);

                if (flippedCards.length === 2) {
                    checkMatch();
                }
            }
        });
    });
}

function checkMatch() {
    const [firstCard, secondCard] = flippedCards;

    if (firstCard.dataset.name === secondCard.dataset.name) {
        matchedCards.push(firstCard, secondCard);
        flippedCards = [];

        if (matchedCards.length === animals.length * 2) {
            setTimeout(() => {
                winMessage.style.display = 'block';
            }, 500);
        }
    } else {
        setTimeout(() => {
            firstCard.classList.remove('flipped');
            secondCard.classList.remove('flipped');
            flippedCards = [];
        }, 1000);
    }
}

restartButton.addEventListener('click', createBoard);

createBoard();
