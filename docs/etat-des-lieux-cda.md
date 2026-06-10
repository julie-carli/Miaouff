# État des lieux — Projet Miaouff vs Titre Professionnel CDA

> Document de travail pour préparer le dossier projet et la soutenance du titre
> **Concepteur Développeur d'Applications** (REAC/REV v04, arrêté du 26/04/2023).
> Dernière mise à jour : 10/06/2026.

---

## 0. Rappel du cadre (REAC / REV)

Le titre CDA = **3 activités-types (AT)** découpées en **11 compétences professionnelles (CP)** :

| AT | Compétences |
|----|-------------|
| **AT1 — Développer une application sécurisée** | CP1 Installer/configurer son environnement · CP2 Développer des interfaces utilisateur · CP3 Développer des composants métier · CP4 Contribuer à la gestion d'un projet |
| **AT2 — Concevoir et développer une application sécurisée organisée en couches** | CP5 Analyser les besoins et maquetter · CP6 Définir l'architecture logicielle · CP7 Concevoir et mettre en place une BDD relationnelle · CP8 Développer des composants d'accès aux données SQL et NoSQL |
| **AT3 — Préparer le déploiement d'une application sécurisée** | CP9 Préparer et exécuter les plans de tests · CP10 Préparer et documenter le déploiement · CP11 Contribuer à la mise en production (DevOps) |

**L'examen** (REV §3.1) :
- **Dossier projet** imprimé : **40 à 60 pages** (hors garde, sommaire, annexes) + **annexes ≤ 40 pages**.
- **Support de présentation** (diaporama).
- **Présentation orale** (40 min) + **entretien technique** (45 min) + **questionnaire professionnel** (30 min, dont anglais) + entretien final (20 min).

**Éléments OBLIGATOIRES du dossier** (REV p.6-7) — c'est la checklist de référence :
- liste des compétences mises en œuvre ;
- cahier des charges / expression des besoins ;
- présentation entreprise/service + gestion de projet (planning, suivi, qualité) ;
- **spécifications fonctionnelles** : contraintes & livrables, **architecture logicielle**, **maquettes + enchaînement**, **MCD + MPD**, **script de création de la BDD**, **diagramme de cas d'utilisation**, **diagramme de séquence** ;
- **spécifications techniques (dont sécurité)** ;
- **réalisations** : extraits de code significatifs (UI, métier, accès données, autres) + **arguments de choix dont sécurité** ;
- **présentation des éléments de sécurité** de l'application ;
- **plan de tests** ;
- **jeu d'essai de la fonctionnalité la plus représentative** (données en entrée / attendues / obtenues + analyse des écarts) ;
- **description de la veille** sur les vulnérabilités + failles corrigées ;
- synthèse / conclusion.

---

## 1. Synthèse globale — où en est Miaouff ?

| Domaine | État | Priorité |
|---|---|---|
| Fonctionnel (boutique, adoption, blog, glossaire, jeux, admin) | ✅ Riche et abouti | — |
| Architecture (models / services / templates) | 🟡 Correcte mais `app.py` monolithique (1268 lignes) | Moyenne |
| Sécurité applicative | 🟢 **Failles critiques corrigées** (CSRF, accès admin, en-têtes, cookies, rate limiting, tokens) | — |
| Tests | 🟢 Suite structurée (67 tests : unit/intégration/sécurité) ; reste e2e Playwright | Moyenne |
| Accessibilité / RGAA | 🟡 Base sémantique + lien d'évitement ; reste audit axe/WAVE | Moyenne |
| Responsivité | ✅ Media queries + viewport OK | Basse |
| SEO | 🟢 Titres/descriptions par page, canonical, OG/Twitter, sitemap.xml, robots.txt, noindex admin | Basse |
| Performance / rapidité | 🟡 Lazy-loading + cache assets faits ; reste WebP + audit Lighthouse | Moyenne |
| Éco-conception | 🟡 Lazy + cache + sobriété ; reste mesure EcoIndex + démarche | Moyenne |
| RGPD / mentions légales | 🟡 Pages présentes, consentement cookies absent | Moyenne |
| Déploiement / CI-CD (DevOps) | 🟡 CI GitHub + Render OK, pas de conteneur/CD complet | Moyenne |
| Qualité de code / outillage (black, flake8, prettier, pre-commit) | 🟡 flake8 seul, à compléter | Moyenne |
| Code propre (code mort, commentaires EN, docstrings, type hints) | 🟡 à nettoyer/documenter | Moyenne |
| Gestion des secrets | ✅ historique sain, 🔴 ajouter gitleaks + traiter `dump.sql` | Moyenne |
| Documents de conception (MCD, MPD, diagrammes UML, dossier) | 🔴 **À produire** | **Haute** |

