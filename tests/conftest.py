# tests/conftest.py
"""
Common pytest configuration and fixtures for the ACEest Fitness project.

This configuration ensures:
1. Tkinter works safely in both local (GUI) and CI (headless) environments.
2. All versioned FitnessTrackerApp modules can be tested using one fixture.
3. Message boxes and UI interactions are fully mocked (no popups, no hangs).
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
    # Headless CI: use dummy replacements that won't trigger TclError
    class DummyTk:
        def withdraw(self): pass
        def destroy(self): pass
        def mainloop(self): pass
        def after(self, *a, **kw): pass
        def update(self): pass
        def title(self, *a, **kw): pass
        def geometry(self, *a, **kw): pass
        def __getattr__(self, name):  # Handle any other call gracefully
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
    Fixture to initialize a FitnessTrackerApp instance that works across
    all versioned modules (ACEest_Fitness, ACEest_Fitness_V1_x, etc.)

    It safely mocks Tkinter dialogs and Entry widgets so tests can run
    without a graphical display or user input.
    """

    # Step 1: Create a safe Tk root
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        root = tk.Tk()  # will be DummyTk in headless mode

    # Step 2: Auto-detect the correct ACEest_Fitness module version
    test_path = request.fspath.strpath
    module_name = "ACEest_Fitness"
    match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
    if match:
        version_module = match.group(0)
        if "versions" in test_path:
            module_name = f"versions.{version_module}"

    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    # Step 3: Mock messagebox dialogs (no popups during test)
    mock_info = MagicMock()
    mock_error = MagicMock()
    mock_yesno = MagicMock(return_value=True)

    monkeypatch.setattr("tkinter.messagebox.showinfo", mock_info)
    monkeypatch.setattr("tkinter.messagebox.showerror", mock_error)
    monkeypatch.setattr("tkinter.messagebox.askyesno", mock_yesno)

    # Step 4: Patch tk.Entry.get() to return realistic strings in CI
    # Prevents "<MagicMock>" appearing in success messages
    def fake_get(self):
        # Try to guess purpose based on instance name or string repr
        repr_lower = str(self).lower()
        if "workout" in repr_lower:
            return "Cycling"
        if "duration" in repr_lower:
            return "45"
        return ""

    monkeypatch.setattr("tkinter.Entry.get", fake_get)

    # Step 5: Create the app instance
    app = app_class(root)

    # Yield the app to tests
    yield app

    # Step 6: Cleanup after each test
    try:
        root.destroy()
    except Exception:
        pass
