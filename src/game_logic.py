"""
MOTEUR DES RÈGLES DE JEU - FANORONA-TELO
Gère les contraintes géométriques du plateau 3x3, la détection des alignements
gagnants et les conditions de défaite par blocage total.
"""
import numpy as np

def initialiser_plateau():
    """
    Crée une matrice NumPy 3x3 vide remplie de 0.
    0 = Case vide, 1 = Pions du Joueur 1 (Noir), 2 = Pions du Joueur 2 / IA (Blanc)
    """
    return np.zeros((3, 3), dtype=int)


def verifier_alignement(plateau, joueur):
    """
    Vérifie si le joueur indiqué a aligné 3 pions sur une ligne physique du plateau.
    Lignes autorisées : 3 Horizontales, 3 Verticales, 2 Grandes Diagonales croisées au centre.
    """
    arr = np.array(plateau)
    
    # 1. Alignements horizontaux (Lignes 0, 1, 2)
    if any(np.all(arr[i, :] == joueur) for i in range(3)): 
        return True
        
    # 2. Alignements verticaux (Colonnes 0, 1, 2)
    if any(np.all(arr[:, j] == joueur) for j in range(3)): 
        return True
        
    # 3. Grande Diagonale principale : (0,0) -> (1,1) -> (2,2)
    if np.all(np.diag(arr) == joueur): 
        return True
        
    # 4. Grande Diagonale secondaire : (0,2) -> (1,1) -> (2,0)
    if np.all(np.diag(np.fliplr(arr)) == joueur): 
        return True
        
    return False


def est_mouvement_valide(de_i, de_j, vers_i, vers_j):
    """
    Vérifie la légalité d'un déplacement sur la grille géométrique :
    - Distance maximale d'une seule case (pas de saut).
    - Interdiction des diagonales depuis les milieux des bords (0,1), (1,0), (1,2), (2,1)
      car ces intersections n'ont pas de lignes diagonales tracées physiquement.
    """
    diff_i = abs(de_i - vers_i)
    diff_j = abs(de_j - vers_j)
    
    # Règle 1 : Distance de déplacement limitée à 1 case maximum (et interdiction du surplace)
    if diff_i > 1 or diff_j > 1 or (de_i == vers_i and de_j == vers_j):
        return False
        
    # Règle 2 : Restriction stricte des mouvements diagonaux
    # Les intersections centrales des bords n'ont pas de lignes diagonales reliées.
    positions_sans_diagonale = [(0, 1), (1, 0), (1, 2), (2, 1)]
    
    if diff_i == 1 and diff_j == 1:  # Tentative de déplacement en diagonale
        if (de_i, de_j) in positions_sans_diagonale or (vers_i, vers_j) in positions_sans_diagonale:
            return False
            
    return True


def est_bloque(plateau, joueur):
    """
    Analyse si le joueur est totalement immobilisé sur la grille.
    Parcourt ses pions et vérifie s'il existe au moins une case vide (0) adjacente et légale.
    """
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == joueur:
                # Analyse des 8 directions adjacentes autour du pion
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        # Rester dans les limites du plateau 3x3
                        if 0 <= ni < 3 and 0 <= nj < 3:
                            # S'il y a un emplacement vide et accessible selon le tracé
                            if plateau[ni][nj] == 0 and est_mouvement_valide(i, j, ni, nj):
                                return False  # Le joueur a au moins un coup jouable, il n'est pas bloqué
    return True  # Aucun coup possible pour l'ensemble de ses pions