**Lecture rapide :** le code fonctionnel est solide et couvre largement les 3 activités-types. Les 3 chantiers qui pèsent le plus pour le titre sont : **(1) la sécurité**, **(2) les tests / plan de tests**, **(3) les livrables documentaires du dossier** (diagrammes, MCD/MPD, dossier projet).

---

## 2. État des lieux compétence par compétence (CP1 → CP11)

> Légende : ✅ acquis · 🟡 partiel · 🔴 à faire

### AT1 — Développer une application sécurisée

**CP1 — Installer et configurer son environnement de travail** — 🟡
- ✅ Environnement Python/venv, Git, dépôt GitHub, `requirements.txt`.
- 🟡 **Conteneurisation attendue par le référentiel** : « paramétrer et utiliser des conteneurs ». Aucun `Dockerfile` / `docker-compose`. → À ajouter (au moins un `docker-compose` Postgres + Mongo + app pour reconstituer l'environnement de prod).
- À documenter dans le dossier : outils choisis et pourquoi.

**CP2 — Développer des interfaces utilisateur** — ✅ (à consolider)
- ✅ Templates Jinja2, CSS responsive, JS (jeux, chatbot), structure sémantique.
- 🟡 Critère « tests unitaires des composants » et « tests de sécurité » : peu/pas couverts (voir §4).
- 🟡 « style défensif, validation des entrées » côté JS à documenter.

**CP3 — Développer des composants métier** — ✅ (à consolider)
- ✅ Logique métier dans `services/` (auth, cart, product, shelter, chat). POO partielle.
- 🟡 Style défensif / gestion des exceptions à renforcer et documenter.
- 🔴 Tests unitaires des composants métier ≈ absents.

**CP4 — Contribuer à la gestion d'un projet informatique** — 🔴 (livrables à produire)
- 🔴 Planning, suivi des tâches, comptes rendus, choix des outils collaboratifs : **à formaliser** (GitHub Projects/issues, journal de bord, planning Gantt). C'est surtout du livrable documentaire.

### AT2 — Concevoir et développer une application sécurisée organisée en couches

**CP5 — Analyser les besoins et maquetter** — 🔴 (livrables à produire)
- 🔴 Cahier des charges / expression des besoins formalisé : à rédiger.
- 🔴 **Maquettes + enchaînement des écrans** (Figma p.ex.) : à produire (ou reconstituer a posteriori).
- 🔴 Dossier de conception structuré.

**CP6 — Définir l'architecture logicielle** — 🟡
- 🟡 Architecture en couches existe de fait (présentation Jinja / services / modèles ORM) mais **pas de couche d'accès aux données (repository/DAO) explicite** et `app.py` mélange routage + logique.
- 🔴 **Schéma d'architecture multicouche** + rôle de chaque couche + stratégie de sécurité : à dessiner et rédiger.

**CP7 — Concevoir et mettre en place une BDD relationnelle** — 🟡
- ✅ Modèle relationnel implémenté (SQLAlchemy + migrations Alembic), `setup_db.py`, `dump.sql`.
- 🔴 **MCD (modèle conceptuel)** et **MPD (modèle physique)** formalisés : à produire (diagrammes).
- 🟡 « jeu d'essai complet en base de test + sauvegarde/restauration » : `dump.sql` existe, à formaliser comme jeu d'essai documenté.

**CP8 — Développer des composants d'accès aux données SQL et NoSQL** — ✅
- ✅ SQL (PostgreSQL/SQLAlchemy) **et** NoSQL (MongoDB/pymongo, articles de blog) → couvre explicitement « SQL et NoSQL ».
- ✅ Accès paramétrés via ORM (anti-injection SQL).
- 🟡 Validation des entrées côté accès données + cas d'exception à renforcer ; 🟡 regex MongoDB non validée (ReDoS potentiel, voir §3).
- 🔴 Tests unitaires + sécurité des composants d'accès : à écrire.

### AT3 — Préparer le déploiement d'une application sécurisée

**CP9 — Préparer et exécuter les plans de tests** — 🔴 **(chantier majeur)**
- 🔴 **Plan de tests** couvrant toutes les fonctionnalités : à rédiger (voir §4).
- 🔴 Tests d'intégration, de non-régression, tests système (sécurité + charge), tests d'acceptation, fuzzing : quasi inexistants.

**CP10 — Préparer et documenter le déploiement** — 🟡
- ✅ Déploiement réel sur **Render** (Procfile, `.python-version`, `render.yaml`), CI GitHub Actions.
- 🔴 **Procédure de déploiement documentée** + scripts + définition des environnements (test/UAT/prod) : à rédiger.

**CP11 — Contribuer à la mise en production (DevOps)** — 🟡
- ✅ CI : `.github/workflows/ci.yml` (lint flake8 + pytest + coverage). Déploiement auto Render sur push.
- 🟡 « outils de qualité de code » : flake8 présent ; ajouter analyse sécurité (bandit) et éventuellement couverture seuil.
- 🔴 Conteneurs (Docker) + script d'intégration complet : à compléter pour cocher pleinement la compétence.

---

## 3. Sécurité — failles identifiées et corrections

> Issues d'un audit du code (fichier:ligne). Classées par sévérité. La sécurité est
> une **préoccupation constante** du CDA (citée dans presque toutes les fiches) :
> ce chantier est prioritaire et fera l'objet de la section « éléments de sécurité »
> + « veille » du dossier.

### 🔴 Critique

1. **Contrôle d'accès manquant sur des routes sensibles**
   - `/edit-users`, `/edit-user/<id>` : **ni `@login_required` ni vérification du rôle admin** → n'importe qui liste/édite les utilisateurs.
   - `/delete_user/<id>` : `@login_required` mais **pas de contrôle rôle admin** → tout utilisateur connecté peut supprimer n'importe quel compte.
   - `/send_reset_code/<id>` : aucune protection → spam/harcèlement.
   - **Correction** : créer un décorateur `@admin_required` et l'appliquer à toutes les routes admin ; vérifier la propriété des ressources.

2. **Absence de protection CSRF** (aucune dépendance Flask-WTF, aucun token dans les formulaires)
   - Toutes les actions POST (login, register, achat, suppression, admin) sont forgeables cross-site.
   - **Correction** : `Flask-WTF` + `CSRFProtect(app)` + `{{ csrf_token() }}` dans tous les `<form>`.

3. **Cookies de session non sécurisés** (aucune config dans `config.py`)
   - **Correction** : `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, `PERMANENT_SESSION_LIFETIME`.

4. **Aucun en-tête HTTP de sécurité** (CSP, X-Frame-Options, HSTS, X-Content-Type-Options…)
   - **Correction** : `Flask-Talisman`, ou un `@app.after_request` qui pose les en-têtes.

### 🟠 Moyen

5. **Pas de rate limiting** (brute-force login, spam register/reset) — un `errorhandler(429)` existe mais n'est jamais déclenché.
   - **Correction** : `Flask-Limiter` (ex. `5/minute` sur `/login`, `/register`, `/send_reset_code`).

6. **Tokens de reset password fragiles** : stockés en mémoire (`reset_tokens = {}`), `secrets.token_hex(4)` (court), **sans expiration**.
   - **Correction** : token `secrets.token_urlsafe(32)`, persistance en base avec `expires_at`, usage unique.

7. **XSS stockée via le contenu d'articles MongoDB** : `{{ article['content'] }}` rendu en HTML brut (l'admin saisit du HTML).
   - **Correction** : assainir le HTML à l'entrée (`bleach`) ou n'autoriser que du Markdown rendu de façon sûre.

8. **ReDoS / NoSQL** : recherche `{"$regex": search_query}` sur input non validé.
   - **Correction** : échapper la requête (`re.escape`) et limiter la longueur.

9. **Upload** : `secure_filename` + whitelist d'extensions OK, mais **pas de validation MIME ni de taille**.
   - **Correction** : `MAX_CONTENT_LENGTH`, vérification du type réel (python-magic / Pillow).

### ✅ Déjà bon
- Pas d'injection SQL (ORM paramétré partout).
- Hash des mots de passe `pbkdf2:sha256` + politique de complexité (12 car., maj/min/chiffre/symbole).
- Auto-échappement Jinja2 actif (pas de `|safe` / `render_template_string`).
- Secrets hors du code (variables d'env Render, `.env` gitignoré).
- `FLASK_DEBUG=False` en production.

> **Sur le « DDoS »** : un vrai DDoS volumétrique se contre à l'infrastructure (Render/Cloudflare),
> pas dans le code. Côté applicatif, ce qui est attendu et réaliste pour le titre, c'est le
> **rate limiting** (anti brute-force / anti-spam) → point 5.

---

## 4. Plan de tests (CP9) — chantier prioritaire

Le référentiel attend un **plan de tests** couvrant tous les niveaux. Voici un plan
concret et l'outillage recommandé. Objectif réaliste pour le titre : **couverture
significative des composants métier + parcours critiques + tests de sécurité ciblés**.

### 4.1 Outillage à mettre en place
| Type | Outil | Déjà là ? |
|---|---|---|
| Tests unitaires & intégration | `pytest`, `pytest-cov` | ✅ (CI) |
| Fixtures / base de test | `pytest` fixtures + SQLite ou Postgres de test | 🟡 partiel |
| Tests end-to-end | **Playwright** (ou Selenium) | 🔴 |
| Analyse sécurité statique | **bandit** | 🔴 |
| Scan vulnérabilités dépendances | **pip-audit** | 🔴 |
| Scan dynamique (DAST) | **OWASP ZAP** (baseline scan) | 🔴 |
| Audit perf/SEO/access/éco | **Lighthouse**, **EcoIndex** | 🔴 |

### 4.2 Tests unitaires (composants métier — `services/`)
Cibler la logique pure, isolée de la BDD quand possible :
- `auth_service` : `is_password_strong()` (cas limites), génération/validation de token de reset, hash/vérif mot de passe.
- `cart_service` : `get_cart_totals()`, `add_to_cart`, `update_cart`, `remove_from_cart`, `is_address_complete` (panier vide, quantités négatives, stock insuffisant).
- `product_service` : regroupement par catégorie, création/màj/suppression.
- `shelter_service` : `allowed_file()` (extensions valides/invalides), save/update/delete.

### 4.3 Tests d'intégration (routes + BDD)
- Auth : register (mot de passe faible refusé), login OK / KO, logout, accès route protégée sans session → redirection.
- **Autorisation** : un utilisateur non-admin reçoit 403 sur `/edit-users`, `/delete_user`, `/edit-products` (test qui **échouera tant que la faille §3.1 n'est pas corrigée** → bon test de non-régression sécurité).
- Boutique : ajout panier → tunnel commande → `payment_success` (Stripe en mode test/mock).
- Blog : lecture article, filtre glossaire, recherche.
- Tests de **non-régression** : figer les parcours critiques.

### 4.4 Tests de sécurité
- CSRF : une requête POST sans token est rejetée (après mise en place Flask-WTF).
- Auth bypass : accès direct aux routes admin sans rôle → refusé.
- Injection : payloads SQL (`' OR 1=1 --`) et NoSQL/regex sur les champs de recherche → pas d'effet.
- XSS : soumission de `<script>` dans un article → échappé/assaini au rendu.
- Brute-force : N tentatives login → 429 (après Flask-Limiter).
- Statique : `bandit -r .` sans finding haute sévérité ; `pip-audit` sans CVE critique.

### 4.5 Tests end-to-end (Playwright)
Scénarios utilisateur complets dans un navigateur réel :
- Parcours visiteur : accueil → glossaire → fiche animal → blog.
- Parcours achat : ajout panier → connexion → commande → confirmation.
- Parcours admin : connexion admin → CRUD produit/article.
- Captures d'écran automatiques (utiles pour le dossier).

### 4.6 Tests système (charge)
- `locust` ou `k6` : montée en charge sur les pages clés, mesure temps de réponse (à corréler avec §6 performance). Documenter les résultats.

### 4.7 Jeu d'essai (exigé au dossier)
Choisir **la fonctionnalité la plus représentative** (recommandation : **le tunnel de commande** ou **l'inscription sécurisée**) et documenter : données en entrée, résultats attendus, résultats obtenus, **analyse des écarts**.

### 4.8 Intégration CI
Étendre `.github/workflows/ci.yml` : ajouter `bandit`, `pip-audit`, seuil de couverture (`--cov-fail-under`), et idéalement un job Playwright.

---

## 5. Accessibilité / RGAA

**Bon socle existant** : `lang="fr"`, `<meta viewport>`, structure sémantique (`header/nav/main/footer/article/section`), ~61 attributs ARIA, labels de formulaires, `alt` sur la majorité des images, contrastes corrects.

**À faire pour viser une conformité démontrable :**
- Audit RGAA avec un outil (extension **axe DevTools**, **WAVE**, ou critères RGAA 4.1).
- Vérifier : `alt` sur **toutes** les images (corriger les manquants), `alt=""` sur les images décoratives.
- Navigation **100 % clavier** (focus visible, ordre de tabulation, pièges au clavier sur le chatbot/menus).
- `aria-required` / `aria-invalid` + messages d'erreur liés aux champs de formulaire.
- Contrastes vérifiés au ratio WCAG AA (4.5:1 texte normal).
- Lien d'évitement (« aller au contenu »).
- Documenter la démarche dans le dossier (le RGAA est cité dans CP1, CP2, CP5).

---

## 6. Responsivité

**État : ✅ bon.** `<meta viewport>` présent, plusieurs media queries (900px, 480px, etc.), layout flex/grid.
**À faire :** tests réels multi-tailles (mobile/tablette/desktop), captures pour le dossier, vérifier les pages admin et les jeux sur petit écran.

---

## 7. SEO (le « wouah » qui se voit immédiatement)

**À structurer (peu présent aujourd'hui) — checklist complète :**
- `<title>` et `<meta name="description">` **uniques et descriptifs par page** (blocs Jinja surchargeables depuis `base.html`).
- **`<link rel="canonical">`** par page (évite le contenu dupliqué).
- Hiérarchie des titres : un seul `<h1>` par page, puis `<h2>/<h3>` logiques.
- **Open Graph** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) + **Twitter Card** → aperçu riche au partage (effet « pro » immédiat).
- **`robots.txt`** (présent ? à compléter) + **`sitemap.xml`** généré (route Flask dynamique idéalement).
- **Données structurées Schema.org (JSON-LD)** : `Organization`, `Product` (boutique), `Article` (blog), `BreadcrumbList` → éligibilité aux rich results Google.
- **Favicon complet** + `apple-touch-icon` + `manifest.webmanifest` (bonus PWA).
- **Fil d'Ariane** (breadcrumb) visible + structuré.
- URLs lisibles (déjà plutôt le cas), `alt` d'images (recoupe l'accessibilité), `lang` correct.
- **Page 404 personnalisée** soignée (déjà un errorhandler 404 → vérifier le rendu).
- Balise `<meta name="robots">` adaptée (indexer le public, `noindex` sur l'admin).
- Mesurer avec **Lighthouse SEO** (viser 100) et la Search Console.

## 8. Performance / rapidité d'affichage

**À mesurer puis optimiser :**
- Lancer **Lighthouse** (Performance) et **WebPageTest** sur le site Render.
- **Images** : ce sont souvent le plus gros poste. Compresser, servir en **WebP**, dimensionner correctement, `loading="lazy"`.
- **CSS/JS** : minification, suppression du CSS mort, regroupement.
- **Cache HTTP** : en-têtes `Cache-Control` sur les assets statiques.
- **BDD** : index sur les colonnes filtrées (recherche, catégories), éviter les requêtes N+1 (SQLAlchemy `joinedload`).
- Garder en tête le **cold start Neon** (free tier) et le réveil de l'instance Render free.
- Documenter avant/après dans le dossier.

## 9. Éco-conception

Cité explicitement dans le référentiel (CP1, CP2, CP5, CP6, AT2/AT3). À traiter :
- Mesurer avec **EcoIndex** (ecoindex.fr) / **GreenIT-Analysis** → obtenir une note (A→G) et le poids des pages.
- Réduire le poids des pages : images optimisées (recoupe §8), limiter les requêtes HTTP, sobriété JS.
- Choix d'hébergement (documenter), pas de chargement inutile (lazy-load, pagination).
- **Documenter une démarche d'éco-conception** dans le dossier (c'est surtout ça qui est valorisé) : les 115 bonnes pratiques GreenIT comme grille.

## 10. RGPD / mentions légales

- ✅ Pages présentes : politique de confidentialité, mentions légales, CGU, politique cookies.
- 🔴 **Bandeau de consentement cookies** (avant dépôt de cookies non essentiels) : absent.
- 🔴 **Droit à l'effacement** (suppression de son compte/données par l'utilisateur) : à implémenter.
- Documenter la base légale et les durées de conservation.

