const allQuestions = [
    // Animal Welfare
    { question: "Quelle est la température corporelle normale d'un chien ?", options: ["37°C", "38-39°C", "40-41°C"], answer: ["38-39°C"] },
    { question: "Quel signe indique qu'un chat est détendu ?", options: ["Queue qui fouette", "Ronronnements", "Oreilles aplaties"], answer: ["Ronronnements"] },
    { question: "Pourquoi est-il important de stériliser son animal ?", options: ["Éviter les maladies", "Contrôler la population animale", "Les deux"], answer: ["Les deux"] },
    { question: "Quel est le meilleur endroit pour adopter un animal ?", options: ["Refuge", "Animalerie", "Élevage intensif"], answer: ["Refuge"] },
    { question: "Quelle est la meilleure façon d’approcher un chien inconnu ?", options: ["Le regarder droit dans les yeux", "S’accroupir et l’appeler doucement", "Tendre directement la main"], answer: ["S’accroupir et l’appeler doucement"] },
    { question: "Quel est l'aliment idéal pour un chien adulte ?", options: ["Croquettes", "Aliments faits maison", "Aliments pour chats"], answer: ["Croquettes"] },
    { question: "Les chats ont-ils besoin de sortir tous les jours ?", options: ["Oui", "Non", "Seulement s'ils sont en cage"], answer: ["Non"] },
    { question: "Quelle est la durée de vie moyenne d’un chien ?", options: ["6-8 ans", "10-15 ans", "15-20 ans"], answer: ["10-15 ans"] },
    { question: "Pourquoi les chiens aiment-ils courir ?", options: ["Par instinct", "Parce qu'ils sont excités", "Ils n'aiment pas être en laisse"], answer: ["Par instinct"] },
    { question: "Quelle est la meilleure façon de dresser un chien ?", options: ["Punir les mauvais comportements", "Utiliser des récompenses", "L'ignorer quand il fait quelque chose de mal"], answer: ["Utiliser des récompenses"] },

    // Awareness of Abandonment
    { question: "Combien d'animaux sont abandonnés chaque année en France ?", options: ["50 000", "100 000", "200 000"], answer: ["100 000"] },
    { question: "Que faire si vous trouvez un chien errant ?", options: ["L'ignorer", "Prévenir un refuge ou la mairie", "L'emmener chez vous immédiatement"], answer: ["Prévenir un refuge ou la mairie"] },
    { question: "Quelle période de l'année connaît le plus d'abandons ?", options: ["Noël", "Été", "Rentrée scolaire"], answer: ["Été"] },
    { question: "Pourquoi les refuges sont souvent saturés ?", options: ["Manque de stérilisation", "Abandons massifs", "Les deux"], answer: ["Les deux"] },
    { question: "Que signifie 'adopter, c'est s'engager' ?", options: ["Adopter un animal pour quelques mois", "S'occuper de lui toute sa vie", "Laisser l'animal dehors"], answer: ["S'occuper de lui toute sa vie"] },
    { question: "Un animal adopté peut-il être retourné après une période d’essai ?", options: ["Oui", "Non", "Cela dépend de l’animal"], answer: ["Non"] },
    { question: "Quelles sont les conséquences d'un abandon d'animal ?", options: ["L'animal est souvent perdu", "L'animal souffre physiquement et émotionnellement", "Aucune conséquence"], answer: ["L'animal souffre physiquement et émotionnellement"] },
    { question: "Les abandons d'animaux augmentent-ils pendant les vacances ?", options: ["Oui", "Non", "Cela n’a pas d’impact"], answer: ["Oui"] },
    { question: "Pourquoi l’adoption dans un refuge est-elle bénéfique ?", options: ["On sauve une vie", "On paye moins cher", "On choisit les animaux"], answer: ["On sauve une vie"] },
    { question: "Est-ce que les refuges peuvent adopter tous les animaux ?", options: ["Oui", "Non", "Cela dépend des dons"], answer: ["Non"] },

    // Animal Health
    { question: "Quel aliment est toxique pour les chiens ?", options: ["Carottes", "Chocolat", "Riz"], answer: ["Chocolat"] },
    { question: "Quelle est la durée moyenne de gestation d'une chatte ?", options: ["30 jours", "63-65 jours", "90 jours"], answer: ["63-65 jours"] },
    { question: "Pourquoi est-il important de vacciner son animal ?", options: ["Pour éviter les maladies", "Pour le plaisir", "Ce n’est pas nécessaire"], answer: ["Pour éviter les maladies"] },
    { question: "Quel signe peut indiquer qu'un chien est malade ?", options: ["Il joue plus", "Il mange moins", "Il aboie beaucoup"], answer: ["Il mange moins"] },
    { question: "Que faire si votre chat a des puces ?", options: ["Rien", "Le laver avec un shampoing anti-puces", "Attendre que ça passe"], answer: ["Le laver avec un shampoing anti-puces"] },
    { question: "Les chiens peuvent-ils souffrir de dépression ?", options: ["Oui", "Non", "Seulement les petites races"], answer: ["Oui"] },
    { question: "Est-il nécessaire de donner des vitamines aux animaux ?", options: ["Oui, si leur régime alimentaire est déséquilibré", "Non, ils se débrouillent très bien", "Seulement aux vieux animaux"], answer: ["Oui, si leur régime alimentaire est déséquilibré"] },
    { question: "Quand doit-on emmener un animal chez le vétérinaire ?", options: ["Tous les ans", "Quand il est malade", "Seulement en cas d’urgence"], answer: ["Quand il est malade"] },
    { question: "Quel vaccin est essentiel pour un chiot ?", options: ["Le vaccin contre la rage", "Le vaccin contre la parvovirose", "Le vaccin contre la toux de chenil"], answer: ["Le vaccin contre la parvovirose"] },
    { question: "Les chats peuvent-ils vivre à l'extérieur ?", options: ["Oui, tout le temps", "Non, ils doivent rester à l'intérieur", "Oui, mais pas trop souvent"], answer: ["Oui, mais pas trop souvent"] },

    // General Knowledge about Dogs and Cats
    { question: "Quelle est l'espérance de vie moyenne d'un chat ?", options: ["5-8 ans", "10-15 ans", "20-25 ans"], answer: ["10-15 ans"] },
    { question: "Pourquoi les chiens reniflent-ils souvent les autres chiens ?", options: ["Par curiosité", "Pour communiquer", "Par faim"], answer: ["Pour communiquer"] },
    { question: "Quel est le sens le plus développé chez le chien ?", options: ["L'ouïe", "La vue", "L'odorat"], answer: ["L'odorat"] },
    { question: "Combien de paupières a un chat ?", options: ["Deux", "Trois", "Quatre"], answer: ["Trois"] },
    { question: "Pourquoi les chats dorment-ils autant ?", options: ["Parce qu'ils sont paresseux", "Pour récupérer leur énergie", "Par ennui"], answer: ["Pour récupérer leur énergie"] },
    { question: "Quelle est la principale raison pour laquelle un chien aboie ?", options: ["Pour prévenir un danger", "Pour communiquer", "Pour jouer"], answer: ["Pour prévenir un danger"] },
    { question: "Les chats sont-ils toujours indépendants ?", options: ["Oui", "Non", "Cela dépend du chat"], answer: ["Cela dépend du chat"] },
    { question: "Les chiens peuvent-ils apprendre à parler ?", options: ["Oui", "Non", "Ils peuvent imiter des sons"], answer: ["Ils peuvent imiter des sons"] },
    { question: "Quel est le temps moyen qu'un chien peut passer seul à la maison ?", options: ["3-4 heures", "10 heures", "Aucune limite"], answer: ["3-4 heures"] },
    { question: "Les chats peuvent-ils être dressés ?", options: ["Oui", "Non", "Seulement pour des tricks simples"], answer: ["Oui"] }
];

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

