import streamlit as st
import pandas as pd
from src.game_logic import verifier_alignement
from src.ia_engine import simuler_calcul_ia

def render_interface():
    # Affichage des informations d'état de la partie
    if st.session_state.gagnant:
        st.balloons()
        st.success(f"🏆 Victoire du {st.session_state.gagnant} !")
        if st.button("🔄 Recommencer une partie"):
            st.session_state.clear()
            st.rerun()
        return

    st.write(f"**Phase :** {st.session_state.phase} | **Tour :** {'Joueur 1 (❌)' if st.session_state.tour == 1 else 'IA (⭕)'}")

    # -------------------------------------------------------------------------
    # DESSIN DU PLATEAU DE JEU 3x3
    # -------------------------------------------------------------------------
    plateau = st.session_state.plateau
    
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            valeur = plateau[i][j]
            label = "⬜" if valeur == 0 else ("❌" if valeur == 1 else "⭕")
            
            # Action au clic sur une intersection
            if cols[j].button(label, key=f"cell_{i}_{j}", use_container_width=True):
                if st.session_state.tour == 1 and valeur == 0:  # Tour de l'humain
                    # Application de la règle selon la phase actuelle
                    if st.session_state.phase == "Placement":
                        st.session_state.plateau[i][j] = 1
                        st.session_state.pions_places += 1
                        
                        # Vérification immédiate de victoire en phase de placement
                        if verifier_alignement(st.session_state.plateau, 1):
                            st.session_state.gagnant = "Joueur 1 (❌)"
                        else:
                            # Changement de tour
                            st.session_state.tour = 2
                            
                        # Fin de la phase de placement après 6 pions posés au total
                        if st.session_state.pions_places >= 6:
                            st.session_state.phase = "Mouvement"
                            
                        st.rerun()

    # -------------------------------------------------------------------------
    # DÉCLENCHEMENT AUTOMATIQUE DE L'IA (SI C'EST SON TOUR)
    # -------------------------------------------------------------------------
    if st.session_state.tour == 2 and not st.session_state.gagnant:
        with st.spinner("L'IA réfléchit à son meilleur coup..."):
            coup, temps_ms = simuler_calcul_ia(st.session_state.plateau, "Difficile")
            
            if coup:
                i, j = coup
                st.session_state.plateau[i][j] = 2
                st.session_state.pions_places += 1
                st.session_state.stats_perf.append(temps_ms)
                
                # Vérification de victoire pour l'IA
                if verifier_alignement(st.session_state.plateau, 2):
                    st.session_state.gagnant = "Intelligence Artificielle (⭕)"
                else:
                    st.session_state.tour = 1
                    
                if st.session_state.pions_places >= 6:
                    st.session_state.phase = "Mouvement"
                    
                st.rerun()

    # -------------------------------------------------------------------------
    # COMPOSANT SECTION 6 : ANALYSES DE PERFORMANCES (PANDAS)
    # -------------------------------------------------------------------------
    if st.session_state.stats_perf:
        st.write("###  Section 6 : Métriques de l'IA")
        df = pd.DataFrame(st.session_state.stats_perf, columns=["Temps de réponse (ms)"])
        
        c1, c2 = st.columns(2)
        c1.metric("Temps Moyen de l'IA", f"{df['Temps de réponse (ms)'].mean():.1f} ms")
        c2.metric("Total Coups Joués", len(df))
        
        with st.expander("Voir le tableau des données brutes"):
            st.dataframe(df)