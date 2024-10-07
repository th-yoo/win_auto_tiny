import time
import pytest
import win32gui
import win32con
from win_auto_tiny.win32_draw import draw_point_on_window, RGB
from win_auto_tiny.process import execute, kill

@pytest.fixture
def notepad():
    app = 'notepad.exe'
    execute(app)
    time.sleep(1)  # Consider replacing with a polling mechanism if necessary
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

def get_pixel_color(hwnd, x, y):
    """Get the color of a pixel at the given coordinates."""
    hdc = win32gui.GetDC(hwnd)  # Get the device context
    pixel = win32gui.GetPixel(hdc, x, y)  # Get the pixel color
    win32gui.ReleaseDC(hwnd, hdc)  # Release the device context
    return pixel

def test_win32_draw(notepad):
    hwnd = wait_for_window("Untitled - Notepad")
    assert hwnd is not None, "Notepad window did not open."

    # Draw a red point at (100, 100)
    x, y = 100, 100
    expected_color = RGB(255, 0, 0)  # Red color in RGB format
    draw_point_on_window(hwnd, x, y, 4, expected_color)

    # Get the color of the pixel at (100, 100)
    pixel_color = get_pixel_color(hwnd, x, y)

    # Compare the color (GetPixel returns a COLORREF value, so we need to extract RGB components)
    red = pixel_color & 0xFF
    green = (pixel_color >> 8) & 0xFF
    blue = (pixel_color >> 16) & 0xFF

    assert (red, green, blue) == (255, 0, 0), f"Expected color (255, 0, 0), but got ({red}, {green}, {blue})."
