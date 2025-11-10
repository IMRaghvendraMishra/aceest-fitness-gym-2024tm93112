# tests/conftest.py
import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib
import re

# --- GLOBAL FIX ---
# Prevent TclError: no display name and no $DISPLAY environment variable
# by mocking tk.Tk() when no display is available.
try:
    _ = tk.Tk()
    _.withdraw()
    _.destroy()
except tk.TclError:
    class DummyTk:
        def withdraw(self): pass
        def destroy(self): pass
        def __getattr__(self, name): return MagicMock()
    tk.Tk = DummyTk  # ✅ Mock globally before any test imports run


@pytest.fixture
def fitness_app(monkeypatch, request):
    """
    Create a version-agnostic FitnessTrackerApp instance
    that runs safely in both GUI and headless (CI) environments.
    """

    # Step 1: Create root safely
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        root = tk.Tk()  # now always DummyTk in headless mode

    # Step 2: Auto-detect correct ACEest_Fitness version
    test_path = request.fspath.strpath
    module_name = "ACEest_Fitness"
    match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
    if match:
        version_module = match.group(0)
        if "versions" in test_path:
            module_name = f"versions.{version_module}"

    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    # Step 3: Mock dialogs
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))

    app = app_class(root)

    yield app

    try:
        root.destroy()
    except Exception:
        pass
