import pytest
from unittest.mock import MagicMock, patch
from datetime import date
import tkinter as tk

from fitness_app.versions.ACEest_Fitness_V1_3 import FitnessTrackerApp


# ---------- Fixtures ---------- #

@pytest.fixture
def fitness_app_instance(monkeypatch):
    """Create a headless FitnessTrackerApp instance with mocked messageboxes."""
    # Mock messageboxes to prevent blocking dialogs
    monkeypatch.setattr(
        "fitness_app.versions.ACEest_Fitness_V1_3.messagebox.showinfo", MagicMock()
    )
    monkeypatch.setattr(
        "fitness_app.versions.ACEest_Fitness_V1_3.messagebox.showerror", MagicMock()
    )

    # Create Tk root headlessly
    root = tk.Tk()
    root.withdraw()
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


# ---------- User Info Tests ---------- #

def test_save_user_info_success(fitness_app_instance):
    app = fitness_app_instance
    app.name_entry.insert(0, "Alice")
    app.regn_entry.insert(0, "R001")
    app.age_entry.insert(0, "25")
    app.gender_entry.insert(0, "F")
    app.height_entry.insert(0, "165")
    app.weight_entry.insert(0, "60")

    app.save_user_info()

    assert app.user_info["name"] == "Alice"
    assert app.user_info["bmi"] == pytest.approx(60 / (1.65 ** 2))
    assert "bmr" in app.user_info
    assert app.user_info["bmr"] > 0
    assert app.user_info["weekly_cal_goal"] == 2000


def test_save_user_info_invalid_input(fitness_app_instance):
    app = fitness_app_instance
    app.name_entry.insert(0, "Bob")
    app.age_entry.insert(0, "not_a_number")

    app.save_user_info()

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showerror.assert_called_once()


# ---------- Add Workout Tests ---------- #

def test_add_workout_success(fitness_app_instance):
    app = fitness_app_instance
    app.user_info = {"weight": 70}
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Pushups")
    app.duration_entry.insert(0, "30")

    app.add_workout()

    today_iso = date.today().isoformat()
    assert today_iso in app.daily_workouts
    assert any(
        e["exercise"] == "Pushups"
        for e in app.daily_workouts[today_iso]["Workout"]
    )

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showinfo.assert_called()


def test_add_workout_missing_fields(fitness_app_instance):
    app = fitness_app_instance
    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")
    app.add_workout()

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showerror.assert_called_with(
        "Input Error", "Please enter both exercise and duration."
    )


def test_add_workout_invalid_duration(fitness_app_instance):
    app = fitness_app_instance
    app.workout_entry.insert(0, "Jogging")
    app.duration_entry.insert(0, "-5")
    app.add_workout()

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showerror.assert_called()


# ---------- Summary Tests ---------- #

def test_view_summary_no_sessions(fitness_app_instance):
    app = fitness_app_instance
    app.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}
    app.view_summary()

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showinfo.assert_called_with("Summary", "No sessions logged yet!")


# ---------- Chart Tests ---------- #

def test_update_progress_chart_no_data(fitness_app_instance):
    """Ensure placeholder label is displayed when no data available."""
    app = fitness_app_instance
    for cat in app.workouts:
        app.workouts[cat].clear()

    app.update_progress_charts()

    children = app.chart_container.winfo_children()
    labels = [c for c in children if isinstance(c, tk.Label)]
    assert labels, "No label widgets found"
    assert any("no workout data" in c.cget("text").lower() for c in labels)


@patch("fitness_app.versions.ACEest_Fitness_V1_3.FigureCanvasTkAgg", autospec=True)
def test_update_progress_chart_with_data(mock_canvas, fitness_app_instance):
    app = fitness_app_instance
    app.workouts["Workout"].append({"exercise": "Run", "duration": 20, "calories": 100})
    app.update_progress_charts()

    mock_canvas.assert_called()  # Chart creation was triggered


# ---------- PDF Export Tests ---------- #

@patch("fitness_app.versions.ACEest_Fitness_V1_3.pdf_canvas.Canvas", autospec=True)
def test_export_weekly_report_success(mock_canvas, fitness_app_instance):
    app = fitness_app_instance
    app.user_info = {
        "name": "TestUser",
        "regn_id": "R002",
        "age": 30,
        "gender": "M",
        "height": 180,
        "weight": 80,
        "bmi": 24.7,
        "bmr": 1700,
    }
    app.workouts["Workout"].append({
        "exercise": "Running",
        "duration": 30,
        "calories": 200,
        "timestamp": "2025-11-10 10:00:00",
    })

    mock_pdf = MagicMock()
    mock_canvas.return_value = mock_pdf

    app.export_weekly_report()

    mock_pdf.save.assert_called_once()
    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showinfo.assert_called()


def test_export_weekly_report_without_user(fitness_app_instance):
    app = fitness_app_instance
    app.user_info = {}
    app.export_weekly_report()

    mod = __import__("fitness_app.versions.ACEest_Fitness_V1_3", fromlist=["messagebox"])
    mod.messagebox.showerror.assert_called_with("Error", "Please save user info first!")
