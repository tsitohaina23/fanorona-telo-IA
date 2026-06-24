import unittest

from src.history import snapshot_state, undo_state, redo_state, push_history


class HistoryTests(unittest.TestCase):
    def test_undo_and_redo_restore_previous_state(self):
        state = {
            "plateau": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "phase": "Placement",
            "tour": 1,
            "pions_places": 0,
            "gagnant": None,
            "pion_selectionne": None,
        }

        history = []
        redo_stack = []

        history.append(snapshot_state(state))
        push_history(state, history, redo_stack)

        state["plateau"][0][0] = 1
        state["pions_places"] = 1
        state["tour"] = 2

        self.assertTrue(undo_state(state, history, redo_stack))
        self.assertEqual(state["plateau"][0][0], 0)
        self.assertEqual(state["pions_places"], 0)
        self.assertEqual(state["tour"], 1)

        self.assertTrue(redo_state(state, history, redo_stack))
        self.assertEqual(state["plateau"][0][0], 1)
        self.assertEqual(state["pions_places"], 1)
        self.assertEqual(state["tour"], 2)


if __name__ == "__main__":
    unittest.main()
