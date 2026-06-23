"""
MOTEUR D'IA - FIX TIE-BREAKER POUR ÉVITER LES MOUVEMENTS RÉPÉTITIFS
"""
import time
import random
from src.game_logic import (
    conversion_plateau_vers_bitboards, verifier_alignement_bitboard, 
    ADJACENCES, idx_to_mat, mat_to_idx
)

def generer_coups_possibles(plateau, phase, joueur):
    coups = []
    if phase == "Placement":
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == 0: coups.append((i, j))
    else:
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == joueur:
                    idx_orig = mat_to_idx(i, j)
                    for idx_dest in ADJACENCES[idx_orig]:
                        ni, nj = idx_to_mat(idx_dest)
                        if plateau[ni][nj] == 0:
                            coups.append((i, j, ni, nj))
    return coups

def evaluer_plateau_classique(plateau, ami, ennemi):
    import src.game_logic as gl
    if gl.verifier_alignement(plateau, ami): return 100
    if gl.verifier_alignement(plateau, ennemi): return -100
    return 0

def minimax(plateau, phase, profondeur, est_max, pions_places, ami, ennemi):
    score = evaluer_plateau_classique(plateau, ami, ennemi)
    if score == 100 or score == -100 or profondeur == 0:
        return score

    joueur = ami if est_max else ennemi
    coups = generer_coups_possibles(plateau, phase, joueur)
    if not coups: return 0

    if est_max:
        meilleur = -1000
        for c in coups:
            if phase == "Placement":
                plateau[c[0]][c[1]] = ami
                nxt = "Mouvement" if pions_places + 1 >= 6 else "Placement"
                meilleur = max(meilleur, minimax(plateau, nxt, profondeur - 1, False, pions_places + 1, ami, ennemi))
                plateau[c[0]][c[1]] = 0
            else:
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = 0, ami
                meilleur = max(meilleur, minimax(plateau, "Mouvement", profondeur - 1, False, pions_places, ami, ennemi))
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = ami, 0
        return meilleur
    else:
        pire = 1000
        for c in coups:
            if phase == "Placement":
                plateau[c[0]][c[1]] = ennemi
                nxt = "Mouvement" if pions_places + 1 >= 6 else "Placement"
                pire = min(pire, minimax(plateau, nxt, profondeur - 1, True, pions_places + 1, ami, ennemi))
                plateau[c[0]][c[1]] = 0
            else:
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = 0, ennemi
                pire = min(pire, minimax(plateau, "Mouvement", profondeur - 1, True, pions_places, ami, ennemi))
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = ennemi, 0
        return pire

def alpha_beta_bitboard(b_ami, b_ennemi, phase, profondeur, alpha, beta, est_max, count_pions):
    if verifier_alignement_bitboard(b_ami): return 1000 + profondeur
    if verifier_alignement_bitboard(b_ennemi): return -1000 - profondeur
    if profondeur == 0:
        score = 0
        if (b_ami & (1 << 4)): score += 15
        if (b_ennemi & (1 << 4)): score -= 15
        return score

    occupé = b_ami | b_ennemi
    if phase == "Placement":
        if est_max:
            val = -10000
            for idx in range(9):
                if not (occupé & (1 << idx)):
                    val = max(val, alpha_beta_bitboard(b_ami | (1 << idx), b_ennemi, "Mouvement" if count_pions + 1 >= 6 else "Placement", profondeur - 1, alpha, beta, False, count_pions + 1))
                    alpha = max(alpha, val)
                    if beta <= alpha: break
            return val
        else:
            val = 10000
            for idx in range(9):
                if not (occupé & (1 << idx)):
                    val = min(val, alpha_beta_bitboard(b_ami, b_ennemi | (1 << idx), "Mouvement" if count_pions + 1 >= 6 else "Placement", profondeur - 1, alpha, beta, True, count_pions + 1))
                    beta = min(beta, val)
                    if beta <= alpha: break
            return val
    else:
        if est_max:
            val = -10000
            for src in range(9):
                if b_ami & (1 << src):
                    for dest in ADJACENCES[src]:
                        if not (occupé & (1 << dest)):
                            nb_ami = (b_ami & ~(1 << src)) | (1 << dest)
                            val = max(val, alpha_beta_bitboard(nb_ami, b_ennemi, "Mouvement", profondeur - 1, alpha, beta, False, count_pions))
                            alpha = max(alpha, val)
                            if beta <= alpha: break
            return val
        else:
            val = 10000
            for src in range(9):
                if b_ennemi & (1 << src):
                    for dest in ADJACENCES[src]:
                        if not (occupé & (1 << dest)):
                            nb_ennemi = (b_ennemi & ~(1 << src)) | (1 << dest)
                            val = min(val, alpha_beta_bitboard(b_ami, nb_ennemi, "Mouvement", profondeur - 1, alpha, beta, True, count_pions))
                            beta = min(beta, val)
                            if beta <= alpha: break
            return val

def simuler_calcul_ia(plateau, difficulte, role_ia=2):
    start_time = time.perf_counter()
    ami = role_ia
    ennemi = 1 if ami == 2 else 2
    
    pions_actuels = sum(1 for i in range(3) for j in range(3) if plateau[i][j] != 0)
    phase = "Placement" if pions_actuels < 6 else "Mouvement"
    
    coups = generer_coups_possibles(plateau, phase, joueur=ami)
    if not coups:
        return None, (time.perf_counter() - start_time) * 1000

    meilleurs_coups = []

    if difficulte == "Facile":
        meilleurs_coups = coups

    elif difficulte == "Moyenne":
        meilleur_score = -10000
        for c in coups:
            if phase == "Placement":
                plateau[c[0]][c[1]] = ami
                score = minimax(plateau, phase, 3, False, pions_actuels, ami, ennemi)
                plateau[c[0]][c[1]] = 0
            else:
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = 0, ami
                score = minimax(plateau, phase, 3, False, pions_actuels, ami, ennemi)
                plateau[c[0]][c[1]], plateau[c[2]][c[3]] = ami, 0
            
            if score > meilleur_score:
                meilleur_score = score
                meilleurs_coups = [c]
            elif score == meilleur_score:
                meilleurs_coups.append(c)

    else: # Difficile (Alpha-Beta avec brise-égalité)
        b1, b2 = conversion_plateau_vers_bitboards(plateau)
        b_ami = b1 if ami == 1 else b2
        b_ennemi = b2 if ami == 1 else b1
        
        meilleur_score = -100000
        for c in coups:
            if phase == "Placement":
                idx = mat_to_idx(c[0], c[1])
                score = alpha_beta_bitboard(b_ami | (1 << idx), b_ennemi, "Mouvement" if pions_actuels + 1 >= 6 else "Placement", 7, -100000, 100000, False, pions_actuels + 1)
            else:
                src = mat_to_idx(c[0], c[1])
                dest = mat_to_idx(c[2], c[3])
                nb_ami = (b_ami & ~(1 << src)) | (1 << dest)
                score = alpha_beta_bitboard(nb_ami, b_ennemi, "Mouvement", 7, -100000, 100000, False, pions_actuels)
            
            if score > meilleur_score:
                meilleur_score = score
                meilleurs_coups = [c]
            elif score == meilleur_score:
                meilleurs_coups.append(c)

    # FIX FIX : Choisit aléatoirement un coup parmi ceux ayant la même note maximale absolue
    # Cela évite que deux IA figent le jeu sur un seul chemin monotone répétitif
    coup_selectionne = random.choice(meilleurs_coups) if meilleurs_coups else random.choice(coups)

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return coup_selectionne, elapsed_ms