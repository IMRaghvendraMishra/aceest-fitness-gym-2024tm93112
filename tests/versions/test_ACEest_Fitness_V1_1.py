import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from datetime import datetime

# Import the class under test
from app.versions.ACEest_Fitness_V1_1 import FitnessTrackerApp

class TestFitnessTrackerAppV11(unittest.TestCase):
    def setUp(self):
        """Prepare a hidden root window before each test."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = FitnessTrackerApp(self.root)

    def tearDown(self):
        """Destroy the root window after each test."""
        try:
            self.root.destroy()
        except Exception:
            pass

    # --- ADD WORKOUT TESTS ---

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_with_empty_fields(self, mock_error):
        """Should show error when fields are empty."""
        self.app.workout_entry.delete(0, tk.END)
        self.app.duration_entry.delete(0, tk.END)

        self.app.add_workout()

        mock_error.assert_called_once_with("Input Error", "Please enter both exercise and duration.")
        for cat in self.app.workouts:
            self.assertEqual(len(self.app.workouts[cat]), 0)

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_with_invalid_duration(self, mock_error):
        """Should reject non-numeric duration."""
        self.app.workout_entry.insert(0, "Push Ups")
        self.app.duration_entry.insert(0, "ten")

        self.app.add_workout()

        mock_error.assert_called_once_with("Input Error", "Duration must be a number.")
        self.assertEqual(len(self.app.workouts["Workout"]), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_add_workout_success(self, mock_info):
        """Should add a valid workout successfully."""
        self.app.category_var.set("Warm-up")
        self.app.workout_entry.insert(0, "Jumping Jacks")
        self.app.duration_entry.insert(0, "15")

        self.app.add_workout()

        self.assertEqual(len(self.app.workouts["Warm-up"]), 1)
        entry = self.app.workouts["Warm-up"][0]
        self.assertEqual(entry["exercise"], "Jumping Jacks")
        self.assertEqual(entry["duration"], 15)
        self.assertIn("timestamp", entry)
        self.assertTrue(isinstance(datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S"), datetime))
        mock_info.assert_called_once()
        self.assertIn("Added Jumping Jacks", self.app.status_label.cget("text"))

    # --- VIEW SUMMARY TESTS ---

    @patch("tkinter.messagebox.showinfo")
    def test_view_summary_no_sessions(self, mock_info):
        """Should inform when no sessions exist."""
        self.app.view_summary()
        mock_info.assert_called_once_with("Summary", "No sessions logged yet!")

    @patch("tkinter.Toplevel")
    def test_view_summary_with_sessions(self, mock_top):
        """Should open summary window when sessions exist."""
        # Mock a fake toplevel window
        fake_window = MagicMock()
        mock_top.return_value = fake_window

        # Add some workouts
        self.app.workouts["Workout"].append({
            "exercise": "Squats",
            "duration": 20,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.app.workouts["Cool-down"].append({
            "exercise": "Stretching",
            "duration": 10,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.app.view_summary()

        mock_top.assert_called_once_with(self.app.master)
        # Confirm motivational message calculation via total time
        total_minutes = sum(e["duration"] for cat in self.app.workouts.values() for e in cat)
        self.assertEqual(total_minutes, 30)

    # --- GUI INITIALIZATION TESTS ---

    def test_initial_state(self):
        """Verify that widgets initialize correctly."""
        self.assertIn("Warm-up", self.app.workouts)
        self.assertEqual(self.app.category_var.get(), "Workout")
        self.assertEqual(self.app.status_label.cget("text"), "Welcome! Log your first session.")
        self.assertTrue(hasattr(self.app, "add_workout"))
        self.assertTrue(hasattr(self.app, "view_summary"))


if __name__ == "__main__":
    unittest.main()
