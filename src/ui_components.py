import streamlit as st
import pandas as pd
# Importation propre depuis la structure de dossier du projet
from src.components.fanorona_board import fanorona_board 
from src.game_logic import verifier_alignement, est_mouvement_valide
from src.ia_engine import simuler_calcul_ia

def render_interface():
    # 1. Gestion de la fin de partie (Gagnant trouvé)
    if st.session_state.gagnant:
        st.balloons()
        st.success(f"🏆 {st.session_state.gagnant} a gagné !")
        if st.button("🔄 Recommencer la partie", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        return

    # En-tête informatif de l'interface
    st.markdown(f"""
    <div style="background-color:#4a2e1b; padding:12px; border-radius:10px; color:white; text-align:center; margin-bottom:20px;">
        <h4 style="margin:0; font-family:sans-serif;">Phase actuelle : {st.session_state.phase}</h4>
    </div>
    """, unsafe_allow_html=True)

    # Initialisation du verrou de clic pour éviter les doubles traitements
    if "dernier_coup_traite" not in st.session_state:
        st.session_state.dernier_coup_traite = None


    # =================================================================
    # --- PHASE 1 : SÉCURITÉ & LOGIQUE DU TOUR DE L'IA (Tour == 2) ---
    # =================================================================
    if st.session_state.tour == 2 and not st.session_state.gagnant:
        with st.spinner("L'IA calcule son coup..."):
            coup, temps_ms = simuler_calcul_ia(st.session_state.plateau, "Difficile")
            if coup:
                if st.session_state.phase == "Placement":
                    st.session_state.plateau[coup[0]][coup[1]] = 2
                    st.session_state.pions_places += 1
                else:
                    # Phase de Mouvement pour l'IA
                    # Si votre ia_engine retourne (old_i, old_j, new_i, new_j)
                    if len(coup) == 4: 
                        st.session_state.plateau[coup[0]][coup[1]] = 0
                        st.session_state.plateau[coup[2]][coup[3]] = 2
                    # Si votre ia_engine retourne uniquement la destination (new_i, new_j)
                    elif len(coup) == 2:
                        st.session_state.plateau[coup[0]][coup[1]] = 2

                # Vérification si l'IA s'est alignée
                if verifier_alignement(st.session_state.plateau, 2):
                    st.session_state.gagnant = "L'IA"
                else:
                    st.session_state.tour = 1 # Redonner la main à l'humain
                
                # Transition de phase automatique
                if st.session_state.pions_places >= 6:
                    st.session_state.phase = "Mouvement"
                
                # Sauvegarde des métriques et relance propre du script
                st.session_state.stats_perf.append(temps_ms)
                st.rerun()
                return # Crucial : on arrête immédiatement la fonction ici pour éviter le doublon de clé


    # =================================================================
    # --- PHASE 2 : RENDU DU COMPOSANT & TOUR DU JOUEUR (Tour == 1) ---
    # =================================================================
    # Le plateau ne s'affiche et ne s'instancie que si c'est au tour du joueur humain
    coup_joueur = fanorona_board(
        plateau=st.session_state.plateau,
        phase=st.session_state.phase,
        pion_selectionne=st.session_state.get("pion_selectionne"),
        key="fanoron_telo_canvas_grid"
    )

    # Détection et traitement du clic de l'utilisateur
    if coup_joueur is not None and st.session_state.tour == 1 and coup_joueur != st.session_state.dernier_coup_traite:
        st.session_state.dernier_coup_traite = coup_joueur # Verrouiller le coup actuel
        i, j = coup_joueur['row'], coup_joueur['col']
        valeur = st.session_state.plateau[i][j]

        # Logique Joueur : Phase de Placement
        if st.session_state.phase == "Placement" and valeur == 0:
            st.session_state.plateau[i][j] = 1
            st.session_state.pions_places += 1
            if verifier_alignement(st.session_state.plateau, 1):
                st.session_state.gagnant = "Joueur 1 (Humain)"
            else:
                st.session_state.tour = 2 # Passer le tour à l'IA
            
            if st.session_state.pions_places >= 6:
                st.session_state.phase = "Mouvement"
                
            st.rerun()
            return # Bloque le reste de l'exécution
            
        # Logique Joueur : Phase de Mouvement
        elif st.session_state.phase == "Mouvement":
            selection = st.session_state.get("pion_selectionne")
            
            # Action A : Sélectionner son propre pion (valeur == 1)
            if valeur == 1:
                st.session_state.pion_selectionne = (i, j)
                st.rerun()
                return # Bloque le reste de l'exécution
                
            # Action B : Cliquer sur une case vide (valeur == 0) avec un pion déjà sélectionné
            elif valeur == 0 and selection:
                oi, oj = selection
                if est_mouvement_valide(oi, oj, i, j):
                    st.session_state.plateau[oi][oj] = 0 # Libère l'ancienne case
                    st.session_state.plateau[i][j] = 1  # Prend la nouvelle case
                    st.session_state.pion_selectionne = None # Réinitialise la sélection
                    
                    if verifier_alignement(st.session_state.plateau, 1):
                        st.session_state.gagnant = "Joueur 1 (Humain)"
                    else:
                        st.session_state.tour = 2 # Donner le tour à l'IA
                        
                    st.rerun()
                    return # Bloque le reste de l'exécution


    # =================================================================
    # --- PHASE 3 : SECTION ANALYTIQUE DE PERFORMANCE (RAPPORT) ------
    # =================================================================
    if st.session_state.stats_perf:
        st.write("---")
        st.write("### 📊 Section 6 : Évaluation analytique de l'IA")
        df = pd.DataFrame(st.session_state.stats_perf, columns=["Temps de réponse (ms)"])
        c1, c2 = st.columns(2)
        c1.metric("Temps moyen de calcul", f"{df['Temps de réponse (ms)'].mean():.1f} ms")
        c2.metric("Total des tours simulés", len(df))