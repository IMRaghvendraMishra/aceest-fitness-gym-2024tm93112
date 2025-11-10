import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from app.ACEest_Fitness import FitnessTrackerApp  # rename file accordingly


class TestFitnessTrackerApp(unittest.TestCase):
    def setUp(self):
        # Create a root window (won’t actually display)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window for tests
        self.app = FitnessTrackerApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_with_empty_fields(self, mock_showerror):
        """Test that empty fields trigger an error message."""
        self.app.workout_entry.delete(0, tk.END)
        self.app.duration_entry.delete(0, tk.END)

        self.app.add_workout()

        mock_showerror.assert_called_once_with("Error", "Please enter both workout and duration.")
        self.assertEqual(len(self.app.workouts), 0)

    @patch("tkinter.messagebox.showerror")
    def test_add_workout_with_non_numeric_duration(self, mock_showerror):
        """Test that non-numeric duration shows an error."""
        self.app.workout_entry.insert(0, "Running")
        self.app.duration_entry.insert(0, "abc")

        self.app.add_workout()

        mock_showerror.assert_called_once_with("Error", "Duration must be a number.")
        self.assertEqual(len(self.app.workouts), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_add_workout_successfully(self, mock_showinfo):
        """Test successful workout addition."""
        self.app.workout_entry.insert(0, "Cycling")
        self.app.duration_entry.insert(0, "45")

        self.app.add_workout()

        mock_showinfo.assert_called_once_with("Success", "'Cycling' added successfully!")
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0], {"workout": "Cycling", "duration": 45})
        self.assertEqual(self.app.workout_entry.get(), "")
        self.assertEqual(self.app.duration_entry.get(), "")

    @patch("tkinter.messagebox.showinfo")
    def test_view_workouts_when_empty(self, mock_showinfo):
        """Test viewing workouts when list is empty."""
        self.app.workouts = []
        self.app.view_workouts()
        mock_showinfo.assert_called_once_with("Workouts", "No workouts logged yet.")

    @patch("tkinter.messagebox.showinfo")
    def test_view_workouts_with_entries(self, mock_showinfo):
        """Test viewing workouts with multiple entries."""
        self.app.workouts = [
            {"workout": "Running", "duration": 30},
            {"workout": "Yoga", "duration": 60},
        ]

        self.app.view_workouts()

        expected_text = (
            "Logged Workouts:\n"
            "1. Running - 30 minutes\n"
            "2. Yoga - 60 minutes\n"
        )
        mock_showinfo.assert_called_once_with("Workouts", expected_text)


if __name__ == "__main__":
    unittest.main()