---

## 10bis. Qualité de code, conventions & outillage (le « code propre » qui impressionne)

Un code propre, cohérent et outillé est immédiatement visible par un jury technique.
Cibles concrètes pour Miaouff :

### Formatage & lint automatiques
| Domaine | Outil | Rôle |
|---|---|---|
| Python — format | **black** | formatage automatique, style unique non négociable |
| Python — imports | **isort** (profil `black`) | tri/regroupement des imports |
| Python — lint | **flake8** | déjà dans la CI ; garder, durcir progressivement |
| Python — code mort | **vulture** | détecte fonctions/imports/variables inutilisés |
| Python — sécurité statique | **bandit** | failles côté code (recoupe §4) |
| HTML/CSS/JS — format | **Prettier** | formatage des templates Jinja, CSS, JS |
| Tout le repo | **pre-commit** | lance black/isort/flake8/prettier/gitleaks **avant chaque commit** |
| Config éditeur | **.editorconfig** | indentation/fins de ligne cohérentes entre machines |

> Mise en place type : un `.pre-commit-config.yaml` + `pyproject.toml` (config black/isort)
> + `.flake8`. Ainsi tout commit est automatiquement propre, et la CI vérifie la même chose.

### Code mort & propreté
- 🔴 **Ne laisser aucun code mort** : passer **vulture** + supprimer le code commenté, les
  routes/fonctions inutilisées, les imports superflus. Exemple déjà repéré : l'`errorhandler(429)`
  n'est jamais déclenché (sera utile une fois Flask-Limiter en place — sinon à retirer).
