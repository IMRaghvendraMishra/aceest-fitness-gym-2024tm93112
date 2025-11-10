import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from fitness_app.versions.ACEest_Fitness_V1_2_1 import FitnessTrackerApp


@pytest.fixture
def fitness_app(monkeypatch):
    """Create a FitnessTrackerApp instance with mocked messageboxes."""
    root = tk.Tk()
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


def test_initial_state(fitness_app):
    assert isinstance(fitness_app.workouts, dict)
    assert all(k in fitness_app.workouts for k in ["Warm-up", "Workout", "Cool-down"])
    assert fitness_app.status_label.cget("text") == "Welcome! Log your first session."


def test_add_workout_success(fitness_app):
    fitness_app.category_var.set("Workout")
    fitness_app.workout_entry.insert(0, "Push-ups")
    fitness_app.duration_entry.insert(0, "15")

    with patch.object(fitness_app, "update_progress_charts") as mock_update:
        fitness_app.add_workout()

    workouts = fitness_app.workouts["Workout"]
    assert len(workouts) == 1
    assert workouts[0]["exercise"] == "Push-ups"
    assert workouts[0]["duration"] == 15
    assert "Push-ups" in fitness_app.status_label.cget("text")
    tk.messagebox.showinfo.assert_called_once()
    mock_update.assert_called_once()


def test_add_workout_missing_fields(fitness_app):
    fitness_app.category_var.set("Workout")
    fitness_app.workout_entry.delete(0, tk.END)
    fitness_app.duration_entry.delete(0, tk.END)

    fitness_app.add_workout()
    tk.messagebox.showerror.assert_called_once_with(
        "Input Error", "Please enter both exercise and duration."
    )
    assert all(len(v) == 0 for v in fitness_app.workouts.values())


def test_add_workout_invalid_duration(fitness_app):
    fitness_app.category_var.set("Warm-up")
    fitness_app.workout_entry.insert(0, "Jogging")
    fitness_app.duration_entry.insert(0, "abc")

    fitness_app.add_workout()
    tk.messagebox.showerror.assert_called_with("Input Error", "Duration must be a number.")
    assert len(fitness_app.workouts["Warm-up"]) == 0


def test_view_summary_no_data(fitness_app):
    fitness_app.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}
    fitness_app.view_summary()
    tk.messagebox.showinfo.assert_called_with("Summary", "No sessions logged yet!")


def test_view_summary_with_data(fitness_app):
    fitness_app.workouts["Workout"].append(
        {"exercise": "Squats", "duration": 20, "timestamp": "2025-11-10 10:00:00"}
    )
    with patch("tkinter.Toplevel") as mock_top:
        mock_window = MagicMock()
        mock_top.return_value = mock_window
        fitness_app.view_summary()
        mock_top.assert_called_once_with(fitness_app.master)
        assert mock_window.title.called
        assert mock_window.geometry.called


def test_update_progress_charts_creates_canvas(fitness_app):
    fitness_app.workouts["Workout"].append(
        {"exercise": "Push-ups", "duration": 10, "timestamp": "2025-11-10 10:00:00"}
    )
    fitness_app.update_progress_charts()

    assert fitness_app.progress_canvas is not None
    widget = fitness_app.progress_canvas.get_tk_widget()
    assert widget is not None
    assert str(widget) != ""   # Ensure widget has a valid Tk id


def test_update_progress_charts_handles_empty_data(fitness_app):
    for k in fitness_app.workouts.keys():
        fitness_app.workouts[k] = []
    fitness_app.update_progress_charts()
    assert fitness_app.progress_canvas is not None
