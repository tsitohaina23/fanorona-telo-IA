"""
ML ENGINE - ROTE LEARNING (Mémorisation d'états)
================================================
Principe :
  - On génère des parties complètes IA vs IA (Alpha-Beta vs Alpha-Beta)
  - Chaque état de plateau rencontré est converti en une clé unique (tuple 9 entiers)
  - On associe à cet état le coup joué ET le résultat final de la partie (victoire=1, défaite=-1, nul=0)
  - En jeu réel, avant de lancer Alpha-Beta, on consulte cette mémoire
  - Si l'état est connu ET que le coup mémorisé a mené à une victoire → on le joue directement
  - Sinon → fallback normal vers Alpha-Beta

Structure de la mémoire :
  memoire[cle_etat] = (coup, score_moyen)
  - cle_etat  : tuple de 9 entiers, ex: (1,0,2,0,1,0,0,2,0)
  - coup       : (i,j) en Placement ou (i,j,ni,nj) en Mouvement
  - score_moyen: moyenne des résultats des parties passant par cet état
"""

import random
from src.game_logic import (
    verifier_alignement,
    est_bloque,
    ADJACENCES,
    mat_to_idx,
    idx_to_mat,
    conversion_plateau_vers_bitboards,
    verifier_alignement_bitboard
)

# ─────────────────────────────────────────────
# MÉMOIRE GLOBALE (persiste pendant la session)
# ─────────────────────────────────────────────
# Format : { cle_etat: {"coup": ..., "score_total": float, "nb_parties": int} }
_memoire_rote: dict = {}

# Nombre de parties générées au démarrage
NB_PARTIES_ENTRAINEMENT = 200


# ─────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────

def plateau_vers_cle(plateau: list) -> tuple:
    """Convertit la matrice 3x3 en tuple de 9 entiers (clé hashable)."""
    return tuple(plateau[i][j] for i in range(3) for j in range(3))

def cle_vers_plateau(cle: tuple) -> list:
    """Reconstruit la matrice 3x3 depuis une clé tuple."""
    return [[cle[i * 3 + j] for j in range(3)] for i in range(3)]

def copier_plateau(plateau: list) -> list:
    return [row[:] for row in plateau]

def generer_coups(plateau: list, phase: str, joueur: int) -> list:
    """Génère tous les coups légaux pour un joueur donné."""
    coups = []
    if phase == "Placement":
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == 0:
                    coups.append((i, j))
    else:
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == joueur:
                    src = mat_to_idx(i, j)
                    for dest in ADJACENCES[src]:
                        ni, nj = idx_to_mat(dest)
                        if plateau[ni][nj] == 0:
                            coups.append((i, j, ni, nj))
    return coups

def appliquer_coup(plateau: list, coup: tuple, joueur: int, phase: str) -> list:
    """Retourne un NOUVEAU plateau après application du coup (non destructif)."""
    p = copier_plateau(plateau)
    if phase == "Placement":
        p[coup[0]][coup[1]] = joueur
    else:
        p[coup[0]][coup[1]] = 0
        p[coup[2]][coup[3]] = joueur
    return p


# ─────────────────────────────────────────────
# ALPHA-BETA LÉGER (pour générer les parties)
# ─────────────────────────────────────────────

def _alpha_beta_simple(plateau, phase, profondeur, alpha, beta, est_max, pions, ami, ennemi):
    """Version allégée d'Alpha-Beta utilisée UNIQUEMENT pour l'entraînement."""
    b1, b2 = conversion_plateau_vers_bitboards(plateau)
    b_ami    = b1 if ami == 1 else b2
    b_ennemi = b2 if ami == 1 else b1

    if verifier_alignement_bitboard(b_ami):   return  100
    if verifier_alignement_bitboard(b_ennemi): return -100
    if profondeur == 0:
        score = 0
        if b_ami   & (1 << 4): score += 5
        if b_ennemi & (1 << 4): score -= 5
        return score

    joueur = ami if est_max else ennemi
    coups  = generer_coups(plateau, phase, joueur)
    if not coups:
        return 0

    if est_max:
        val = -1000
        for c in coups:
            p2   = appliquer_coup(plateau, c, joueur, phase)
            pions2 = pions + (1 if phase == "Placement" else 0)
            phase2 = "Mouvement" if pions2 >= 6 else phase
            val = max(val, _alpha_beta_simple(p2, phase2, profondeur - 1, alpha, beta, False, pions2, ami, ennemi))
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return val
    else:
        val = 1000
        for c in coups:
            p2   = appliquer_coup(plateau, c, joueur, phase)
            pions2 = pions + (1 if phase == "Placement" else 0)
            phase2 = "Mouvement" if pions2 >= 6 else phase
            val = min(val, _alpha_beta_simple(p2, phase2, profondeur - 1, alpha, beta, True, pions2, ami, ennemi))
            beta = min(beta, val)
            if beta <= alpha:
                break
        return val


