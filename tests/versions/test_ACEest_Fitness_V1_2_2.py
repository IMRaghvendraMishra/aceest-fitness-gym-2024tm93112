import pytest
import tkinter as tk
from unittest.mock import MagicMock

from fitness_app.versions.ACEest_Fitness_V1_2_2 import FitnessTrackerApp


@pytest.fixture
def app_instance(monkeypatch):
    """Create a FitnessTrackerApp instance with mocked messageboxes to avoid GUI popups."""
    # Mock messagebox functions to prevent blocking dialogs
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())

    # Initialize Tkinter root without showing window
    root = tk.Tk()
    root.withdraw()
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


# --- Initialization & Structure ---

def test_app_initialization(app_instance):
    app = app_instance
    assert isinstance(app.master, tk.Tk)
    assert isinstance(app.notebook, tk.Widget)
    assert "Workout" in app.workouts
    assert hasattr(app, "create_log_tab")
    assert hasattr(app, "update_progress_charts")


def test_notebook_tabs_created(app_instance):
    tabs = [app_instance.notebook.tab(i, "text") for i in app_instance.notebook.tabs()]
    assert any("Log Workouts" in t for t in tabs)
    assert any("Workout Plan" in t for t in tabs)
    assert any("Diet Guide" in t for t in tabs)
    assert any("Progress Tracker" in t for t in tabs)


# --- Logging Workouts ---

def test_add_workout_valid(monkeypatch, app_instance):
    app = app_instance
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Push-ups")
    app.duration_entry.insert(0, "15")

    called = {}

    def fake_info(title, msg):
        called["msg"] = msg

    monkeypatch.setattr("tkinter.messagebox.showinfo", fake_info)

    app.add_workout()
    assert called["msg"].startswith("Push-ups added")
    assert len(app.workouts["Workout"]) == 1


def test_add_workout_invalid_duration(monkeypatch, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "Jogging")
    app.duration_entry.insert(0, "-5")

    called = {}
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda t, m: called.setdefault("err", m))

    app.add_workout()
    assert "Duration" in called["err"]


def test_add_workout_missing_input(monkeypatch, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")

    called = {}
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda t, m: called.setdefault("err", m))

    app.add_workout()
    assert "enter both" in called["err"].lower()


# --- Summary View ---

def test_view_summary_empty(monkeypatch, app_instance):
    called = {}
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda t, m: called.setdefault("msg", m))

    app_instance.view_summary()
    assert "no sessions" in called["msg"].lower()


def test_view_summary_with_data(app_instance):
    app = app_instance
    app.workouts["Workout"].append({
        "exercise": "Squats",
        "duration": 20,
        "timestamp": "2025-11-10 10:00:00"
    })
    app.view_summary()

    # Verify that a summary window (Toplevel) was created
    summary_windows = [w for w in app.master.winfo_children() if isinstance(w, tk.Toplevel)]
    assert len(summary_windows) == 1


# --- Charts / Progress ---

def test_update_progress_charts_no_data(app_instance):
    app = app_instance
    app.update_progress_charts()

    labels = [w for w in app.chart_container.winfo_children() if isinstance(w, tk.Label)]
    assert any("no workout data" in w.cget("text").lower() for w in labels)


def test_update_progress_charts_with_data(app_instance):
    app = app_instance
    app.workouts["Warm-up"].append({"exercise": "Jogging", "duration": 10, "timestamp": "2025-11-10 09:00"})
    app.workouts["Workout"].append({"exercise": "Push-ups", "duration": 20, "timestamp": "2025-11-10 09:10"})

    app.update_progress_charts()
    assert app.chart_canvas is not None
    widget = app.chart_canvas.get_tk_widget()
    assert isinstance(widget, tk.Widget)


# --- Tab Change Event ---

def test_on_tab_change_triggers_update(monkeypatch, app_instance):
    called = {}
    monkeypatch.setattr(app_instance, "update_progress_charts", lambda: called.setdefault("updated", True))

    app_instance.notebook.select(app_instance.progress_tab)
    app_instance.on_tab_change(None)
    assert called.get("updated", False)
