## - Section 1 : En-tête institutionnel et Identification

### 1. Lien hypertexte vers le site officiel de l'institut :
https://ispm-edu.com

### 2. Nom du groupe de projet : **Lemurien-Codeur**


### 3. Tableau listant les membres de l'équipe :

| 		**Nom Complet**                       | **Numéro d'étudiant** |  **Classe** | **Rôle précis pour ce hackathon** |
|-------------------------------------------------|-------------------|---------|-------------------------------|
| RANAIVONOHATRA Mahentsoa Akel                   | 	   02	      | ESIIA 4 | 				                |
| RAJOELISOLO Sitraka Tsitohaina                  | 	   05	      | ESIIA 4 | 				                |
| ANDRISOAMALALA Volakanto Landréa                | 	   10	      | ESIIA 4 | 				                |
| RAMESON Andrianarinosy Imanoela Fiderana Ny Avo | 	   12	      | ESIIA 4 | 				                |
| TANG Fakanah Randy                              | 	   27	      | ESIIA 4 | 				                |
| LEONARD Jamaviston Lucas                        | 	   36	      | ESIIA 4 | 				                |
|-------------------------------------------------|-------------------|---------|-------------------------------|

## - Section 2 : Description du Travail Réalisé

### 1. Présentation globale de votre application et des fonctionnalités implémentées:<br>
**1. Le Contexte** <br>
Le **Fanoron-telo** est un jeu de société traditionnel originaire de Madagascar. Se jouant sur un plateau de 3x3 intersections connectées avec 3 pions par joueur, il propose des règles simples mais une profondeur tactique propice à l’optimisation algorithmique.<br>

**2. Règles du Jeu**<br>
Le plateau comprend 9 intersections. Chaque joueur possède 3 pions.<br>

* **Phase 1 (Placement)** : Les joueurs posent un pion à tour de rôle sur une intersection libre. Si un joueur aligne ses 3 pions (ligne, colonne ou diagonale) pendant cette phase, il gagne immédiatement.<br>
* **Phase 2 (Mouvement)** : Si aucun alignement n’est fait après la pose des 6 pions, chacun déplace à tour de rôle un pion vers une intersection adjacente libre en suivant les lignes. Le premier qui aligne ses 3 pions gagne.<br>

**3. Objectifs et Fonctionnalités Attendues**<br>
Dans le cadre de ce hackathon, les fonctionnalités sont classées par priorité :<br>

* **Priorité 1** : Mode Humain vs Humain en local + Mode Humain vs IA (Niveau Facile/Moyen) + Gestion robuste des règles du jeu.<br>
* **Priorité 2** : Mode IA vs IA (Mode Démo) + IA Difficile (Alpha-Beta optimisé) + Déploiement/Hébergement en ligne.<br>
* **Priorité 3** : Option d’annulation de coup (*Undo/Redo*), design d’interface soigné, animations.<br>

### 2. Présentation de l'architecture et de la pile (stack) technologique utilisée :<br>

Le projet **Fanoron-telo avec IA** a été développé en **Python**, un langage de programmation adapté à la conception d’algorithmes et à l’implémentation de l’intelligence artificielle. L’interface utilisateur ainsi que l’exécution de l’application ont été réalisées avec **Streamlit**, un framework Python permettant de créer rapidement des applications web interactives. Pour le déploiement et l’hébergement, nous avons utilisé **Streamlit Community Cloud**, ce qui permet d’exécuter le jeu directement depuis un navigateur sans nécessiter d’installation locale. Cette architecture simple et légère facilite le développement, la maintenance et l’accessibilité de l’application.


### 3. Lien vers la version hébergée, le cas échéant :

## - Section 3 : Guide d'Installation Rapide

. Procédure pas-à-pas pour cloner, installer les dépendances et lancer l'application en local :

## - Section 4 : Outils d'Aide IA Utilisés

1. Explication de la manière dont votre équipe a exploité les assistants IA (ex. GitHub Copilot, ChatGPT, Claude, etc.) pour accélérer le développement : 

2. Exemples d'utilisation (écriture d'algorithmes, génération de tests rapides, débogage, CSS, génération d'images, génération de documentation) et retour d'expérience sur le gain de temps obtenu.

## - Section 5 : Modélisation et Algorithmes de l'IA du Jeu

1. Explication scientifique de l'intelligence artificielle que vous avez conçue et implémentée :

  1. Représentation de l'état du plateau : Comment avez-vous représenté le plateau 3x3 et ses lignes diagonales/orthogonales (Structures de Données).

  2. Fonctionnement de votre Minimax et définition de la fonction d'évaluation.

  3. Les techniques avancées utilisées (le cas échéant) :

  	1. Table de transposition pour stocker les états déjà évalués et éviter les calculs redondants.

	2. Opening book, c'est-à-dire une bibliothèque de coups d'ouverture prédéfinis.

	3. bit à bit / bitboards.

	4. Iterative deepening.

	5. Machine Learning : Rote learning (mémorisation/indexation), modèle de classification, Q-Learning...

## - Section 6 : Analyses de Performances

1. Temps de réponse moyen de l'IA (en millisecondes) lors de la recherche du meilleur coup : 

2. Résultats ou statistiques des affrontements IA contre IA (ex. l'IA difficile bat-elle l'IA moyenne dans 100% des cas ?) :

3. D'autres métriques liées aux éventuelles techniques avancées utilisées :
