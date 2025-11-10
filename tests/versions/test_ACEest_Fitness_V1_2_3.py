import pytest
import tkinter as tk
from unittest.mock import MagicMock

from fitness_app.versions.ACEest_Fitness_V1_2_3 import FitnessTrackerApp


# ---------- Fixtures ---------- #

@pytest.fixture
def app_instance(monkeypatch):
    """Create a headless FitnessTrackerApp instance with mocked messageboxes."""
    # Mock messagebox methods to avoid blocking dialogs during tests
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())

    # Initialize root without showing GUI
    root = tk.Tk()
    root.withdraw()
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


# ---------- Initialization & Structure ---------- #

def test_app_initialization(app_instance):
    app = app_instance
    assert isinstance(app.master, tk.Tk)
    assert "Workout" in app.workouts
    assert hasattr(app, "add_workout")
    assert hasattr(app, "view_summary")
    assert hasattr(app, "update_progress_charts")


def test_notebook_tabs_created(app_instance):
    tabs = [app_instance.notebook.tab(t, "text") for t in app_instance.notebook.tabs()]
    assert any("Log Workouts" in t for t in tabs)
    assert any("Workout Plan" in t for t in tabs)
    assert any("Diet Guide" in t for t in tabs)
    assert any("Progress Tracker" in t for t in tabs)


# ---------- Add Workout ---------- #

def test_add_workout_success(monkeypatch, app_instance):
    app = app_instance
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Push-ups")
    app.duration_entry.insert(0, "15")

    called = {}
    def fake_info(title, msg):
        called["msg"] = msg

    monkeypatch.setattr("tkinter.messagebox.showinfo", fake_info)

    app.add_workout()

    assert "added successfully" in called["msg"].lower()
    assert len(app.workouts["Workout"]) == 1
    assert "push-ups" in app.status_label.cget("text").lower()


def test_add_workout_missing_fields(monkeypatch, app_instance):
    app = app_instance
    called = {}
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: called.setdefault("msg", a[1]))

    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")
    app.add_workout()

    assert "enter both" in called["msg"].lower()


def test_add_workout_invalid_duration(monkeypatch, app_instance):
    app = app_instance
    called = {}
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: called.setdefault("msg", a[1]))

    app.workout_entry.insert(0, "Jogging")
    app.duration_entry.insert(0, "-5")
    app.add_workout()

    assert "positive" in called["msg"].lower()


# ---------- Summary View ---------- #

def test_view_summary_no_data(monkeypatch, app_instance):
    app = app_instance
    called = {}
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: called.setdefault("msg", a[1]))

    app.view_summary()
    assert "no sessions logged yet" in called["msg"].lower()


def test_view_summary_with_data(app_instance):
    app = app_instance
    app.workouts["Workout"].append({
        "exercise": "Squats",
        "duration": 20,
        "timestamp": "2025-11-10 10:00:00"
    })

    app.view_summary()

    # Ensure a new summary window (Toplevel) was created
    summary_windows = [w for w in app.master.winfo_children() if isinstance(w, tk.Toplevel)]
    assert len(summary_windows) == 1


# ---------- Charts / Progress ---------- #

def test_update_progress_charts_empty(app_instance):
    app = app_instance
    app.update_progress_charts()
    labels = [w for w in app.chart_container.winfo_children() if isinstance(w, tk.Label)]
    assert any("no workout data" in w.cget("text").lower() for w in labels)


def test_update_progress_charts_with_data(app_instance):
    app = app_instance
    app.workouts["Warm-up"].append({"exercise": "Jog", "duration": 10, "timestamp": "2025-11-10"})
    app.workouts["Workout"].append({"exercise": "Push-ups", "duration": 15, "timestamp": "2025-11-10"})
    app.workouts["Cool-down"].append({"exercise": "Stretching", "duration": 5, "timestamp": "2025-11-10"})

    app.update_progress_charts()
    assert app.chart_canvas is not None

    widget = app.chart_canvas.get_tk_widget()
    app.master.update_idletasks()
    assert widget.winfo_exists()


# ---------- Tab Change Event ---------- #

def test_on_tab_change_triggers_chart_update(monkeypatch, app_instance):
    app = app_instance
    called = {}
    monkeypatch.setattr(app, "update_progress_charts", lambda: called.setdefault("updated", True))

    app.notebook.select(app.progress_tab)
    app.on_tab_change(None)

    assert called.get("updated", False)


# ---------- UI Creation ---------- #

def test_create_workout_plan_tab_creates_labels(app_instance):
    labels = [w for w in app_instance.chart_tab.winfo_children() if isinstance(w, tk.Label)]
    assert any("workout plan" in w.cget("text").lower() for w in labels)


def test_create_diet_guide_tab_creates_labels(app_instance):
    labels = [w for w in app_instance.diet_tab.winfo_children() if isinstance(w, tk.Label)]
    assert any("nutritional" in w.cget("text").lower() for w in labels)