# ─────────────────────────────────────────────
# GÉNÉRATION DE PARTIES (ENTRAÎNEMENT)
# ─────────────────────────────────────────────

def _jouer_une_partie() -> list:
    """
    Simule une partie complète IA(1) vs IA(2) avec Alpha-Beta profondeur 4.
    Retourne la liste des (cle_etat, coup_joue, joueur_actif) de la partie.
    """
    plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    phase   = "Placement"
    pions   = 0
    tour    = 1   # joueur 1 commence
    historique = []  # (cle_etat, coup, joueur)

    for _ in range(50):  # max 50 demi-coups pour éviter les boucles infinies
        coups = generer_coups(plateau, phase, tour)
        if not coups:
            break

        # Chercher le meilleur coup par Alpha-Beta profondeur 4
        meilleurs, meilleur_score = [], -100000
        ami, ennemi = tour, (2 if tour == 1 else 1)

        for c in coups:
            p2     = appliquer_coup(plateau, c, tour, phase)
            pions2 = pions + (1 if phase == "Placement" else 0)
            phase2 = "Mouvement" if pions2 >= 6 else phase
            score  = _alpha_beta_simple(p2, phase2, 4, -100000, 100000, False, pions2, ami, ennemi)
            if score > meilleur_score:
                meilleur_score = score
                meilleurs = [c]
            elif score == meilleur_score:
                meilleurs.append(c)

        coup_choisi = random.choice(meilleurs)

        # Enregistrer l'état AVANT le coup
        historique.append((plateau_vers_cle(plateau), coup_choisi, tour))

        # Appliquer le coup
        plateau = appliquer_coup(plateau, coup_choisi, tour, phase)
        pions  += 1 if phase == "Placement" else 0
        if pions >= 6:
            phase = "Mouvement"

        # Vérifier victoire
        if verifier_alignement(plateau, tour):
            return historique, tour  # retourne aussi le gagnant

        # Alterner les tours
        tour = 2 if tour == 1 else 1

    return historique, 0  # match nul / bloqué


def entrainer(nb_parties: int = NB_PARTIES_ENTRAINEMENT):
    """
    Lance nb_parties simulations et remplit _memoire_rote.
    À appeler une seule fois au démarrage (via is_entraine()).
    """
    global _memoire_rote
    _memoire_rote = {}

    for _ in range(nb_parties):
        historique, gagnant = _jouer_une_partie()

        for (cle, coup, joueur) in historique:
            # Score du point de vue du joueur qui a joué ce coup
            if gagnant == 0:
                resultat = 0.0       # nul
            elif gagnant == joueur:
                resultat = 1.0       # victoire
            else:
                resultat = -1.0      # défaite

            if cle not in _memoire_rote:
                _memoire_rote[cle] = {"coup": coup, "score_total": resultat, "nb_parties": 1}
            else:
                entree = _memoire_rote[cle]
                entree["nb_parties"]  += 1
                entree["score_total"] += resultat
                # Mettre à jour le meilleur coup si le score moyen de ce nouveau coup est meilleur
                score_moyen_actuel = entree["score_total"] / entree["nb_parties"]
                if resultat > score_moyen_actuel:
                    entree["coup"] = coup


def is_entraine() -> bool:
    """Retourne True si l'entraînement a déjà été effectué."""
    return len(_memoire_rote) > 0

def taille_memoire() -> int:
    """Nombre d'états mémorisés."""
    return len(_memoire_rote)


# ─────────────────────────────────────────────
# CONSULTATION DE LA MÉMOIRE EN JEU
# ─────────────────────────────────────────────

def choisir_coup_ml(plateau: list, phase: str, joueur: int) -> tuple | None:
    """
    Consulte la mémoire Rote Learning.

    Retourne le coup mémorisé si :
      - l'état est connu
      - le score moyen mémorisé est positif (coup historiquement gagnant)
      - le coup est encore légal dans la configuration actuelle

    Sinon retourne None (→ fallback vers Alpha-Beta dans ia_engine).
    """
    if not is_entraine():
        return None

    cle = plateau_vers_cle(plateau)

    if cle not in _memoire_rote:
        return None

    entree       = _memoire_rote[cle]
    score_moyen  = entree["score_total"] / entree["nb_parties"]
    coup_memoise = entree["coup"]

    # N'utiliser la mémoire que si historiquement positif
    if score_moyen <= 0:
        return None

    # Vérifier que le coup est encore légal (plateau peut différer)
    coups_legaux = generer_coups(plateau, phase, joueur)
    if coup_memoise in coups_legaux:
        return coup_memoise

    return None