const selectedQuestions = shuffleArray(allQuestions).slice(0, 10);

const questionContainer = document.querySelector('.quiz-question');
const optionsContainer = document.querySelector('.quiz-options');
const checkButton = document.querySelector('.quiz-check');
const nextButton = document.querySelector('.quiz-next');
const submitButton = document.querySelector('.quiz-submit');
const scoreContainer = document.querySelector('.quiz-score');
const scoreValue = document.querySelector('.score-value');

let currentQuestionIndex = 0;
let answered = false;
let score = 0;

function displayQuestion() {
    const question = selectedQuestions[currentQuestionIndex];
    questionContainer.textContent = question.question;

    optionsContainer.innerHTML = ''; 
    answered = false;
    
    checkButton.style.display = 'block';
    nextButton.style.display = 'none';
    submitButton.style.display = 'none';

    const progressBar = document.querySelector('.quiz-progress-bar');
    progressBar.style.width = `${(currentQuestionIndex / selectedQuestions.length) * 100}%`;

    question.options.forEach(option => {
        const optionElement = document.createElement('div');
        optionElement.classList.add('quiz-option');
        optionElement.textContent = option;
        optionsContainer.appendChild(optionElement);

        optionElement.addEventListener('click', () => {
            if (!answered) {
                optionElement.classList.toggle('selected'); 
            }
        });
    });
}

