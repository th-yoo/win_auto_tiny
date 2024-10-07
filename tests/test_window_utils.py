import time
import pytest
import psutil
from win_auto_tiny.process import execute, kill
from win_auto_tiny.window_utils import find_windows

@pytest.fixture
def notepad():
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)

    # Check if the process is running
    assert any(proc.name() == app for proc in psutil.process_iter()), f"{app} did not start."
    
    yield
    
    # Ensure the process is killed
    kill(app)

    # Verify that the process has been terminated
    time.sleep(1)  # Allow some time for the process to be killed
    assert not any(proc.name() == app for proc in psutil.process_iter()), f"{app} did not terminate."

def test_window_utils(notepad):
    def match(hwnd, exe_path):
        return exe_path and exe_path.lower().endswith('notepad.exe')
    
    hwnds = find_windows(match)
    
    # Ensure that windows were found
    assert hwnds, "No Notepad windows were found."
    
    # Optional: Check specific properties of the found windows, if applicable
    # Example: assert len(hwnds) > 0  # Or any other specific assertions based on your needs
