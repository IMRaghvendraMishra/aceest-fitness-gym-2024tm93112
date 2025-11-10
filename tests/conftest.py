# tests/conftest.py
import os
import sys
import pytest
import tkinter as tk
from unittest.mock import MagicMock

# --- Ensure the project root is importable ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ---------------------------------------------

@pytest.fixture
def fitness_app(monkeypatch):
    """Create a FitnessTrackerApp instance safely for both GUI and CI (headless)."""
    from fitness_app.ACEest_Fitness import FitnessTrackerApp

    # ✅ If no display (e.g., GitHub Actions), mock the entire Tk root
    if os.environ.get("DISPLAY", "") == "":
        root = MagicMock(name="MockTkRoot")
        # Also mock child widget methods often used in tests
        root.destroy = MagicMock()
    else:
        root = tk.Tk()
        root.withdraw()

    # Mock all tkinter popups to avoid UI calls
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.simpledialog.askstring", lambda *a, **k: "mock_input")

    app = FitnessTrackerApp(root)
    yield app

    # Safely destroy real Tk roots
    if hasattr(root, "destroy"):
        root.destroy()
