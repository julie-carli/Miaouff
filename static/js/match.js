const wordDefinitionPairs = [
    { word: "Chien", definition: "Animal domestique fidèle, souvent considéré comme le meilleur ami de l'homme." },
    { word: "Chat", definition: "Animal domestique indépendant, apprécié pour sa compagnie et sa capacité à chasser les souris." },
    { word: "Lapin", definition: "Petit mammifère herbivore connu pour ses grandes oreilles et sa rapidité." },
    { word: "Poisson", definition: "Animal aquatique à nageoires, souvent gardé comme animal de compagnie." },
    { word: "Oiseau", definition: "Animal à plumes, connu pour sa capacité à voler et à chanter." },
    { word: "Hamster", definition: "Petit rongeur souvent utilisé comme animal de compagnie, connu pour ses joues gonflées." },
    { word: "Cheval", definition: "Grand mammifère herbivore utilisé pour le travail ou les loisirs, souvent monté." },
    { word: "Tigre", definition: "Grand félin sauvage, connu pour sa force et ses rayures caractéristiques." },
    { word: "Lion", definition: "Grand félin carnivore, surnommé le roi de la jungle." },
    { word: "Éléphant", definition: "Grand mammifère terrestre à trompe, connu pour sa mémoire et sa taille impressionnante." },
    { word: "Kangourou", definition: "Mammifère marsupial d'Australie, caractérisé par sa poche ventrale et sa capacité à sauter." },
    { word: "Serpent", definition: "Reptile sans membres, souvent craint, qui se déplace en rampant." },
    { word: "Tortue", definition: "Reptile connu pour sa carapace dure et sa lenteur." },
    { word: "Panda", definition: "Mammifère herbivore d'Asie, célèbre pour ses taches noires et blanches." },
    { word: "Koala", definition: "Mammifère marsupial d'Australie, connu pour sa paresse et son alimentation exclusive d'eucalyptus." },
    { word: "Zèbre", definition: "Animal sauvage à rayures blanches et noires, de la famille des équidés." },
    { word: "Requin", definition: "Grand poisson prédateur, souvent redouté dans les océans." },
    { word: "Dauphin", definition: "Mammifère marin connu pour son intelligence et ses sauts spectaculaires." },
    { word: "Ours", definition: "Grand mammifère carnivore, souvent trouvé dans les régions froides." },
    { word: "Singe", definition: "Mammifère primate, souvent agile et intelligent." },
    { word: "Elephant", definition: "Animal majestueux, énorme, vivant principalement en Afrique et en Asie." },
    { word: "Souris", definition: "Petit rongeur nocturne, souvent trouvé dans les maisons." },
    { word: "Vache", definition: "Grand mammifère domestique, élevé pour son lait." },
    { word: "Mouton", definition: "Animal domestique élevé pour sa laine et sa viande." },
    { word: "Chevreuil", definition: "Petit cervidé vivant dans les forêts, apprécié pour sa rapidité." },
    { word: "Cochon", definition: "Animal domestique élevé pour sa viande, souvent très intelligent." },
    { word: "Perroquet", definition: "Oiseau souvent coloré, connu pour sa capacité à imiter des sons humains." },
    { word: "Autruche", definition: "Grand oiseau non volant, connu pour sa vitesse et ses longues jambes." },
    { word: "Crocodile", definition: "Grand reptile carnivore vivant dans les zones tropicales." },
    { word: "Paon", definition: "Oiseau coloré et élégant, connu pour ses plumes magnifiques." },
    { word: "Baleine", definition: "Gros mammifère marin, connu pour sa taille impressionnante." },
    { word: "Loutre", definition: "Petit mammifère aquatique, souvent trouvé près des rivières." },
    { word: "Chinchilla", definition: "Petit rongeur, connu pour sa fourrure dense et douce." },
    { word: "Alpaga", definition: "Mammifère de la famille des camélidés, élevé pour sa laine." },
    { word: "Hérisson", definition: "Petit mammifère nocturne couvert de piquants." },
    { word: "Poulpe", definition: "Animal marin avec huit tentacules et une grande intelligence." },
    { word: "Morse", definition: "Grand mammifère marin, souvent trouvé dans les eaux froides." },
    { word: "Sardine", definition: "Petit poisson souvent consommé en conserve." },
    { word: "Raie", definition: "Poisson plat vivant dans les mers chaudes." },
    { word: "Tortue de mer", definition: "Reptile marin connu pour sa lenteur et sa carapace." },
    { word: "Narval", definition: "Cétacé caractérisé par sa longue corne spirale." },
    { word: "Pangolin", definition: "Mammifère insectivore, caractérisé par ses écailles." },
    { word: "Gorille", definition: "Grand primate, très intelligent et souvent vivant dans les forêts tropicales." },
    { word: "Chacal", definition: "Petit carnivore, souvent trouvé dans les zones désertiques." },
];