nextButton.addEventListener('click', () => {
    if (currentQuestionIndex < selectedQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();

        const progressBar = document.querySelector('.quiz-progress-bar');
        progressBar.style.width = `${(currentQuestionIndex / selectedQuestions.length) * 100}%`;
    }
});

checkButton.addEventListener('click', () => {
    if (answered) return;

    const question = selectedQuestions[currentQuestionIndex];
    const selectedOptions = document.querySelectorAll('.quiz-option.selected');

    if (selectedOptions.length === 0) return;

    answered = true;
    checkButton.style.display = 'none';
    
    if (currentQuestionIndex === selectedQuestions.length - 1) {
        submitButton.style.display = 'block';
    } else {
        nextButton.style.display = 'block';
    }

    let correctAnswers = 0;
    selectedOptions.forEach(option => {
        if (question.answer.includes(option.textContent)) {
            option.classList.add('correct');
            correctAnswers++;
        } else {
            option.classList.add('incorrect');
        }
    });

    document.querySelectorAll('.quiz-option').forEach(option => {
        if (question.answer.includes(option.textContent)) {
            option.classList.add('correct');
        }
    });

    if (correctAnswers === question.answer.length) {
        score++; 
    }

    const progressBar = document.querySelector('.quiz-progress-bar');
    progressBar.style.width = `${((currentQuestionIndex + 1) / selectedQuestions.length) * 100}%`;
});


displayQuestion();

submitButton.addEventListener('click', () => {
    scoreContainer.style.display = 'block';

    scoreValue.textContent = `Quiz terminé ! Votre score est de ${score} sur ${selectedQuestions.length}.`;

    checkButton.style.display = 'none';
    nextButton.style.display = 'none';
    submitButton.style.display = 'none';

    let message = "";
    if (score === selectedQuestions.length) {
        message = "Félicitations ! Vous avez tout juste 🎉";
    } else if (score > selectedQuestions.length / 2) {
        message = "Bien joué ! Vous avez un bon score 👍";
    } else {
        message = "Vous pouvez faire mieux, réessayez ! 😊";
    }

    const finalMessage = document.createElement('div');
    finalMessage.classList.add('quiz-final-message');
    finalMessage.textContent = message;

    const existingMessage = scoreContainer.querySelector('.quiz-final-message');
    if (existingMessage) {
        existingMessage.textContent = message;
    } else {
        scoreContainer.appendChild(finalMessage);
    }
});
