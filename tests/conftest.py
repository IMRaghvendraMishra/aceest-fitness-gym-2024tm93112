"""
Common pytest configuration and fixtures for the ACEest Fitness project.

Ensures:
1. Tkinter works safely in both local and CI environments.
2. No GUI popups interrupt tests.
3. FitnessTrackerApp can be loaded regardless of version folder structure.
"""

import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib
import re


# ---------------------------------------------------------------------------
# GLOBAL FIX: make Tkinter safe for headless CI (GitHub Actions, etc.)
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
# FIXTURE: version-safe FitnessTrackerApp instance
# ---------------------------------------------------------------------------
@pytest.fixture
def fitness_app(monkeypatch, request):
    """
    Creates a FitnessTrackerApp instance that works for any version (ACEest_Fitness, ACEest_Fitness_V1_x, etc.)
    and ensures no Tkinter or messagebox popups appear during CI.
    """

    # Step 1. Safe root
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        root = tk.Tk()  # DummyTk in headless mode

    # Step 2. Detect correct module (handles versioned dirs)
    test_path = request.fspath.strpath
    module_name = "ACEest_Fitness"
    match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
    if match:
        version_module = match.group(0)
        if "versions" in test_path:
            module_name = f"versions.{version_module}"

    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    # Step 3. Mock messagebox dialogs (prevent popups)
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))

    # Step 4. Create app instance
    app = app_class(root)

    # Step 5. Fix Entry widgets: ensure .get() always returns plain strings
    def make_safe_entry(entry_widget):
        """Ensure entry.get() always returns a string, never a MagicMock."""
        if hasattr(entry_widget, "get"):
            original_get = entry_widget.get
            if isinstance(original_get, MagicMock):
                entry_widget.get = lambda: ""
        else:
            # In case Tk is mocked, add a safe get() fallback
            entry_widget.get = lambda: ""

    for widget_name in ("entry_workout", "entry_duration"):
        if hasattr(app, widget_name):
            make_safe_entry(getattr(app, widget_name))

    yield app

    # Step 6. Cleanup
    try:
        root.destroy()
    except Exception:
        pass
