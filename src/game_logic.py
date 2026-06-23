import numpy as np

def initialiser_plateau():
    """ Crée une matrice NumPy 3x3 vide (remplie de 0) """
    return np.zeros((3, 3), dtype=int)

def verifier_alignement(plateau, joueur):
    """ Vérifie si un joueur a aligné 3 pions (Horizontal, Vertical, Diagonal) """
    arr = np.array(plateau)
    
    # Lignes & Colonnes
    if any(np.all(arr[i, :] == joueur) for i in range(3)): return True
    if any(np.all(arr[:, j] == joueur) for j in range(3)): return True
    # Diagonales
    if np.all(np.diag(arr) == joueur): return True
    if np.all(np.diag(np.fliplr(arr)) == joueur): return True
        
    return False

def est_mouvement_valide(de_i, de_j, vers_i, vers_j):
    """ 
    Vérifie le déplacement selon les lignes de designe.jpg :
    - Distance maximale de 1 case.
    - Interdiction des diagonales depuis les positions sans intersection diagonale croisée.
    """
    diff_i = abs(de_i - vers_i)
    diff_j = abs(de_j - vers_j)
    
    # 1. Vérification de la distance de base (Pas de saut, déplacement d'une seule case)
    if diff_i > 1 or diff_j > 1 or (de_i == vers_i and de_j == vers_j):
        return False
        
    # 2. Restriction des diagonales pour les positions orthogonales pures
    # Les positions (0,1), (1,0), (1,2) et (2,1) n'ont pas de lignes diagonales.
    positions_sans_diagonale = [(0, 1), (1, 0), (1, 2), (2, 1)]
    
    if diff_i == 1 and diff_j == 1:  # Tentative de mouvement en diagonale
        if (de_i, de_j) in positions_sans_diagonale or (vers_i, vers_j) in positions_sans_diagonale:
            return False
            
    return True