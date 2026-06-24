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
    if len(history) <= 1:
        return False

    current_snapshot = snapshot_state(state)
    redo_stack.append(current_snapshot)
    history.pop()
    restore_state(state, history[-1])
    return True


def redo_state(state, history, redo_stack):
    if not redo_stack:
        return False

    history.append(redo_stack.pop())
    restore_state(state, history[-1])
    return True