- Supprimer les fichiers/scripts non utilisés (`delete_tables.py`, `__pycache__`, `flask_session/`
  ne doivent pas être versionnés → vérifier `.gitignore`).
- Factoriser `app.py` (1268 lignes) en **Blueprints** par domaine (auth, shop, blog, admin…) :
  gros gain de lisibilité et argument d'architecture pour le dossier.

### Commentaires & documentation du code
- 🔴 **Commentaires et docstrings en anglais uniquement** (exigence pro + cohérence ;
  le référentiel demande d'ailleurs un code documenté « y compris en anglais »).
- **Docstrings** sur chaque fonction/route (format Google ou reST) : but, paramètres, retour.
- Commenter le **pourquoi**, pas le **quoi** ; pas de commentaire qui paraphrase le code.
- **Type hints** Python sur les signatures de fonctions (`def get_cart(user_id: int) -> dict:`).
- Convention de nommage cohérente (snake_case Python, déjà globalement le cas).
- (Bonus) **commits conventionnels** (`feat:`, `fix:`, `docs:`…) — déjà partiellement le cas.

## 10ter. Gestion des secrets (vérifié ✅ + garde-fous)

**État actuel — bon :**
- ✅ `.env` **n'a jamais été commité** (vérifié sur tout l'historique git).
- ✅ Aucun fichier sensible (`.env`, `.pem`, `.key`, `credentials`) ajouté dans l'historique.
- ✅ Aucun secret en dur dans le code tracké (seul un mot de passe de **test** factice).
- ✅ Tous les secrets sont en variables d'environnement (Render) ; `.env` gitignoré.

