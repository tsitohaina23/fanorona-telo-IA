## - Section 1 : En-tête institutionnel et Identification

### 1. Lien hypertexte vers le site officiel de l'institut :
https://ispm-edu.com

### 2. Nom du groupe de projet : **Lemurien-Codeur**


### 3. Tableau listant les membres de l'équipe :

| 		**Nom Complet**                       | **Numéro d'étudiant** |  **Classe** | **Rôle précis pour ce hackathon** |
|-------------------------------------------------|-------------------|---------|-------------------------------|
| RANAIVONOHATRA Mahentsoa Akel                   | 	   02	      | ESIIA 4 | 			Tech Lead	                |
| RAJOELISOLO Sitraka Tsitohaina                  | 	   05	      | ESIIA 4 | Développeur Backend et Développeur IA                |
| ANDRISOAMALALA Volakanto Landréa                | 	   10	      | ESIIA 4 | Integration de l'algorithme ML				                |
| RAMESON Andrianarinosy Imanoela Fiderana Ny Avo | 	   12	      | ESIIA 4 | 			Développeur Frontend	                |
| TANG Fakanah Randy                              | 	   27	      | ESIIA 4 | 		Développeur Backend		                |
| LEONARD Jamaviston Lucas                        | 	   36	      | ESII A 4| Développeur IA                |
|Razafimanantsoa Betina							|			23			|	ESII A 4|Vérification final			|

## - Section 2 : Description du Travail Réalisé

### 2.1. Présentation globale de votre application et des fonctionnalités implémentées:<br>
**2.1.1. Le Contexte** <br>
Le **Fanoron-telo** est un jeu de société traditionnel originaire de Madagascar. Se jouant sur un plateau de 3x3 intersections connectées avec 3 pions par joueur, il propose des règles simples mais une profondeur tactique propice à l’optimisation algorithmique.<br>

**2.1.2. Règles du Jeu**<br>
Le plateau comprend 9 intersections. Chaque joueur possède 3 pions.<br>

* **Phase 1 (Placement)** : Les joueurs posent un pion à tour de rôle sur une intersection libre. Si un joueur aligne ses 3 pions (ligne, colonne ou diagonale) pendant cette phase, il gagne immédiatement.<br>
* **Phase 2 (Mouvement)** : Si aucun alignement n’est fait après la pose des 6 pions, chacun déplace à tour de rôle un pion vers une intersection adjacente libre en suivant les lignes. Le premier qui aligne ses 3 pions gagne.<br>

**2.2.3. Objectifs et Fonctionnalités Attendues**<br>
Dans le cadre de ce hackathon, les fonctionnalités sont classées par priorité :<br>

* **Priorité 1** : Mode Humain vs Humain en local + Mode Humain vs IA (Niveau Facile/Moyen) + Gestion robuste des règles du jeu.<br>
* **Priorité 2** : Mode IA vs IA (Mode Démo) + IA Difficile (Alpha-Beta optimisé) + Déploiement/Hébergement en ligne.<br>
* **Priorité 3** : Option d’annulation de coup (*Undo/Redo*), design d’interface soigné, animations.<br>

### 2.2. Présentation de l'architecture et de la pile (stack) technologique utilisée :<br>

Le projet **Fanoron-telo avec IA** a été développé en **Python**, un langage de programmation adapté à la conception d’algorithmes et à l’implémentation de l’intelligence artificielle. L’interface utilisateur ainsi que l’exécution de l’application ont été réalisées avec **Streamlit**, un framework Python permettant de créer rapidement des applications web interactives. Pour le déploiement et l’hébergement, nous avons utilisé **Streamlit Community Cloud**, ce qui permet d’exécuter le jeu directement depuis un navigateur sans nécessiter d’installation locale. Cette architecture simple et légère facilite le développement, la maintenance et l’accessibilité de l’application.
### 2.3. Lien vers la version hébergée, le cas échéant :
https://drive.google.com/file/d/1SluygrtcQDmPGpNFeCKxJbrHn99tou8r/view?usp=sharing

