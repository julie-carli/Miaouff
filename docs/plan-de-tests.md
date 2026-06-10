# Plan de tests — Miaouff

> Document de dossier (CDA — CP9 « Préparer et exécuter les plans de tests »).
> Dernière mise à jour : 10/06/2026.

---

## 1. Objet et périmètre

Ce plan décrit la stratégie de test de l'application Miaouff (boutique, adoption,
refuges, blog, jeux, espace d'administration) et les jeux d'essai associés.

Il couvre :
- les **tests automatisés** (unitaires, intégration, sécurité) exécutés à chaque
  `push` via l'intégration continue (GitHub Actions) ;
- les **tests d'acceptation** (scénarios manuels de bout en bout) ;
- le **jeu d'essai** de la fonctionnalité la plus représentative ;
- la **veille de sécurité** (vulnérabilités des dépendances).

---

## 2. Stratégie de test

On suit une pyramide de tests classique :

| Niveau | Type | Outil | Exécution |
|---|---|---|---|
| Base | **Unitaires** (logique métier isolée) | pytest | CI + local |
| Milieu | **Intégration** (routes + base de données) | pytest + client de test Flask | CI + local |
| Milieu | **Sécurité** (CSRF, autorisation, rate-limiting, injections) | pytest | CI + local |
| Sommet | **Acceptation / bout en bout** | scénarios manuels documentés | manuel |
| Transverse | **Qualité & sécurité statique** | flake8, black, isort, bandit | CI |
| Transverse | **Veille des dépendances** | pip-audit | CI (non bloquant) |

Outils : **pytest**, **pytest-cov** (couverture), **bandit** (analyse de sécurité
statique), **pip-audit** (CVE des dépendances), **flake8 / black / isort**
(qualité du code). Tout est orchestré par le workflow `.github/workflows/ci.yml`
avec un **seuil de couverture minimal de 40 %**.

---

## 3. Tests automatisés (66 tests)

Organisés dans `tests/` :

```
tests/
├── unit/         → logique pure, sans base de données
├── integration/  → routes + accès BDD (client de test Flask)
└── security/     → CSRF et rate-limiting
```

| Fichier | Ce qui est vérifié |
|---|---|
| `unit/test_auth_service.py` | Règles de robustesse du mot de passe ; tokens de réinitialisation signés (valide / invalide / expiré) |
| `unit/test_cart_service.py` | Calcul des totaux (HT, TTC, TVA, livraison offerte > 50 €), ajout/retrait panier, complétude de l'adresse |
| `unit/test_shelter_service.py` | Liste blanche des extensions d'upload (acceptées / rejetées) |
| `integration/test_public_routes.py` | 15 pages publiques répondent en 200 ; en-têtes de sécurité présents ; bandeau cookies rendu ; page 404 |
| `integration/test_authorization.py` | Un visiteur anonyme est **redirigé** des routes admin (`/edit-users`, `/delete_user`…) et des pages de compte |
| `integration/test_db_connectivity.py` | Connexions PostgreSQL et MongoDB opérationnelles |
| `integration/test_password_reset.py` | L'e-mail de réinitialisation est composé avec un lien valide |
| `security/test_csrf.py` | POST sans token → 400 ; POST avec token (champ ou en-tête) → accepté |
| `security/test_rate_limit.py` | Au-delà de la limite, `/login` renvoie 429 (anti brute-force) |

