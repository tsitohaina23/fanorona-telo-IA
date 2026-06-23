import streamlit as st
import time
import copy
import numpy as np
from src.game_logic import verifier_alignement, est_mouvement_valide

def evaluer_plateau(plateau):
    """
    Évaluation défensive et offensive :
    +100 si l'IA gagne.
    -100 si l'humain gagne (à éviter absolument pour l'IA).
    """
    if verifier_alignement(plateau, 2): return 100
    if verifier_alignement(plateau, 1): return -100
    return 0

def generer_coups_possibles(plateau, phase, joueur):
    coups = []
    if phase == "Placement":
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == 0: coups.append((i, j))
    elif phase == "Mouvement":
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == joueur:
                    for di in range(3):
                        for dj in range(3):
                            # S'assure que la destination est vide ET respecte les lignes tracées
                            if plateau[di][dj] == 0 and est_mouvement_valide(i, j, di, dj):
                                coups.append(((i, j), (di, dj)))
    return coups

def minimax(plateau, profondeur, est_max, phase):
    score = evaluer_plateau(plateau)
    # Fin de simulation ou coup décisif trouvé
    if score == 100 or score == -100 or profondeur == 0:
        return score
        
    if est_max:
        meilleur_score = -float('inf')
        for coup in generer_coups_possibles(plateau, phase, 2):
            p_virtuel = copy.deepcopy(plateau)
            if phase == "Placement": p_virtuel[coup[0]][coup[1]] = 2
            else: p_virtuel[coup[0][0]][coup[0][1]], p_virtuel[coup[1][0]][coup[1][1]] = 0, 2
            
            score_coup = minimax(p_virtuel, profondeur - 1, False, phase)
            meilleur_score = max(meilleur_score, score_coup)
        return meilleur_score if meilleur_score != -float('inf') else 0
    else:
        meilleur_score = float('inf')
        for coup in generer_coups_possibles(plateau, phase, 1):
            p_virtuel = copy.deepcopy(plateau)
            if phase == "Placement": p_virtuel[coup[0]][coup[1]] = 1
            else: p_virtuel[coup[0][0]][coup[0][1]], p_virtuel[coup[1][0]][coup[1][1]] = 0, 1
            
            score_coup = minimax(p_virtuel, profondeur - 1, True, phase)
            meilleur_score = min(meilleur_score, score_coup)
        return meilleur_score if meilleur_score != float('inf') else 0

def simuler_calcul_ia(plateau, niveau):
    debut = time.time()
    phase = st.session_state.phase
    coups = generer_coups_possibles(plateau, phase, 2)
    
    if not coups: return None, 0
        
    meilleur_coup = coups[0]
    meilleur_score = -float('inf')
    
    # Augmentation de la profondeur à 4 pour anticiper plusieurs coups à l'avance
    profondeur = 4 if niveau == "Difficile" else 1
    
    for coup in coups:
        p_virtuel = copy.deepcopy(plateau)
        if phase == "Placement": p_virtuel[coup[0]][coup[1]] = 2
        else: p_virtuel[coup[0][0]][coup[0][1]], p_virtuel[coup[1][0]][coup[1][1]] = 0, 2
            
        score_coup = minimax(p_virtuel, profondeur, False, phase)
        
        # En mode défensif, si un coup empêche l'adversaire de gagner, son score restera haut
        if score_coup > meilleur_score:
            meilleur_score = score_coup
            meilleur_coup = coup
            
    fin = time.time()
    temps_ms = (fin - debut) * 1000
    
    # Application du mouvement de l'IA si phase de déplacement
    if phase == "Mouvement" and meilleur_coup:
        (oi, oj), (di, dj) = meilleur_coup
        st.session_state.plateau[oi][oj] = 0
        st.session_state.plateau[di][dj] = 2
        return (di, dj), temps_ms
        
    return meilleur_coup, temps_ms