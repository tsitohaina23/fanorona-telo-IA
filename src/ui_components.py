import streamlit as st
import pandas as pd
# Importation propre depuis la nouvelle structure de dossier
from src.components.fanorona_board import fanorona_board 
from src.game_logic import verifier_alignement, est_mouvement_valide
from src.ia_engine import simuler_calcul_ia

def render_interface():
    if st.session_state.gagnant:
        st.balloons()
        st.success(f"🏆 {st.session_state.gagnant} a gagné !")
        if st.button("🔄 Recommencer la partie", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        return

    # En-tête informatif
    st.markdown(f"""
    <div style="background-color:#4a2e1b; padding:12px; border-radius:10px; color:white; text-align:center; margin-bottom:20px;">
        <h4 style="margin:0; font-family:sans-serif;">Phase actuelle : {st.session_state.phase}</h4>
    </div>
    """, unsafe_allow_html=True)

    # 🌟 APPEL DU COMPOSANT NATIF CUSTOM
    coup_joueur = fanorona_board(
        plateau=st.session_state.plateau,
        phase=st.session_state.phase,
        pion_selectionne=st.session_state.get("pion_selectionne"),
        key="fanoron_telo_canvas_grid"
    )

    # Si l'utilisateur clique, la valeur est transmise à l'instant ici
    if coup_joueur is not None and st.session_state.tour == 1:
        i, j = coup_joueur['row'], coup_joueur['col']
        valeur = st.session_state.plateau[i][j]

        # Logique : Phase de Placement
        if st.session_state.phase == "Placement" and valeur == 0:
            st.session_state.plateau[i][j] = 1
            st.session_state.pions_places += 1
            if verifier_alignement(st.session_state.plateau, 1):
                st.session_state.gagnant = "Joueur 1 (Humain)"
            else:
                st.session_state.tour = 2
            if st.session_state.pions_places >= 6:
                st.session_state.phase = "Mouvement"
            st.rerun()
            
        # Logique : Phase de Mouvement
        elif st.session_state.phase == "Mouvement":
            selection = st.session_state.get("pion_selectionne")
            if valeur == 1:
                st.session_state.pion_selectionne = (i, j)
                st.rerun()
            elif valeur == 0 and selection:
                oi, oj = selection
                if est_mouvement_valide(oi, oj, i, j):
                    st.session_state.plateau[oi][oj] = 0
                    st.session_state.plateau[i][j] = 1
                    st.session_state.pion_selectionne = None
                    if verifier_alignement(st.session_state.plateau, 1):
                        st.session_state.gagnant = "Joueur 1 (Humain)"
                    else:
                        st.session_state.tour = 2
                    st.rerun()

    # --- ACTION ET CALCUL DE L'IA ---
    if st.session_state.tour == 2 and not st.session_state.gagnant:
        with st.spinner("L'IA calcule son coup de blocage..."):
            coup, temps_ms = simuler_calcul_ia(st.session_state.plateau, "Difficile")
            if coup:
                if st.session_state.phase == "Placement":
                    st.session_state.plateau[coup[0]][coup[1]] = 2
                    st.session_state.pions_places += 1
                    if verifier_alignement(st.session_state.plateau, 2):
                        st.session_state.gagnant = "L'IA"
                    else:
                        st.session_state.tour = 1
                else:
                    if verifier_alignement(st.session_state.plateau, 2):
                        st.session_state.gagnant = "L'IA"
                    else:
                        st.session_state.tour = 1
                
                if st.session_state.pions_places >= 6:
                    st.session_state.phase = "Mouvement"
                st.session_state.stats_perf.append(temps_ms)
                st.rerun()

    # Section 6 du rapport : Métriques analytiques de performance
    if st.session_state.stats_perf:
        st.write("---")
        st.write("### 📊 Section 6 : Évaluation analytique de l'IA")
        df = pd.DataFrame(st.session_state.stats_perf, columns=["Temps de réponse (ms)"])
        c1, c2 = st.columns(2)
        c1.metric("Temps moyen de calcul", f"{df['Temps de réponse (ms)'].mean():.1f} ms")
        c2.metric("Total des tours simulés", len(df))