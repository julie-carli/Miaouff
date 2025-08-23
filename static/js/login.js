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

    // To force login form to be the first one to appear
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");

    // To switch between login and register
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

    // Password Validation
    passwordInput.addEventListener("input", function () {
        let password = passwordInput.value;

        for (let key in passwordRegex) {
            if (passwordRegex[key].test(password)) {
                criteria[key].classList.add("valid");
            } else {
                criteria[key].classList.remove("valid");
            }
        }
    });});