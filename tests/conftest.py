# tests/conftest.py
import pytest
from unittest.mock import MagicMock, patch

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- MOCK Tkinter for headless CI environments (no DISPLAY) ---
@pytest.fixture(scope="function")
def mock_tkinter_for_ci(monkeypatch):
    """
    Automatically mock Tkinter root window and dialogs when running in CI (no GUI).
    This prevents TclError: no display name and no $DISPLAY environment variable.
    """

    try:
        import tkinter as tk
        # Try creating a real root — only works locally with a display
        root = tk.Tk()
        root.withdraw()
        root.destroy()
    except Exception:
        # In GitHub Actions or other headless environments: mock everything
        monkeypatch.setattr("tkinter.Tk", MagicMock(name="MockTk"))
        monkeypatch.setattr("tkinter.Toplevel", MagicMock(name="MockToplevel"))
        monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
        monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
        monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))
        monkeypatch.setattr("tkinter.simpledialog.askstring", MagicMock(return_value="mocked_input"))
        monkeypatch.setattr("tkinter.filedialog.askopenfilename", MagicMock(return_value="mocked_file.txt"))