**À ajouter (garde-fous pour que ça reste vrai) :**
- 🔴 **gitleaks** ou **detect-secrets** branché dans **pre-commit** + dans la CI → bloque
  tout commit/PR contenant une clé, un token, un mot de passe. C'est le « truc » qui garantit
  qu'aucun secret ne pourra fuiter à l'avenir.
- 🟠 **`dump.sql` versionné** : il contient des e-mails / données (≈ données personnelles).
  → **À vérifier et idéalement retirer du repo** (ou anonymiser) : on ne versionne pas un dump
  de données réelles (enjeu RGPD, surtout si le repo est public). Préférer un **script de seed
  avec des données fictives** comme jeu d'essai (recoupe CP7 §2).
- Documenter dans le README la liste des variables d'environnement requises (sans valeurs).

## 11. Checklist des livrables du dossier projet (REV)

> À cocher au fur et à mesure. Hors page de garde/sommaire/annexes : **40–60 pages**.

- [ ] Liste des compétences mises en œuvre (mapping CP1–CP11 ↔ Miaouff)
- [ ] Cahier des charges / expression des besoins
- [ ] Présentation du contexte (projet de formation) + gestion de projet (planning, suivi, qualité)
- [ ] **Architecture logicielle** (schéma multicouche + rôle des couches + sécurité)
- [ ] **Maquettes + enchaînement des écrans**
- [ ] **MCD + MPD** de la base
- [ ] **Script de création** de la base de données
- [ ] **Diagramme de cas d'utilisation**
- [ ] **Diagramme(s) de séquence** des cas les plus significatifs
- [ ] Spécifications techniques (dont sécurité)
- [ ] **Extraits de code** significatifs : UI, métier, accès données, autres + **arguments de choix (dont sécurité)**
- [ ] **Présentation des éléments de sécurité** (recoupe §3)
- [ ] **Plan de tests** (recoupe §4)
- [ ] **Jeu d'essai** de la fonctionnalité la plus représentative (entrée/attendu/obtenu + écarts)
- [ ] **Veille sécurité** : vulnérabilités suivies + failles trouvées/corrigées
- [ ] Synthèse / conclusion
- [ ] Anglais : être prêt sur le vocabulaire technique (questionnaire + extraits B1)

