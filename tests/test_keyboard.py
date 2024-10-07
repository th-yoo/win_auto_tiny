import time
import pytest
import win32gui
from win_auto_tiny.keyboard import (
    send_text,
    replace_text_in_edit_control,
    get_text_from_control,
)
from win_auto_tiny.process import execute, kill

@pytest.fixture
def notepad():
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)  # Wait for Notepad to launch
    yield app
    kill(app)

def wait_for_window(title, timeout=5):
    """Poll for a window to appear."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            return hwnd
        time.sleep(0.1)  # Check every 100ms
    return None

def test_replace_text_in_edit_control(notepad):
    hwnd = wait_for_window("Untitled - Notepad")
    assert hwnd is not None, "Notepad window did not open."

    edit = win32gui.FindWindowEx(hwnd, None, 'Edit', None)
    assert edit is not None, "Edit control not found."

    # Send initial text to Notepad
    initial_text = 'Hello World!'
    send_text(edit, initial_text)
    time.sleep(1)  # Allow time for text to be sent

    # Replace the text in the edit control
    new_text = 'Goodbye World!'
    replace_text_in_edit_control(edit, new_text)  # Assuming this function takes the new text as an argument

    # Retrieve the text from the edit control to verify replacement
    retrieved_text = get_text_from_control(edit)
    assert retrieved_text == new_text, f"Expected '{new_text}', but got '{retrieved_text}'."

