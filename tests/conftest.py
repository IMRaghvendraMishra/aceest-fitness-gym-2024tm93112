# tests/conftest.py
"""
Common pytest configuration and fixtures for the ACEest Fitness project.

This setup ensures:
1. Tkinter can run safely in both local (GUI) and CI (headless) environments.
2. A reusable fixture is available for creating version-specific
   FitnessTrackerApp instances without code duplication.
"""

import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib
import re


# ---------------------------------------------------------------------------
# GLOBAL FIX: make Tkinter safe for headless GitHub Actions or CI runs
# ---------------------------------------------------------------------------
try:
    # Local setup (macOS / Windows): create and hide a real Tk root
    root = tk.Tk()
    root.withdraw()
    tk._default_root = root
    root.destroy()
except tk.TclError:
    # CI (no display): replace Tk with a harmless mock implementation
    class DummyTk:
        def withdraw(self): pass
        def destroy(self): pass
        def mainloop(self): pass
        def after(self, *a, **kw): pass
        def update(self): pass
        def title(self, *a, **kw): pass
        def geometry(self, *a, **kw): pass
        def __getattr__(self, name):  # handle any other call gracefully
            return MagicMock()

    dummy_root = DummyTk()
    tk.Tk = lambda *a, **kw: dummy_root
    tk._default_root = dummy_root


# ---------------------------------------------------------------------------
# FIXTURE: create a version-agnostic FitnessTrackerApp instance
# ---------------------------------------------------------------------------
@pytest.fixture
def fitness_app(monkeypatch, request):
    """
    Fixture to initialize a FitnessTrackerApp instance that works
    across all versioned modules (ACEest_Fitness, ACEest_Fitness_V1_x, etc.)

    Automatically mocks messagebox dialogs so no popups appear during tests.
    """

    # Step 1: Create a safe Tk root
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        root = tk.Tk()  # will be DummyTk in headless mode

    # Step 2: Auto-detect the correct module version based on the test file
    test_path = request.fspath.strpath
    module_name = "ACEest_Fitness"
    match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
    if match:
        version_module = match.group(0)
        if "versions" in test_path:
            module_name = f"versions.{version_module}"

    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    # Step 3: Mock messagebox dialogs
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))

    # Step 4: Create the app instance
    app = app_class(root)

    yield app

    # Step 5: Cleanup after each test
    try:
        root.destroy()
    except Exception:
        pass
