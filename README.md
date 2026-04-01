# 🐾 Miaouff

Miaouff est un site web dédié aux animaux de compagnie. Il permet aux utilisateurs de consulter des animaux disponibles à l'adoption, d'accéder à une boutique en ligne, de lire des articles de blog, de jouer à des mini-jeux thématiques et de s'informer via un glossaire des espèces animales.

---

## 🗂️ Stack technique

| Technologie | Rôle |
|---|---|
| Python / Flask | Framework back-end |
| PostgreSQL / SQLAlchemy | Base de données relationnelle |
| MongoDB / PyMongo | Stockage des articles de blog |
| HTML / CSS / JavaScript | Front-end |
| Flask-Login | Gestion de l'authentification |
| Flask-Mail | Envoi d'e-mails |
| Flask-Session | Gestion des sessions côté serveur |
| Werkzeug | Hashage des mots de passe & upload de fichiers |

---

## 📁 Architecture du projet

```
miaouff/
│
├── static/              # Assets statiques (CSS, JS, images)
├── templates/           # Templates HTML (Jinja2)
├── tests/               # Tests unitaires (pytest)
│
├── app.py               # Point d'entrée de l'application Flask
├── setup_db.py          # Initialisation et modèles de la base de données
├── add_articles.py      # Script de peuplement des articles MongoDB
├── delete_tables.py     # Script de suppression des tables PostgreSQL
│
├── .env                 # Variables d'environnement (non versionné)
├── .gitignore
├── requirements.txt
├── robots.txt
└── llms.txt
```

---

## ⚙️ Installation

### Prérequis

- Python 3.10+
- PostgreSQL
- MongoDB

### Étapes

**1. Cloner le dépôt**

```bash
git clone https://github.com/julie-carli/miaouff.git
cd miaouff
```

**2. Créer et activer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**4. Configurer les variables d'environnement**

Créer un fichier `.env` à la racine du projet :

```env
SECRET_KEY=ta_clé_secrète

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/miaouff
DB_NAME=miaouff
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# MongoDB
MONGODB_URI=mongodb://localhost:27017/miaouff

# Flask-Mail
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=ton@email.com
MAIL_PASSWORD=ton_mot_de_passe
MAIL_DEFAULT_SENDER=ton@email.com
```

**5. Initialiser la base de données PostgreSQL**

```bash
python setup_db.py
```

**6. Lancer l'application**

```bash
python app.py
```

L'application est accessible sur `http://localhost:5000`.

---

## 🔐 Rôles utilisateurs

| Rôle | Accès |
|---|---|
| `user` | Compte personnel, boutique, adoption, blog, jeux |
| `admin` | Gestion des utilisateurs, produits, animaux, refuges, articles |

---

## 🧩 Fonctionnalités principales

- **Authentification** — inscription, connexion, déconnexion, réinitialisation de mot de passe par e-mail
- **Adoption** — consultation des animaux disponibles avec filtres par refuge et espèce
- **Refuges** — liste des refuges partenaires avec leurs animaux
- **Boutique** — catalogue de produits avec panier, gestion des stocks et tunnel de commande
- **Blog** — articles stockés dans MongoDB, liés optionnellement à un refuge
- **Glossaire** — encyclopédie des espèces animales avec filtres alphabétiques
- **Mini-jeux** — quiz, memory, jeu du pendu, mots mêlés, match d'animaux, Rapido
- **Espace admin** — interface CRUD complète pour les utilisateurs, animaux, refuges, produits, catégories et articles

---

## 🚀 Déploiement (Railway)

Le projet est déployé sur [Railway](https://railway.app).

Les variables d'environnement sont à renseigner directement dans le dashboard Railway (onglet **Variables**), sans fichier `.env`.

Railway détecte automatiquement le projet Python. Il faut s'assurer d'avoir à la racine :

- `requirements.txt` — pour l'installation des dépendances
- Un `Procfile` ou la commande de démarrage configurée dans Railway :

```
web: python app.py
```

> ⚠️ En production, penser à passer `debug=False` dans `app.run()` et à sécuriser la `SECRET_KEY`.

---

## 🧪 Tests

```bash
pytest
```

Les tests se trouvent dans le dossier `tests/`.

---

## 📌 Notes de développement

- Les mots de passe sont hashés avec `pbkdf2:sha256` via Werkzeug.
- Les tokens de réinitialisation de mot de passe sont stockés en mémoire (dictionnaire Python). Une amélioration future serait de les persister en base de données avec une date d'expiration.
- Les uploads d'images sont stockés dans `static/images/`.

---

## 👩‍💻 Auteur

Projet réalisé dans le cadre de la formation **Concepteur Développeur d'Applications (Bac+3/+4)** de Julie.
