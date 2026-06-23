"""
INTERFACE UTILISATEUR - STREAMLIT
"""
import streamlit as st
import pandas as pd
import time
from src.components.fanorona_board import fanorona_board 
from src.game_logic import verifier_alignement, est_mouvement_valide, est_bloque
from src.ia_engine import simuler_calcul_ia

def render_interface():
    # Options propres et normalisées (sans émojis, sans espaces superflus)
    options_jeux = ["Humain vs Machine", "Humain vs Humain", "IA vs IA"]

    # En-tête de configuration
    st.markdown("""
        <div style="text-align:center; margin-bottom:5px;">
            <span style="color:#4a2e1b; font-weight:bold; font-size:13px; text-transform:uppercase; letter-spacing:1px;">
                Configuration de la confrontation
            </span>
        </div>
    """, unsafe_allow_html=True)

    col_menu, col_statut = st.columns([2, 1])
    
    with col_menu:
        # Correction du bug ValueError en utilisant la liste propre
        mode_choisi = st.selectbox(
            label="Mode de confrontation",
            options=options_jeux,
            index=options_jeux.index(st.session_state.mode_jeu),
            label_visibility="collapsed"
        )
        if mode_choisi != st.session_state.mode_jeu:
            st.session_state.mode_jeu = mode_choisi
            st.session_state.plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            st.session_state.phase = "Placement"
            st.session_state.tour = 1
            st.session_state.pions_places = 0
            st.session_state.pion_selectionne = None
            st.session_state.stats_perf = []
            st.rerun()

    with col_statut:
        if st.session_state.tour == 1:
            st.markdown('<div style="background-color:#404040; color:white; padding:8px; border-radius:8px; text-align:center; font-weight:bold; font-size:12px;">⚫ Tour : J1 (Noir)</div>', unsafe_allow_html=True)
        else:
            label_j2 = "Machine" if st.session_state.mode_jeu == "Humain vs Machine" else ("IA-2" if st.session_state.mode_jeu == "IA vs IA" else "⚪ J2 (Blanc)")
            st.markdown(f'<div style="background-color:#e0e0e0; color:#333; padding:8px; border-radius:8px; text-align:center; font-weight:bold; font-size:12px; border:1px solid #ccc;">⚪ Tour : {label_j2}</div>', unsafe_allow_html=True)

    # Zone de notification de statut (Phase ou Victoire)
    if st.session_state.gagnant:
        st.markdown(f"""
        <div style="background-color:#d4edda; border: 2px solid #c3e6cb; padding:10px; border-radius:10px; color:#155724; text-align:center; margin-top:8px; margin-bottom:15px; font-weight:bold;">
            🏆 FIN DE PARTIE : {st.session_state.gagnant} a gagné !
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#4a2e1b; padding:10px; border-radius:10px; color:white; text-align:center; margin-top:8px; margin-bottom:15px;">
            <h5 style="margin:0; font-family:sans-serif;">📋 Phase : {st.session_state.phase}</h5>
        </div>
        """, unsafe_allow_html=True)

    if "dernier_coup_traite" not in st.session_state:
        st.session_state.dernier_coup_traite = None

    # =================================================================
    # --- RENDU DE L'ARÈNE GRAPHIQUE (Toujours visible pour voir les coups)
    # =================================================================
    coup_joueur = fanorona_board(
        plateau=st.session_state.plateau,
        phase=st.session_state.phase,
        pion_selectionne=st.session_state.get("pion_selectionne"),
        key="fanoron_telo_canvas_grid"
    )

    # =================================================================
    # --- LOGIQUE DE TRAITEMENT AUTOMATIQUE DE L'IA (Modes Machine & IA vs IA)
    # =================================================================
    ia_doit_calculer = (st.session_state.mode_jeu == "Humain vs Machine" and st.session_state.tour == 2) or \
                       (st.session_state.mode_jeu == "IA vs IA")

    if ia_doit_calculer and not st.session_state.gagnant:
        role_ia = st.session_state.tour
        
        if st.session_state.phase == "Mouvement" and est_bloque(st.session_state.plateau, role_ia):
            if st.session_state.mode_jeu == "IA vs IA":
                st.session_state.gagnant = f"L'IA-{3-role_ia} (Blocage de l'IA-{role_ia})"
            else:
                st.session_state.gagnant = "Joueur 1 (Humain) par blocage"
            st.rerun()
            return

        with st.spinner(f"L'IA-{role_ia} calcule son coup..."):
            # Pause de 0.8s pour voir distinctement le mouvement sur le Canvas en IA vs IA
            time.sleep(0.8)
            
            coup, temps_ms = simuler_calcul_ia(st.session_state.plateau, "Difficile")
            
            if coup:
                if st.session_state.phase == "Placement":
                    st.session_state.plateau[coup[0]][coup[1]] = role_ia
                    st.session_state.pions_places += 1
                else:
                    if len(coup) == 4:
                        st.session_state.plateau[coup[0]][coup[1]] = 0
                        st.session_state.plateau[coup[2]][coup[3]] = role_ia
                    elif len(coup) == 2:
                        st.session_state.plateau[coup[0]][coup[1]] = role_ia

                # Sauvegarde du temps d'exécution
                st.session_state.stats_perf.append(temps_ms)

                if verifier_alignement(st.session_state.plateau, role_ia):
                    st.session_state.gagnant = f"L'IA-{role_ia}" if st.session_state.mode_jeu == "IA vs IA" else "L'IA (Machine)"
                else:
                    st.session_state.tour = 2 if role_ia == 1 else 1
                
                if st.session_state.pions_places >= 6:
                    st.session_state.phase = "Mouvement"
                
                st.rerun()
                return

    # =================================================================
    # --- LOGIQUE DE RECEPTION DU CLIC HUMAIN ------------------------
    # =================================================================
    if not st.session_state.gagnant and coup_joueur is not None and coup_joueur != st.session_state.dernier_coup_traite:
        st.session_state.dernier_coup_traite = coup_joueur
        i, j = coup_joueur['row'], coup_joueur['col']
        valeur_case = st.session_state.plateau[i][j]
        humain = st.session_state.tour

        if st.session_state.phase == "Mouvement" and est_bloque(st.session_state.plateau, humain):
            st.session_state.gagnant = f"Joueur {3 - humain}"
            st.rerun()
            return

        # Phase Placement
        if st.session_state.phase == "Placement" and valeur_case == 0:
            st.session_state.plateau[i][j] = humain
            st.session_state.pions_places += 1
            
            if verifier_alignement(st.session_state.plateau, humain):
                st.session_state.gagnant = f"Joueur {humain} (Humain)"
            else:
                st.session_state.tour = 2 if humain == 1 else 1
            
            if st.session_state.pions_places >= 6:
                st.session_state.phase = "Mouvement"
            st.rerun()
            return
            
        # Phase Mouvement
        elif st.session_state.phase == "Mouvement":
            selection = st.session_state.get("pion_selectionne")
            if valeur_case == humain:
                st.session_state.pion_selectionne = (i, j)
                st.rerun()
                return
            elif valeur_case == 0 and selection:
                oi, oj = selection
                if est_mouvement_valide(oi, oj, i, j):
                    st.session_state.plateau[oi][oj] = 0
                    st.session_state.plateau[i][j] = humain
                    st.session_state.pion_selectionne = None
                    
                    if verifier_alignement(st.session_state.plateau, humain):
                        st.session_state.gagnant = f"Joueur {humain} (Humain)"
                    else:
                        st.session_state.tour = 2 if humain == 1 else 1
                    st.rerun()
                    return

    # Bouton Recommencer (Toujours accessible en bas du plateau)
    if st.session_state.gagnant:
        st.balloons()
        if st.button("🔄 Lancer une nouvelle partie", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # =================================================================
    # --- SECTION DES MÉTRIQUES ET TEMPS D'EXÉCUTION (En bas du plateau)
    # =================================================================
    if st.session_state.stats_perf and st.session_state.mode_jeu != "Humain vs Humain":
        st.write("---")
        st.write("### 📊 Évaluation analytique des performances de l'IA")
        df = pd.DataFrame(st.session_state.stats_perf, columns=["Temps de reponse (ms)"])
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Dernier calcul", f"{st.session_state.stats_perf[-1]:.1f} ms")
        c2.metric("Temps moyen", f"{df['Temps de reponse (ms)'].mean():.1f} ms")
        c3.metric("Tours calculés", len(df))

        # Petit graphique d'évolution temporelle pour le rapport obligatoire
        st.line_chart(df, height=130)