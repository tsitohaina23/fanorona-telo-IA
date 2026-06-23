"""
INTERFACE DES MODULES GRAPHIQUES STREAMLIT - FIX BOUCLE INFINIE IA VS IA
"""
import streamlit as st
import pandas as pd
import time
from src.components.fanorona_board import fanorona_board 
from src.game_logic import verifier_alignement, est_mouvement_valide, est_bloque
from src.ia_engine import simuler_calcul_ia

def render_interface():
    options_jeux = ["Humain vs Machine", "Humain vs Humain", "IA vs IA"]
    options_diff = ["Facile", "Moyenne", "Difficile"]

    # --- BARRE CONFIGURATION ---
    st.markdown("""
        <div style="text-align:center; margin-bottom:5px;">
            <span style="color:#4a2e1b; font-weight:bold; font-size:12px; text-transform:uppercase; letter-spacing:1px;">
                ⚙️ CORE ENGINE CONFIGURATION (ISPM HACKATHON)
            </span>
        </div>
    """, unsafe_allow_html=True)

    c_mode, c_diff, c_tour = st.columns([2, 1, 1])
    
    with c_mode:
        mode_choisi = st.selectbox(
            "Mode", options=options_jeux, 
            index=options_jeux.index(st.session_state.mode_jeu), label_visibility="collapsed"
        )
        if mode_choisi != st.session_state.mode_jeu:
            st.session_state.mode_jeu = mode_choisi
            st.session_state.plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            st.session_state.phase = "Placement"
            st.session_state.tour = 1
            st.session_state.pions_places = 0
            st.session_state.gagnant = None
            st.session_state.pion_selectionne = None
            st.session_state.stats_perf = []
            st.rerun()

    with c_diff:
        desactive = (st.session_state.mode_jeu == "Humain vs Humain")
        diff_choisie = st.selectbox(
            "Niveau", options=options_diff,
            index=options_diff.index(st.session_state.difficulte_ia),
            disabled=desactive, label_visibility="collapsed"
        )
        if diff_choisie != st.session_state.difficulte_ia:
            st.session_state.difficulte_ia = diff_choisie

    with c_tour:
        if st.session_state.tour == 1:
            st.markdown('<div style="background-color:#404040; color:white; padding:8px; border-radius:8px; text-align:center; font-weight:bold; font-size:12px;">⚫ J1 (Noir)</div>', unsafe_allow_html=True)
        else:
            lbl = "Machine" if st.session_state.mode_jeu == "Humain vs Machine" else ("IA-2" if st.session_state.mode_jeu == "IA vs IA" else "⚪ J2")
            st.markdown(f'<div style="background-color:#e0e0e0; color:#333; padding:8px; border-radius:8px; text-align:center; font-weight:bold; font-size:12px; border:1px solid #ccc;">⚪ {lbl}</div>', unsafe_allow_html=True)

    # --- STATUS BANNER ---
    if st.session_state.gagnant:
        st.markdown(f"""
        <div style="background-color:#d4edda; border: 2px solid #c3e6cb; padding:12px; border-radius:10px; color:#155724; text-align:center; margin-top:10px; margin-bottom:15px; font-weight:bold; font-size:16px;">
            🏆 FIN DE PARTIE : {st.session_state.gagnant} a gagné !
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#4a2e1b; padding:10px; border-radius:10px; color:white; text-align:center; margin-top:10px; margin-bottom:15px;">
            <h5 style="margin:0; font-family:sans-serif;">Phase de Jeu Actuelle : {st.session_state.phase}</h5>
        </div>
        """, unsafe_allow_html=True)

    if "dernier_coup_traite" not in st.session_state:
        st.session_state.dernier_coup_traite = None

    # RENDU DU CANVAS GRAPHIC
    coup_joueur = fanorona_board(
        plateau=st.session_state.plateau,
        phase=st.session_state.phase,
        pion_selectionne=st.session_state.get("pion_selectionne"),
        key="fanoron_telo_canvas_grid"
    )

    # --- LOGIQUE D'AUTOMATION DES TOURS POUR L'IA (FIX BOUCLE INFINIE) ---
    ia_doit_calculer = (st.session_state.mode_jeu == "Humain vs Machine" and st.session_state.tour == 2) or \
                       (st.session_state.mode_jeu == "IA vs IA")

    if ia_doit_calculer and not st.session_state.gagnant:
        role_ia = st.session_state.tour
        
        if st.session_state.phase == "Mouvement" and est_bloque(st.session_state.plateau, role_ia):
            st.session_state.gagnant = f"IA-{'2' if role_ia == 1 else '1'} (Par blocage total)"
            st.rerun()
            return

        with st.spinner(f"Calcul de l'IA-{role_ia} ({st.session_state.difficulte_ia})..."):
            # Temporisation physique pour éviter la saturation CPU et laisser l'interface souffler
            time.sleep(0.5)
            
            coup, temps_ms = simuler_calcul_ia(st.session_state.plateau, st.session_state.difficulte_ia, role_ia)
            
            if coup:
                if st.session_state.phase == "Placement":
                    st.session_state.plateau[coup[0]][coup[1]] = role_ia
                    st.session_state.pions_places += 1
                else:
                    if len(coup) == 4:
                        st.session_state.plateau[coup[0]][coup[1]] = 0
                        st.session_state.plateau[coup[2]][coup[3]] = role_ia

                st.session_state.stats_perf.append(temps_ms)

                # Annuler explicitement toute sélection humaine parasite en cours pour éviter les collisions
                st.session_state.pion_selectionne = None
                st.session_state.dernier_coup_traite = None 

                if verifier_alignement(st.session_state.plateau, role_ia):
                    if st.session_state.mode_jeu == "IA vs IA":
                        st.session_state.gagnant = f"L'IA-{role_ia} ({'Noir' if role_ia == 1 else 'Blanc'})"
                    else:
                        st.session_state.gagnant = "L'IA (Machine)"
                else:
                    # Alternance stricte
                    st.session_state.tour = 2 if role_ia == 1 else 1
                
                if st.session_state.pions_places >= 6:
                    st.session_state.phase = "Mouvement"
                    
                st.rerun()
                return

    # --- CAPTURE DES CLICS HUMAINS ---
    if not st.session_state.gagnant and coup_joueur is not None and coup_joueur != st.session_state.dernier_coup_traite:
        st.session_state.dernier_coup_traite = coup_joueur
        i, j = coup_joueur['row'], coup_joueur['col']
        valeur_case = st.session_state.plateau[i][j]
        humain = st.session_state.tour

        if st.session_state.phase == "Placement" and valeur_case == 0:
            st.session_state.plateau[i][j] = humain
            st.session_state.pions_places += 1
            if verifier_alignement(st.session_state.plateau, humain):
                st.session_state.gagnant = f"Joueur {humain}"
            else:
                st.session_state.tour = 2 if humain == 1 else 1
            if st.session_state.pions_places >= 6:
                st.session_state.phase = "Mouvement"
            st.rerun()
            return
            
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
                        st.session_state.gagnant = f"Joueur {humain}"
                    else:
                        st.session_state.tour = 2 if humain == 1 else 1
                    st.rerun()
                    return

    if st.session_state.gagnant:
        st.balloons()
        if st.button("🔄 Lancer un nouveau match", use_container_width=True):
            m, d = st.session_state.mode_jeu, st.session_state.difficulte_ia
            st.session_state.clear()
            st.session_state.mode_jeu = m
            st.session_state.difficulte_ia = d
            st.session_state.plateau = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            st.session_state.phase = "Placement"
            st.session_state.tour = 1
            st.session_state.pions_places = 0
            st.session_state.stats_perf = []
            st.rerun()

    if st.session_state.stats_perf and st.session_state.mode_jeu != "Humain vs Humain":
        st.write("---")
        st.write("### 📊 Section 6 : Évaluation analytique de l'IA")
        df = pd.DataFrame(st.session_state.stats_perf, columns=["Temps"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Dernier calcul", f"{st.session_state.stats_perf[-1]:.2f} ms")
        c2.metric("Vitesse moyenne", f"{df['Temps'].mean():.2f} ms")
        c3.metric("Tours simulés", len(df))
        st.line_chart(df, height=130)