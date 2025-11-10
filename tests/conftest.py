# tests/conftest.py
import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib
import re

# ============================================================
# ✅ GLOBAL FIX (final version)
# Prevent TclError, no-display crashes, StringVar errors,
# and infinite mainloop hangs in GitHub Actions (headless CI).
# ============================================================
try:
    real_root = tk.Tk()
    real_root.withdraw()
    tk._default_root = real_root
    real_root.destroy()
except tk.TclError:
    class DummyTk:
        def withdraw(self): pass
        def destroy(self): pass
        def mainloop(self): pass          # prevent blocking in CI
        def after(self, *a, **kw): pass   # prevent async loops
        def update(self): pass
        def title(self, *a, **kw): pass
        def geometry(self, *a, **kw): pass
        def __getattr__(self, name):
            return MagicMock()

    dummy_root = DummyTk()
    tk.Tk = lambda *a, **kw: dummy_root   # safely override Tk()
    tk._default_root = dummy_root         # required for StringVar, IntVar


# ====================================================================
# ✅ Your ORIGINAL FIXTURE (keep unchanged)
# ====================================================================
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
        root = tk.Tk()

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