## - Section 3 : Guide d'Installation Rapide<br>
  **I.** Cloner le projet et entrer dans le dossier:
git clone https://github.com/tsitohaina23/fanorona-telo-IA.git && cd fanorona-telo-IA <br>

 **II.** Créer le venv, l'activer, installer les dépendances et initialiser le fichier .env
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && echo. > .env<br>

 **III.** Lancer l'application Fanorona Telo
streamlit run app.py

## - Section 4 : Outils d'Aide IA Utilisés

Notre équipe a principalement exploité **Gemini** comme assistant IA afin d’accélérer le développement du projet. Il a été utilisé pour la génération de portions de code, la proposition d’une structure de projet cohérente et bien organisée, ainsi que pour la résolution de certains problèmes de débogage rencontrés au cours du développement. L’assistant nous a également fourni diverses suggestions concernant les choix techniques, l’organisation des fonctionnalités et les différentes étapes du processus de réalisation. Son utilisation nous a permis de gagner du temps, d’améliorer la qualité du code et d’adopter une démarche de développement plus efficace.


## - Section 5 : Modélisation et Algorithmes de l'IA du Jeu

### Explication scientifique de l'intelligence artificielle que nous avons conçue et implémentée :

   Notre IA a été conçue comme un moteur de recherche adversariale capable de choisir les meilleurs coups à partir de l'état courant du plateau. Les niveaux Facile et Moyen reposent sur une logique de recherche simple, tandis que le niveau Difficile combine Minimax, Alpha-Beta et une représentation par bitboards pour accélérer le calcul et améliorer la qualité des décisions. Le mode ML complète cette approche par une mémoire de certains états déjà rencontrés, ce qui permet à l'IA de réagir plus efficacement dans des situations similaires.

### Représentation de l'état du plateau :
      Le plateau est représenté sous forme de matrice 3x3 où chaque case peut contenir un pion libre, un pion du joueur 1 ou un pion du joueur 2. Pour améliorer la rapidité des calculs, cette structure est également encodée sous forme de bitboards, ce qui facilite la détection des alignements et l'évaluation des positions.

### Fonctionnement du Minimax et de la fonction d'évaluation :
      Le Minimax explore les différentes branches possibles du jeu en supposant que chaque joueur joue de manière optimale. À chaque profondeur, l'algorithme attribue une valeur à une position selon sa qualité pour le joueur courant. Cette évaluation repose sur plusieurs critères : la présence d'alignements potentiels, les menaces immédiates, le contrôle des cases clés et la possibilité de bloquer l'adversaire. L'élagage Alpha-Beta réduit ensuite le nombre de branches à explorer sans diminuer significativement la qualité du choix.

### Techniques avancées utilisées :
      - Alpha-Beta pruning : optimisation du Minimax pour éviter de parcourir des branches inutiles.
      - Bitboards : représentation compacte des pions sous forme de bits pour une évaluation plus rapide.
      - Rote learning : mémoire simple utilisée dans le mode ML pour retenir certains états rencontrés et améliorer les décisions futures.
      - Recherche en profondeur limitée : adaptation du temps de calcul selon le niveau de difficulté choisi.

   En résumé, notre IA combine recherche, évaluation heuristique et optimisation algorithmique pour proposer des coups cohérents, rapides et stratégiques tout au long de la partie.

## - Section 6 : Analyses de Performances

1. Temps de réponse moyen de l'IA (en millisecondes) lors de la recherche du meilleur coup : **32ms**

2. Résultats ou statistiques des affrontements IA contre IA (ex. l'IA difficile bat-elle l'IA moyenne dans 100% des cas ?) : l'IA difficile bat l'IA moyenne dans 100% des cas car l'IA difficile utilise une profondeur de **niveau 7** pour gagner tandis que l'IA moyenne est **entre 3 a 5 seulement**

3. D'autres métriques liées aux éventuelles techniques avancées utilisées :
