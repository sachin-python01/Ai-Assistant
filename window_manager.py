import pygetwindow as gw
import win32gui
import win32con
import win32process
import win32api
import time

def find_window(app_name):
    """Find the closest matching window title."""
    windows = gw.getAllTitles()
    for win in windows:
        if app_name.lower() in win.lower():
            return gw.getWindowsWithTitle(win)[0]
    return None

def minimize_window(app_name):
    window = find_window(app_name)
    if window:
        window.minimize()
        print(f"Minimized {window.title}")
    else:
        print(f"Could not find a window with '{app_name}'")

def maximize_window(app_name):
    window = find_window(app_name)
    if window:
        window.maximize()
        print(f"Maximized {window.title}")
    else:
        print(f"Could not find a window with '{app_name}'")


def switch_to_window(app_name):
    """Finds and switches to the given window, forcing it to the foreground."""
    window = None
    for win in gw.getAllTitles():
        if app_name.lower() in win.lower():
            window = gw.getWindowsWithTitle(win)[0]
            break

    if window:
        hwnd = window._hWnd  # Get window handle
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
        time.sleep(0.1)  # Small delay for stability

        # Corrected: GetCurrentThreadId is in win32api, not win32process
        foreground = win32gui.GetForegroundWindow()
        current_thread = win32api.GetCurrentThreadId()
        target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]

        win32gui.AttachThreadInput(current_thread, target_thread, True)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.AttachThreadInput(current_thread, target_thread, False)

        print(f"Switched to {window.title}")
    else:
        print(f"Could not find a window with '{app_name}'")




