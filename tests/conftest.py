# tests/conftest.py
import os
import pytest
import tkinter as tk
from unittest.mock import MagicMock

@pytest.fixture
def fitness_app(monkeypatch):
    """Create a FitnessTrackerApp instance safely for both GUI and CI (headless)."""
    from fitness_app.ACEest_Fitness import FitnessTrackerApp

    # Headless environment: simulate Tkinter root
    if os.environ.get("DISPLAY", "") == "":
        root = MagicMock(name="MockTkRoot")
    else:
        root = tk.Tk()

    # Mock common dialog functions so no popups appear
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.simpledialog.askstring", lambda *a, **k: "mock_input")

    app = FitnessTrackerApp(root)
    yield app

    # Cleanup (if real Tk)
    if hasattr(root, "destroy"):
        root.destroy()
