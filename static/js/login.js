document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const showRegister = document.getElementById("showRegister");
    const showLogin = document.getElementById("showLogin");
    const passwordInput = document.getElementById("register-password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    
    const criteria = {
        length: document.getElementById("length-criteria"),
        uppercase: document.getElementById("uppercase-criteria"),
        lowercase: document.getElementById("lowercase-criteria"),
        number: document.getElementById("number-criteria"),
        symbol: document.getElementById("symbol-criteria")
    };

    const passwordRegex = {
        length: /.{12,}/,
        uppercase: /[A-Z]/,
        lowercase: /[a-z]/,
        number: /\d/,
        symbol: /[@$!%*?&,.;:\-_+=()[\]{}\/\\|^~#]/
    };

    if (!loginForm || !registerForm || !showRegister || !showLogin) {
        console.error("Erreur : Un ou plusieurs éléments sont introuvables.");
        return;
    }

    // Forcer l'affichage du formulaire de connexion au chargement
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");

    // Fonction pour basculer entre login et register
    function toggleForms(showLoginForm) {
        if (showLoginForm) {
            loginForm.classList.remove("hidden");
            registerForm.classList.add("hidden");
        } else {
            registerForm.classList.remove("hidden");
            loginForm.classList.add("hidden");
        }
    }

    showRegister.addEventListener("click", function (event) {
        event.preventDefault();
        toggleForms(false);
    });

    showLogin.addEventListener("click", function (event) {
        event.preventDefault();
        toggleForms(true);
    });

    // Validation du mot de passe
    passwordInput.addEventListener("input", function () {
        let password = passwordInput.value;

        for (let key in passwordRegex) {
            if (passwordRegex[key].test(password)) {
                criteria[key].classList.add("valid");
            } else {
                criteria[key].classList.remove("valid");
            }
        }
    });

    // Gestion de l'inscription
    registerForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let email = document.getElementById("register-email").value;
        let password = passwordInput.value;
        let confirmPassword = confirmPasswordInput.value;

        let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            alert("Veuillez entrer une adresse e-mail valide.");
            return;
        }

        if (!Object.values(criteria).every(el => el.classList.contains("valid"))) {
            alert("Le mot de passe ne respecte pas tous les critères.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Les mots de passe ne correspondent pas.");
            return;
        }

        console.log("Envoi des données d'inscription...");

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                email: email,
                password: password,
                confirm_password: confirmPassword,
                action: "register"
            })
        })
        .then(response => response.text())
        .then(data => {
            console.log("Réponse du serveur :", data);
            window.location.href = "/login";
        })
        .catch(error => console.error("Erreur lors de l'inscription :", error));
    });

    // Gestion de la connexion
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let email = document.getElementById("login-email").value;
        let password = document.getElementById("login-password").value;

        console.log("Envoi des données de connexion...");

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                email: email,
                password: password,
                action: "login"
            })
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.text();
            }
        })
        .then(data => {
            if (data) console.log("Réponse du serveur :", data);
        })
        .catch(error => console.error("Erreur lors de la connexion :", error));
    });
});