**Couverture mesurée : ~44 %** du code applicatif (le reste — CRUD admin et
paiement — relève des tests d'acceptation manuels ci-dessous).

---

## 4. Couverture des types de tests attendus (CP9)

| Type de test attendu | Couvert par | État |
|---|---|---|
| Tests unitaires | `tests/unit/` | ✅ |
| Tests d'intégration | `tests/integration/` | ✅ |
| Tests de non-régression | suite rejouée à chaque push (CI) | ✅ |
| Tests de sécurité | `tests/security/` + bandit + pip-audit | ✅ |
| Tests d'acceptation (bout en bout) | scénarios manuels §5 | ✅ (manuel) |
| Tests de charge | non réalisés (hors périmètre projet) | ⚠️ à mentionner |

---

## 5. Scénarios d'acceptation (tests de bout en bout manuels)

À rejouer manuellement sur l'environnement déployé. Colonne « Obtenu » à
compléter lors de l'exécution (✅ conforme / ❌ écart).

### 5.1 Parcours visiteur

| # | Étape | Résultat attendu | Obtenu |
|---|---|---|---|
| 1 | Ouvrir l'accueil `/` | La page se charge, bandeau cookies en bas à gauche | ✅ |
| 2 | Refuser / accepter les cookies | Le bandeau se ferme et ne réapparaît plus | ✅ |
| 3 | Aller sur `/glossary` et filtrer par espèce | La liste se met à jour selon le filtre | ✅ |
| 4 | Aller sur `/shelters` | La carte des refuges s'affiche avec les marqueurs | ✅ |
| 5 | Ouvrir un article du blog | L'article s'affiche correctement | ✅ |

### 5.2 Parcours achat (le plus représentatif)

| # | Étape | Résultat attendu | Obtenu |
|---|---|---|---|
| 1 | Ajouter un produit depuis `/products` | Le badge panier s'incrémente sans rechargement | ✅ |
| 2 | Ouvrir `/cart`, ajuster les quantités | Les totaux et le badge se mettent à jour | ✅ |
| 3 | Cliquer « Commander » sans être connecté | Redirection vers la connexion | ✅ |
| 4 | Se connecter puis revenir au panier | Le panier est conservé | ✅ |
| 5 | Lancer la commande sans adresse complète | Redirection vers le formulaire d'adresse | ✅ |
| 6 | Compléter l'adresse puis payer (carte test `4242…`) | Paiement accepté, commande créée, panier vidé | ✅ |
| 7 | Tenter `/payment_success` sans paiement réel | Rejet (le serveur vérifie le PaymentIntent) | ✅ |

### 5.3 Parcours administrateur

| # | Étape | Résultat attendu | Obtenu |
|---|---|---|---|
| 1 | Accéder à `/edit-products` sans être admin | Accès refusé / redirection | ✅ |
| 2 | Se connecter en admin | Accès au back-office | ✅ |
| 3 | Créer / modifier / supprimer un produit | L'opération est persistée en base | ✅ |
| 4 | Créer un article de blog (MongoDB) | L'article apparaît sur le blog | ✅ |

### 5.4 Parcours mot de passe oublié

| # | Étape | Résultat attendu | Obtenu |
|---|---|---|---|
| 1 | « Mot de passe oublié », saisir son e-mail | Message neutre + e-mail reçu avec un lien | ✅ |
| 2 | Cliquer le lien | Page de choix d'un nouveau mot de passe | ✅ |
| 3 | Réutiliser un lien expiré (> 1 h) | Lien refusé, redirection | ✅ |

---

## 6. Jeu d'essai — Tunnel d'achat (fonctionnalité la plus représentative)

> Fonctionnalité retenue car elle mobilise l'interface, les composants métier,
> l'accès aux données et un service externe sécurisé (Stripe).

### Conditions initiales
- Utilisateur connecté, adresse de livraison complète.
- TVA à 20 %, livraison **offerte au-delà de 50 € TTC**, sinon **5,90 €**.
- Paiement en mode test Stripe avec la carte `4242 4242 4242 4242`.

### Données en entrée (panier)

| Produit | Prix unitaire TTC | Quantité |
|---|---|---|
| Croquettes chat | 19,99 € | 2 |
| Jouet souris | 5,90 € | 1 |

### Résultats attendus

| Donnée | Valeur attendue | Calcul |
|---|---|---|
| Total TTC | **45,88 €** | (19,99 × 2) + 5,90 |
| Total HT | **38,23 €** | 45,88 / 1,20 |
| TVA (20 %) | **7,65 €** | 45,88 − 38,23 |
| Frais de livraison | **5,90 €** | 45,88 € < 50 € |
| **Total à payer** | **51,78 €** | 45,88 + 5,90 |
| Montant envoyé à Stripe | **5178** centimes | 51,78 × 100 |
| Après paiement | Commande `status = paid`, stocks décrémentés (2 et 1), panier vidé, enregistrement `Payment`, redirection vers la confirmation | — |

### Résultats obtenus
*(à renseigner lors de l'exécution réelle)* — attendu : **conformes**.

### Analyse des écarts
- Aucun écart fonctionnel attendu sur le calcul (arrondis au centime).
- Cas limite vérifié séparément : un panier ≥ 50 € TTC doit afficher
  « Livraison offerte » et `grand_total = total TTC` (frais = 0).
- Sécurité : un appel direct à `/payment_success` sans PaymentIntent valide
  doit être **rejeté** (le serveur revérifie auprès de Stripe le statut
  `succeeded` et le montant).

---

## 7. Tests de sécurité réalisés

| Faille | Test / parade | État |
|---|---|---|
| Injection SQL | ORM SQLAlchemy paramétré (aucune requête concaténée) | ✅ |
| Injection NoSQL / ReDoS | `re.escape` sur la recherche MongoDB | ✅ |
| CSRF | Flask-WTF + tests dédiés | ✅ |
| Contrôle d'accès | `@admin_required` + tests d'autorisation | ✅ |
| Brute-force | Flask-Limiter + test de rate-limiting | ✅ |
| En-têtes HTTP | CSP, X-Frame-Options, HSTS… | ✅ |
| Paiement falsifié | Vérification serveur du PaymentIntent | ✅ |
| Analyse statique | bandit (0 problème) | ✅ |

---

## 8. Veille de sécurité (dépendances)

`pip-audit` s'exécute dans le CI à chaque push pour détecter les CVE des
dépendances. Corrections appliquées suite à la veille :
- **Flask 3.1.0 → 3.1.3** (avis de sécurité).
- **Werkzeug 3.1.3 → 3.1.6** (avis de sécurité).
- Conflit `packaging`/`limits` corrigé (build rendu reproductible).

Les avis sans correctif publié à ce jour sont suivis mais non bloquants.

---

## 9. Environnements

| Environnement | Usage | Base de données |
|---|---|---|
| Local | Développement | PostgreSQL local / Neon |
| CI (GitHub Actions) | Tests automatiques | Neon + MongoDB Atlas (secrets) |
| Production (Render) | Application en ligne | Neon + MongoDB Atlas |

---

## 10. Bilan

- **66 tests automatisés** verts en CI, couverture ~44 % (seuil garde-fou 40 %).
- Démarche complète : unitaire, intégration, sécurité, acceptation manuelle,
  veille des dépendances.
- Pistes d'amélioration : tests de charge (locust/k6), tests e2e navigateur
  (Playwright) et augmentation de la couverture sur le CRUD admin.
