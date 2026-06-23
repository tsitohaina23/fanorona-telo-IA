import time
import random
import numpy as np

def simuler_calcul_ia(plateau, niveau):
    """
    Simule la prise de décision de l'IA et calcule précisément le temps d'exécution.
    Retourne : (meilleur_coup, temps_ms)
    """
    debut = time.time()
    
    # Trouver les cases vides disponibles sur la matrice
    cases_vides = []
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == 0:
                cases_vides.append((i, j))
                
    # --- ZONE DE TRAVAIL DE L'ÉQUIPE IA ---
    # TODO : Implémenter le Minimax simple et l'élagage Alpha-Beta selon le niveau
    # Pour l'instant, l'IA choisit un coup au hasard de manière sécurisée
    if cases_vides:
        coup_choisi = random.choice(cases_vides)
    else:
        coup_choisi = None
        
    # Simulation d'un léger délai de calcul algorithmique (ex: 30ms à 70ms)
    time.sleep(random.uniform(0.03, 0.07))
    # --------------------------------------
    
    fin = time.time()
    temps_ms = (fin - debut) * 1000 # Conversion en millisecondes
    
    return coup_choisi, temps_ms