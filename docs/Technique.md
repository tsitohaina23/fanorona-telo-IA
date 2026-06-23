Structures dossiers:
fanorona-telo-ia/
│
├── assets/                     # Fichiers statiques globaux
│   └── style.css
│
├── src/                        # Tout le code source applicatif
│   ├── __init__.py
│   ├── game_logic.py           # Logique pure des règles (Mouvements, Alignements, Victoires)
│   ├── ia_engine.py            # Moteur IA (Calcul des scores, Minimax/Alpha-Beta)
│   ├── ui_components.py        # Structure de la page, menus déroulants et synchronisation
│   │
│   └── components/             # Zone des composants frontend personnalisés
│       └── fanorona_board/
│           ├── __init__.py     # Déclaration / Pont Python du composant
│           ├── index.html      # Rendu visuel Premium et interactions JS rapides
│           └── streamlit-component-lib.js # Communication Streamlit-JS
│
├── app.py                      # Point d'entrée de l'application Streamlit (Racine)
├── README.md                   # Rapport obligatoire de l'évaluation
└── requirements.txt            # Liste des dépendances (Streamlit, Pandas, etc.)

cree une environnement .env en locla avec commande:
python -m venv .venv

# 2. L'activer
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py