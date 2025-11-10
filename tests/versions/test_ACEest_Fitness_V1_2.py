import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from app.versions.ACEest_Fitness_V1_2 import FitnessTrackerApp


class TestFitnessTrackerAppV12(unittest.TestCase):

    def setUp(self):
        """Set up a mock Tkinter root for each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent window from showing during tests
        self.app = FitnessTrackerApp(self.root)

    def tearDown(self):
        """Destroy Tkinter root after each test."""
        self.root.destroy()

    def test_initialization_creates_tabs_and_workouts(self):
        """Ensure that all tabs and workout categories are initialized."""
        self.assertIn("Warm-up", self.app.workouts)
        self.assertIn("Workout", self.app.workouts)
        self.assertIn("Cool-down", self.app.workouts)
        self.assertIsNotNone(self.app.log_tab)
        self.assertIsNotNone(self.app.chart_tab)
        self.assertIsNotNone(self.app.diet_tab)

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_missing_fields(self, mock_showerror):
        """Should show error when fields are missing."""
        self.app.workout_entry.insert(0, "")
        self.app.duration_entry.insert(0, "")
        self.app.add_workout()
        mock_showerror.assert_called_once_with("Input Error", "Please enter both exercise and duration.")
        for category in self.app.workouts:
            self.assertEqual(len(self.app.workouts[category]), 0)

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_invalid_duration(self, mock_showerror):
        """Should show error if duration is not an integer."""
        self.app.workout_entry.insert(0, "Push-ups")
        self.app.duration_entry.insert(0, "abc")
        self.app.add_workout()
        mock_showerror.assert_called_once_with("Input Error", "Duration must be a number.")
        self.assertEqual(len(self.app.workouts["Workout"]), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_add_workout_successful(self, mock_showinfo):
        """Should add workout entry and clear inputs."""
        self.app.workout_entry.insert(0, "Push-ups")
        self.app.duration_entry.insert(0, "20")
        self.app.add_workout()
        self.assertEqual(len(self.app.workouts["Workout"]), 1)
        entry = self.app.workouts["Workout"][0]
        self.assertEqual(entry["exercise"], "Push-ups")
        self.assertEqual(entry["duration"], 20)
        mock_showinfo.assert_called_once()
        self.assertEqual(self.app.workout_entry.get(), "")
        self.assertEqual(self.app.duration_entry.get(), "")

    @patch("tkinter.messagebox.showinfo")
    def test_view_summary_no_sessions(self, mock_showinfo):
        """Should show messagebox if no sessions are logged."""
        for key in self.app.workouts:
            self.app.workouts[key] = []
        self.app.view_summary()
        mock_showinfo.assert_called_once_with("Summary", "No sessions logged yet!")

    @patch("tkinter.Toplevel")
    def test_view_summary_with_sessions(self, mock_toplevel):
        """Should open summary window and compute total time correctly."""
        # Mock Toplevel to avoid creating a real window
        summary_window = MagicMock()
        mock_toplevel.return_value = summary_window

        # Add sessions to multiple categories
        self.app.workouts["Workout"].append({"exercise": "Push-ups", "duration": 20, "timestamp": "2025-01-01"})
        self.app.workouts["Warm-up"].append({"exercise": "Jogging", "duration": 10, "timestamp": "2025-01-01"})

        self.app.view_summary()
        mock_toplevel.assert_called_once_with(self.root)
        # It should create labels and calculate total 30 minutes
        summary_window.title.assert_called_with("Workout Summary")
        self.assertEqual(sum(e["duration"] for e in self.app.workouts["Workout"] + self.app.workouts["Warm-up"]), 30)

    def test_workout_chart_tab_creation(self):
        """Ensure workout chart tab has correct labels."""
        labels = [child.cget("text") for child in self.app.chart_tab.winfo_children()]
        self.assertIn("🏋️ Personalized Workout Chart", labels)
        self.assertIn("Warm-up Exercises:", labels)
        self.assertIn("Workout Exercises:", labels)
        self.assertIn("Cool-down Exercises:", labels)

    def test_diet_chart_tab_creation(self):
        """Ensure diet chart tab has correct labels."""
        labels = [child.cget("text") for child in self.app.diet_tab.winfo_children()]
        self.assertIn("🥗 Best Diet Chart for Fitness Goals", labels)
        self.assertIn("Weight Loss Plan:", labels)
        self.assertIn("Muscle Gain Plan:", labels)
        self.assertIn("Endurance Plan:", labels)


if __name__ == "__main__":
    unittest.main()
