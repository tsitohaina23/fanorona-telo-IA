Structures dossiers:
fanoron-telo-ia/
│
├── assets/               # Images, icônes des pions, style CSS
│   └── style.css
│
├── src/                  # Tout le code source est rangé ici
│   ├── game_logic.py     # Règles du jeu et plateau
│   ├── ia_engine.py      # Algorithmes IA (Minimax / Alpha-Beta)
│   └── ui_components.py  # Éléments visuels Streamlit
│
├── app.py                # Point d'entrée principal (à la racine)
├── README.md             # Rapport obligatoire (6 sections)
└── requirements.txt      # Dépendances du projet

cree une environnement .env en locla avec commande:
python -m venv .venv

# 2. L'activer
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py