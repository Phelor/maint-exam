# Projet maintenance applicative

## Contexte

Un développeur alcoolisé et sous pression a pondu à la hâte un petit service de gestion de tâches en Python.  
Le code fonctionne (à peu près), mais regorge de bugs subtils, de duplications, et n’obéit à aucune des bonnes pratiques modernes.

## Objectifs du projet

1. Corriger tous les **bugs** (comportements incorrects ou inattendus) tout en conservant la logique métier existante.
2. Réorganiser l’architecture selon les principes **SOLID**, en appliquant également **DRY** et **KISS**.
3. Introduire un minimum de **programmation fonctionnelle** (fonctions pures, immutabilité partielle, utilisation de `map`/`filter`/compréhensions).
4. Mettre en place un **couche d’abstraction** pour la persistance (dépendance inversée) afin de pouvoir remplacer facilement le stockage JSON par une base de données ou un mock pour tests.
5. Écrire une **suite de tests unitaires** exhaustive :
   - **Happy paths** : scénarios normaux (ajout, suppression, recherche, listing).
   - **Unhappy paths** : cas d’erreur ou d’usage incorrect (ID inexistant, fichier corrompu, format invalide, permissions refusées, etc.).
6. Vérifier dans les tests que le fichier `tasks.json` est bien mis à jour (lecture et écriture) et que son contenu est conforme après chaque opération.

## Consignes détaillées

### 1. Structure du code

- Séparer clairement :
  - la **gestion du domaine** (modèle `Task`, logique de création/recherche/suppression),
  - la **couche de persistance** (interface abstraite + implémentation JSON),
  - la **couche CLI** (parsing des arguments, affichage utilisateur).
- Utiliser `argparse`, `click` ou équivalent pour gérer les commandes `add`, `remove`, `list`, `find`.

### 2. SOLID

- **Single Responsibility** : chaque classe ou module ne doit avoir qu’une seule raison de changer.
- **Open/Closed** : extension sans modification des classes existantes (ajout d’un nouveau backend de stockage ou d’une nouvelle commande).
- **Liskov Substitution** : toute implémentation de l’interface de stockage doit pouvoir remplacer l’ancienne sans casser la logique.
- **Interface Segregation** : découper les interfaces (persist/chargement, recherche, modification).
- **Dependency Inversion** : la couche métier ne doit pas dépendre directement de JSON, mais d’une abstraction `StorageBackend`.

### 3. DRY & KISS

- Extraire les lectures/écritures de fichier en utilitaires réutilisables.
- Utiliser des compréhensions de liste ou fonctions `filter`/`map` pour les recherches.
- Éviter les fonctions trop longues : max ~20 lignes par fonction.

### 4. Programmation fonctionnelle

- Favoriser les **fonctions pures** pour calculer les nouveaux états de liste de tâches (retourner une nouvelle liste, ne pas modifier en place).

### 5. Tests unitaires

- Choisir un framework (`pytest`, `unittest`…) et créer un dossier `tests/`.
- **Happy paths** :
  - Ajout d’une tâche → `tasks.json` contient la nouvelle tâche avec ID incrémental.
  - Suppression d’une tâche existante → tâche retirée, IDs inexistants non affectés.
  - Recherche de mots-clés présents et absents.
  - Listing global.
- **Unhappy paths** :
  - Suppression avec ID inexistant → lève une exception ou retourne `False`.
  - Fichier JSON corrompu → lever/attraper et logguer une erreur propre.
  - Permissions d’écriture refusées → comportement contrôlé.
  - Arguments CLI manquants ou mal formés → code de sortie non nul et message d’aide.

### 6. Critères d’évaluation

- **Maintenabilité** : conformité aux principes SOLID, découplage des responsabilités, code lisible et bien structuré.
- **Qualité des tests** : couverture autour de 90 %, tests clairs et indépendants, bonne isolation de la couche de persistance.
- **Performance** : réduction de la complexité algorithmique (passer des recherches O(n) à O(1) si pertinent), suppression des appels de fichier redondants.
- **Robustesse** : gestion propre des cas d’erreur, absence de comportements inattendus.

## Livrables

Votre repository git contenant :

- Le code source refactoré.
- Le dossier `tests/` contenant tous les tests unitaires.
- Un fichier `README.md` décrivant l’architecture, les choix effectués et la procédure pour exécuter les tests.
- Un fichier `AUTHORS` contenant les adresses email des membres de votre groupe (e.g. john.doe@etu.univ-lyon1.fr)

Bonne refactorisation et bon débogage !

# Contributors
- Baptiste Rousselot baptiste.rousselot@etu.univ-lyon1.fr
- Eliott Sauvaget eliott.sauvaget@etu.univ-lyon1.fr