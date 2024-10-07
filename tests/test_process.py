import time
import pytest
import psutil
from win_auto_tiny.process import execute, kill

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

def test_process(notepad):
    pass  # The fixture handles everything
