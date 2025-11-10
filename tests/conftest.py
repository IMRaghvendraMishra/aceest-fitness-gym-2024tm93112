# tests/conftest.py
import pytest
import tkinter as tk
import importlib

@pytest.fixture
def fitness_app(monkeypatch, request):
    """
    Create a FitnessTrackerApp instance for any ACEest_Fitness module version.
    Works in headless CI (no DISPLAY) and auto-imports correct module per test file.
    """

    # --- Step 1: Create safe Tk root (handles GitHub CI with no display)
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        class DummyTk:
            def withdraw(self): pass
            def destroy(self): pass
        root = DummyTk()

    # --- Step 2: Auto-detect correct ACEest_Fitness module from test path
    test_path = request.fspath.strpath  # e.g. "tests/versions/test_ACEest_Fitness_V1_2_3.py"
    module_name = "ACEest_Fitness"
    if "versions" in test_path:
        # Extract version part dynamically
        import re
        match = re.search(r"ACEest_Fitness(?:_V[\d_]+)?", test_path)
        if match:
            module_name = match.group(0)
        module_name = f"versions.{module_name}" if not module_name.startswith("ACEest_Fitness") else module_name

    # --- Step 3: Dynamically import correct version
    module = importlib.import_module(module_name)
    app_class = getattr(module, "FitnessTrackerApp")

    app = app_class(root)

    # --- Step 4: Mock messagebox dialogs for test automation
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **kw: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **kw: None)
    monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **kw: True)

    yield app

    # --- Step 5: Cleanup root (real or dummy)
    try:
        root.destroy()
    except Exception:
        pass
