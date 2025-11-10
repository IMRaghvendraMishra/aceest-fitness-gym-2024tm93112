import pytest
import tkinter as tk
from unittest import mock
from fitness_app.versions.ACEest_Fitness_V1_2_1 import FitnessTrackerApp


@pytest.fixture
def app():
    """Fixture to initialize the FitnessTrackerApp with a hidden Tkinter root window."""
    root = tk.Tk()
    root.withdraw()  # Hide GUI during tests
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


def test_initial_setup(app):
    """Ensure app initializes with correct structure."""
    assert app.master.title() == "ACEest Fitness & Gym Tracker"
    assert isinstance(app.workouts, dict)
    assert set(app.workouts.keys()) == {"Warm-up", "Workout", "Cool-down"}
    assert app.status_label.cget("text") == "Welcome! Log your first session."


@mock.patch("fitness_tracker_app.messagebox.showerror")
def test_add_workout_missing_input(mock_showerror, app):
    """Check input validation when workout or duration is missing."""
    app.workout_entry.delete(0, tk.END)
    app.duration_entry.delete(0, tk.END)

    app.add_workout()

    mock_showerror.assert_called_once_with("Input Error", "Please enter both exercise and duration.")


@mock.patch("fitness_tracker_app.messagebox.showerror")
def test_add_workout_invalid_duration(mock_showerror, app):
    """Ensure invalid duration (non-numeric) triggers error."""
    app.workout_entry.insert(0, "Push-ups")
    app.duration_entry.insert(0, "ten")

    app.add_workout()

    mock_showerror.assert_called_once_with("Input Error", "Duration must be a number.")


@mock.patch("fitness_tracker_app.messagebox.showinfo")
def test_add_workout_success(mock_showinfo, app):
    """Test successful workout addition and chart refresh."""
    app.workout_entry.insert(0, "Push-ups")
    app.duration_entry.insert(0, "20")

    with mock.patch.object(app, "update_progress_charts") as mock_update_chart:
        app.add_workout()

    # Assertions
    assert len(app.workouts["Workout"]) == 1
    entry = app.workouts["Workout"][0]
    assert entry["exercise"] == "Push-ups"
    assert entry["duration"] == 20

    mock_showinfo.assert_called_once()
    mock_update_chart.assert_called_once()
    assert "Added Push-ups" in app.status_label.cget("text")


@mock.patch("fitness_tracker_app.messagebox.showinfo")
def test_view_summary_no_sessions(mock_showinfo, app):
    """Should show info message if no sessions logged."""
    app.view_summary()
    mock_showinfo.assert_called_once_with("Summary", "No sessions logged yet!")


def test_view_summary_with_sessions(app):
    """Ensure summary window is created with proper labels."""
    app.workouts["Workout"].append({
        "exercise": "Squats",
        "duration": 30,
        "timestamp": "2025-11-10 18:00:00"
    })

    with mock.patch("tkinter.Toplevel") as mock_top:
        mock_instance = mock.Mock()
        mock_top.return_value = mock_instance

        app.view_summary()

        mock_top.assert_called_once_with(app.master)
        mock_instance.title.assert_called_once_with("Workout Summary")
        mock_instance.geometry.assert_called_once_with("450x400")


def test_update_progress_charts(app):
    """Ensure chart update creates FigureCanvasTkAgg instance."""
    app.workouts["Workout"].append({
        "exercise": "Plank",
        "duration": 15,
        "timestamp": "2025-11-10 18:30:00"
    })

    with mock.patch("fitness_tracker_app.FigureCanvasTkAgg") as mock_canvas:
        mock_canvas.return_value = mock.Mock()
        app.update_progress_charts()
        mock_canvas.assert_called_once()