const pairsToShow = 5;
let draggedItem = null;

function generateGame() {
    document.getElementById('match-score').textContent = '';
    const wordsContainer = document.querySelector('.match-words-container');
    const definitionsContainer = document.querySelector('.match-definitions-container');

    wordsContainer.innerHTML = '';
    definitionsContainer.innerHTML = '';

    let selectedPairs = [...wordDefinitionPairs].sort(() => Math.random() - 0.5).slice(0, pairsToShow);
    let definitions = selectedPairs.map(pair => pair.definition).sort(() => Math.random() - 0.5);

    selectedPairs.forEach(pair => {
        const wordDiv = document.createElement('div');
        wordDiv.classList.add('match-word');
        wordDiv.textContent = pair.word;

        const dropZone = document.createElement('div');
        dropZone.classList.add('match-dropzone');
        dropZone.setAttribute('data-word', pair.word);

        wordDiv.appendChild(dropZone);
        wordsContainer.appendChild(wordDiv);
    });

    definitions.forEach(def => {
        const definitionDiv = document.createElement('div');
        definitionDiv.classList.add('match-definition');
        definitionDiv.textContent = def;
        definitionDiv.setAttribute('draggable', true);

        definitionDiv.addEventListener('dragstart', (event) => {
            draggedItem = event.target;
            setTimeout(() => event.target.classList.add('hide'), 0);
        });

        definitionDiv.addEventListener('dragend', (event) => {
            event.target.classList.remove('hide');
        });

        definitionsContainer.appendChild(definitionDiv);
    });

    document.querySelectorAll('.match-dropzone').forEach(zone => {
        zone.addEventListener('dragover', (event) => event.preventDefault());

        zone.addEventListener('drop', (event) => {
            event.preventDefault();
            if (!zone.hasChildNodes()) {
                draggedItem.classList.remove('hide');
                zone.appendChild(draggedItem);
                draggedItem.draggable = false;
                draggedItem = null;
                checkCompletion();
            }
        });
    });
}

function checkCompletion() {
    let allFilled = true;
    document.querySelectorAll('.match-dropzone').forEach(zone => {
        if (!zone.hasChildNodes()) {
            allFilled = false;
        }
    });

    if (allFilled) {
        let score = 0;
        document.querySelectorAll('.match-dropzone').forEach(zone => {
            const word = zone.getAttribute('data-word');
            const droppedDef = zone.firstChild.textContent;
            const correctDef = wordDefinitionPairs.find(pair => pair.word === word).definition;
            if (droppedDef === correctDef) {
                zone.firstChild.style.color = "green";
                score++;
            } else {
                zone.firstChild.style.color = "red";
            }
        });

        document.getElementById('match-score').textContent = `Votre score : ${score} / ${pairsToShow}`;

    }
}

document.querySelector('.match-restart').addEventListener('click', generateGame);

generateGame();
