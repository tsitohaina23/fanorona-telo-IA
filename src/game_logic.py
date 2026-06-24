"""
LOGIQUE DU JEU & INFRASTRUCTURE BITBOARD (NATIVE)
"""

# Représentation physique des lignes d'alignement sur 9 bits (indices de 0 à 8)
MASQUES_ALIGNEMENT = [
    0b000000111,  # Ligne Haute (0,1,2)
    0b000011100,  # Ligne Milieu (3,4,5)
    0b111000000,  # Ligne Basse (6,7,8)
    0b001001001,  # Colonne Gauche (0,3,6)
    0b010010010,  # Colonne Milieu (1,4,7)
    0b100100100,  # Colonne Droite (2,5,8)
    0b100010001,  # Diagonale Principale (0,4,8)
    0b001010100,  # Diagonale Secondaire (2,4,6)
]

# Graphe des connexions physiques du Fanorona-telo pour la phase de mouvement
ADJACENCES = {
    0: [1, 3, 4],       1: [0, 2, 4],       2: [1, 4, 5],
    3: [0, 4, 6],       4: [0, 1, 2, 3, 5, 6, 7, 8], # Le Centre connecte tout
    5: [2, 4, 8],       6: [3, 4, 7],       7: [6, 8, 4],       8: [4, 5, 7]
}

def mat_to_idx(i, j):
    return i * 3 + j

def idx_to_mat(idx):
    return idx // 3, idx % 3

def verifier_alignement(plateau, joueur):
    """Vérification classique par matrice pour l'interface."""
    for i in range(3):
        if plateau[i][0] == joueur and plateau[i][1] == joueur and plateau[i][2] == joueur: return True
    for j in range(3):
        if plateau[0][j] == joueur and plateau[1][j] == joueur and plateau[2][j] == joueur: return True
    if plateau[0][0] == joueur and plateau[1][1] == joueur and plateau[2][2] == joueur: return True
    if plateau[0][2] == joueur and plateau[1][1] == joueur and plateau[2][0] == joueur: return True
    return False

def est_mouvement_valide(oi, oj, ni, nj):
    """Vérifie l'adjacence stricte selon la grille topologique du Fanorona-telo."""
    orig = mat_to_idx(oi, oj)
    dest = mat_to_idx(ni, nj)
    return dest in ADJACENCES[orig]

def est_bloque(plateau, joueur):
    """Indique si un joueur ne peut plus bouger aucun de ses pions."""
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == joueur:
                idx_orig = mat_to_idx(i, j)
                for idx_dest in ADJACENCES[idx_orig]:
                    ni, nj = idx_to_mat(idx_dest)
                    if plateau[ni][nj] == 0:
                        return False
    return True

# --- FONCTIONS BITBOARD POUR LA SECTION 5 ---
def conversion_plateau_vers_bitboards(plateau):
    b1, b2 = 0, 0
    idx = 0
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == 1: b1 |= (1 << idx)
            elif plateau[i][j] == 2: b2 |= (1 << idx)
            idx += 1
    return b1, b2

def verifier_alignement_bitboard(b_joueur):
    for m in MASQUES_ALIGNEMENT:
        if (b_joueur & m) == m: return True
    return False