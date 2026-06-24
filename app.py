import streamlit as st
from src.ui_components import render_interface

st.set_page_config(page_title="Fanoron-telo avec IA", layout="centered")

# Initialisations globales indispensables
if "mode_jeu" not in st.session_state:
    st.session_state.mode_jeu = "Humain vs Machine"

if "difficulte_ia" not in st.session_state:
    st.session_state.difficulte_ia = "Difficile"  # Choix : Facile, Moyenne, Difficile

if "plateau" not in st.session_state:
    st.session_state.plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

if "phase" not in st.session_state:
    st.session_state.phase = "Placement"

if "tour" not in st.session_state:
    st.session_state.tour = 1  # 1 = Humain (Noir), 2 = IA / Second Joueur (Blanc)

if "pions_places" not in st.session_state:
    st.session_state.pions_places = 0

if "gagnant" not in st.session_state:
    st.session_state.gagnant = None

if "stats_perf" not in st.session_state:
    st.session_state.stats_perf = []

if "pion_selectionne" not in st.session_state:
    st.session_state.pion_selectionne = None

render_interface()