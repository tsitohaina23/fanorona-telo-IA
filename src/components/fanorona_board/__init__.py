import os
import streamlit.components.v1 as components

# S'assurer que le chemin pointe exactement sur "fanorona_board"
_RELEASE_DIR = os.path.dirname(os.path.abspath(__file__))
_component_func = components.declare_component("fanorona_board", path=_RELEASE_DIR)

def fanorona_board(plateau, phase, pion_selectionne=None, key=None):
    """
    Appelle le plateau personnalisé avec le bon nom de dossier.
    """
    # Force l'envoi explicite des variables nommées
    component_value = _component_func(
        plateau=plateau,
        phase=phase,
        pion_selectionne=pion_selectionne,
        key=key,
        default=None
    )
    return component_value