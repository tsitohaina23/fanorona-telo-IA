import streamlit as st
from src.ui_components import render_interface

st.set_page_config(page_title="Fanoron-telo avec IA", layout="centered")

# 🌟 CRUCIAL : Initialisation complète des états si absents pour alimenter le JS
if "plateau" not in st.session_state:
    # Matrice 3x3 vide (0 = vide, 1 = Joueur, 2 = IA)
    st.session_state.plateau = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
if "phase" not in st.session_state:
    st.session_state.phase = "Placement"
if "tour" not in st.session_state:
    st.session_state.tour = 1  # 1 = Humain, 2 = IA
if "pions_places" not in st.session_state:
    st.session_state.pions_places = 0
if "gagnant" not in st.session_state:
    st.session_state.gagnant = None
if "stats_perf" not in st.session_state:
    st.session_state.stats_perf = []

# Appel du rendu
render_interface()