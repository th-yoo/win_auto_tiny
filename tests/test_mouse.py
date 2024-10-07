import time
import threading
import pytest
import win32api
import win32gui
import win32con
from win_auto_tiny.mouse import lclick

@pytest.fixture
def message_box_thread():
    title = "Message Box Title"
    message = "This message box will close automatically after 3 seconds!"

    def show_msg():
        win32api.MessageBox(0, message, title, win32con.MB_OK | win32con.MB_ICONINFORMATION)

    thread = threading.Thread(target=show_msg)
    thread.start()
    
    # Poll for the message box to appear
    start_time = time.time()
    while time.time() - start_time < 5:  # Wait up to 5 seconds
        message_box_hwnd = win32gui.FindWindow(None, title)
        if message_box_hwnd:
            break
        time.sleep(0.1)  # Check every 100ms

    yield title, thread  # Yield title and thread

def test_mouse(message_box_thread):
    title, thread = message_box_thread  # Unpack title and thread
    
    # Find the message box window
    message_box_hwnd = win32gui.FindWindow(None, title)
    assert message_box_hwnd is not None, "Message box not found."
    
    # Find the OK button within the message box
    ok_button_hwnd = win32gui.FindWindowEx(message_box_hwnd, None, 'Button', None)
    assert ok_button_hwnd is not None, "OK button not found."

    # Click the OK button
    lclick(ok_button_hwnd)

    # Poll for the message box to close
    start_time = time.time()
    while time.time() - start_time < 5:  # Wait up to 5 seconds
        message_box_hwnd_after = win32gui.FindWindow(None, title)
        print(f'msg box {message_box_hwnd_after:08X}')
        if not message_box_hwnd_after:
            break
        time.sleep(.1)  # Check every 100ms

    assert not message_box_hwnd_after, "Message box was not closed after clicking OK."

    thread.join()
