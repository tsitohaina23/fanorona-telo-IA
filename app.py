import streamlit as st
import pandas as pd
# Imports depuis le dossier src/
from src.game_logic import initialiser_plateau
from src.ui_components import render_interface

st.set_page_config(
    page_title="Fanoron-telo IA - ISPM",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------------------------------
# INITIALIZATION DES ÉTATS (SESSION STATE)
# -------------------------------------------------------------------------
if "plateau" not in st.session_state:
    st.session_state.plateau = initialiser_plateau()
if "tour" not in st.session_state:
    # 1 = Joueur Humain (❌), 2 = IA ou Joueur 2 (⭕)
    st.session_state.tour = 1 
if "phase" not in st.session_state:
    # 'Placement' (jusqu'à 6 pions posés) ou 'Mouvement'
    st.session_state.phase = "Placement"  
if "pions_places" not in st.session_state:
    # Compteur pour basculer automatiquement de phase
    st.session_state.pions_places = 0  
if "gagnant" not in st.session_state:
    st.session_state.gagnant = None
if "stats_perf" not in st.session_state:
    # Pour la Section 6 du README (Analyses de performances)
    st.session_state.stats_perf = [] 

# -------------------------------------------------------------------------
# AFFICHAGE DE L'INTERFACE
# -------------------------------------------------------------------------
st.title("🧠 Fanoron-telo avec IA")
st.caption("Projet Hackathon - Institut Supérieur Polytechnique de Madagascar")

render_interface()

# Pied de page informatif
st.markdown("---")
st.caption("Développé en 5 heures par l'équipe. ISPM 2026.")