---

## 12. Plan d'action priorisé

### Lot 1 — Sécurité (le plus urgent, très valorisé) — ✅ FAIT
1. ✅ Décorateur `@admin_required` sur toutes les routes admin (faille critique corrigée).
2. ✅ CSRF (Flask-WTF) sur tous les formulaires + header `X-CSRFToken` sur les fetch.
3. ✅ Cookies de session sécurisés (HttpOnly, SameSite, Secure en prod) + `MAX_CONTENT_LENGTH`.
4. ✅ En-têtes de sécurité (CSP, X-Frame-Options, nosniff, Referrer-Policy, HSTS, Permissions-Policy).
5. ✅ Rate limiting (Flask-Limiter) sur login/reset/send_reset_code.
6. ✅ Tokens de reset : expiration 15 min, comparaison constante, usage unique, vérif force du mot de passe. *(persistance en base = amélioration future restante)*
7. ✅ `re.escape` sur la recherche Mongo. *(XSS articles : non concerné — Jinja échappe déjà, pas de `|safe`.)*

### Lot 2 — Tests (chantier CP9) — 🟢 EN GRANDE PARTIE FAIT
8. ✅ Tests unitaires `services/` + intégration routes + ✅ tests d'autorisation admin (régression sécurité).
9. ✅ Tests de sécurité : CSRF (rejet/acceptation) + rate-limiting (429). *(injection SQL/NoSQL : couverte par l'ORM + `re.escape`.)*
10. 🔴 Reste : E2E Playwright des 3 parcours + jeu d'essai documenté.
11. 🔴 Reste : CI étendue (bandit, pip-audit, seuil de couverture).

### Lot 3 — Qualité de code & outillage (rapide, fort effet « pro »)
12. **pre-commit** + **black** + **isort** + **flake8** + **Prettier** + **.editorconfig**.
13. **gitleaks/detect-secrets** (pre-commit + CI) ; vérifier/retirer `dump.sql`, nettoyer `.gitignore`.
14. **vulture** : supprimer tout le code mort ; docstrings + commentaires **en anglais** + type hints.
15. (Argument d'archi) refactor `app.py` en **Blueprints** par domaine.

### Lot 4 — Qualité transverse (visible au jury) — 🟢 EN GRANDE PARTIE FAIT
16. ✅ SEO : title/description par page, canonical, OG/Twitter, sitemap.xml, robots.txt, noindex admin, favicon corrigé. *(reste : JSON-LD Schema.org — bonus.)*
17. 🟡 Performance : ✅ lazy-loading images + cache HTTP assets (30 j). *(reste : conversion WebP + audit Lighthouse + index BDD.)*
18. 🟡 Accessibilité : ✅ lien d'évitement + ancre `#main-content`. *(reste : audit axe/WAVE + corrections.)* · Éco : ✅ lazy + cache + sobriété. *(reste : mesure EcoIndex + démarche GreenIT documentée.)*
19. ✅ RGPD : bandeau de consentement cookies fait (Lot bandeau). *(reste : droit à l'effacement.)*

### Lot 5 — Documentaire (pour le dossier)
20. MCD/MPD, diagrammes UML (cas d'utilisation, séquence), maquettes, architecture, cahier des charges, planning, dossier projet 40–60 pages.
21. (Bonus DevOps) `docker-compose` + procédure de déploiement documentée pour cocher pleinement CP1/CP10/CP11.

---

*Ce document est une base de travail interne, pas un livrable d'examen tel quel.*
