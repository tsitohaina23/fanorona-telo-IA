import copy


def snapshot_state(state):
    return {
        "plateau": copy.deepcopy(state.get("plateau", [])),
        "phase": state.get("phase", "Placement"),
        "tour": state.get("tour", 1),
        "pions_places": state.get("pions_places", 0),
        "gagnant": state.get("gagnant", None),
        "pion_selectionne": copy.deepcopy(state.get("pion_selectionne", None)),
    }


def restore_state(state, snapshot):
    state["plateau"] = copy.deepcopy(snapshot["plateau"])
    state["phase"] = snapshot["phase"]
    state["tour"] = snapshot["tour"]
    state["pions_places"] = snapshot["pions_places"]
    state["gagnant"] = snapshot["gagnant"]
    state["pion_selectionne"] = copy.deepcopy(snapshot["pion_selectionne"])


def push_history(state, history, redo_stack):
    snapshot = snapshot_state(state)
    history.append(snapshot)
    redo_stack.clear()
    return snapshot


def undo_state(state, history, redo_stack):
    if not history:
        return False

    current_snapshot = snapshot_state(state)
    redo_stack.append(current_snapshot)
    previous_snapshot = history.pop()
    restore_state(state, previous_snapshot)
    return True


def redo_state(state, history, redo_stack):
    if not redo_stack:
        return False

    next_snapshot = redo_stack.pop()
    history.append(snapshot_state(state))
    restore_state(state, next_snapshot)
    return True
