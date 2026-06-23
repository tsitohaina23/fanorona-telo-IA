import numpy as np

def initialiser_plateau():
    """
    Crée une matrice NumPy 3x3 remplie de 0 (cases vides).
    """
    return np.zeros((3, 3), dtype=int)

def verifier_alignement(plateau, joueur):
    """
    Vérifie si un joueur (1 ou 2) a aligné 3 pions (Horizontal, Vertical, Diagonal).
    Retourne True si gagné, False sinon.
    """
    arr = np.array(plateau)
    
    # 1. Vérification des lignes
    if any(np.all(arr[i, :] == joueur) for i in range(3)):
        return True
    # 2. Vérification des colonnes
    if any(np.all(arr[:, j] == joueur) for j in range(3)):
        return True
    # 3. Diagonale principale
    if np.all(np.diag(arr) == joueur):
        return True
    # 4. Diagonale secondaire
    if np.all(np.diag(np.fliplr(arr)) == joueur):
        return True
        
    return False

def est_mouvement_valide(de_i, de_j, vers_i, vers_j):
    """
    Vérifie si le déplacement se fait vers une case adjacente connectée (Règles Fanoron-telo).
    """
    # Distance maximale absolue de déplacement = 1 case
    diff_i = abs(de_i - vers_i)
    diff_j = abs(de_j - vers_j)
    
    # Vérification standard des lignes orthogonales/diagonales d'un plateau 3x3
    if diff_i <= 1 and diff_j <= 1 and (de_i != vers_i or de_j != vers_j):
        return True
    return False