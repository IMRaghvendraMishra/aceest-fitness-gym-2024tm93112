"""
Common pytest configuration and fixtures for the ACEest Fitness project.

This setup ensures:
1. Tkinter runs safely in both local (GUI) and CI (headless) environments.
2. FitnessTrackerApp can be instantiated in tests without GUI popups or crashes.
"""

import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib
import re


# ---------------------------------------------------------------------------
# GLOBAL FIX: make Tkinter safe for headless CI (e.g., GitHub Actions)
# ---------------------------------------------------------------------------
try:
    root = tk.Tk()
    root.withdraw()
    tk._default_root = root
    root.destroy()
except tk.TclError:
    class DummyTk:
        def withdraw(self): pass
        def destroy(self): pass
        def mainloop(self): pass
        def after(self, *a, **kw): pass
        def update(self): pass
        def title(self, *a, **kw): pass
        def geometry(self, *a, **kw): pass
        def __getattr__(self, name):
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
    across all module versions (ACEest_Fitness, ACEest_Fitness_V1_x, etc.).

    Automatically:
      - Mocks messagebox dialogs (no GUI popups)
      - Provides safe Tk root
      - Resolves correct module name based on test path
    """

    # Step 1: Safe Tk root
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        root = tk.Tk()

    # Step 2: Detect correct version of ACEest_Fitness module
    test_path = request.fspath.strpath
    module_name = "ACEest_Fitness"
    match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
    if match:
        version_module = match.group(0)
        if "versions" in test_path:
            module_name = f"versions.{version_module}"

    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    # Step 3: Mock messagebox dialogs (avoid real popups)
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))

    # Step 4: Initialize app
    app = app_class(root)

    # Step 5: Ensure Entry.get() behaves normally even if Entry is mocked
    for widget in ("entry_workout", "entry_duration"):
        if hasattr(app, widget):
            entry = getattr(app, widget)
            if isinstance(entry, MagicMock):
                # Ensure .get() returns "" by default (like a real empty Entry)
                entry.get = MagicMock(return_value="")

    yield app

    # Step 6: Cleanup
    try:
        root.destroy()
    except Exception:
        pass
