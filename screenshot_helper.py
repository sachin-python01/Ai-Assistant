import pyautogui
import os
import time
import pygetwindow as gw


def take_screenshot(command):
    """
    Takes a screenshot and saves it with the given command as the filename.

    :param command: The voice command used to take the screenshot (used as filename).
    :return: Path of the saved screenshot.
    """
    # Create 'Screenshots' folder if it doesn't exist
    save_dir = "Screenshots"
    os.makedirs(save_dir, exist_ok=True)

    # Format filename from command (replace spaces with underscores)
    filename = command.replace(" ", "_") + ".png"
    filepath = os.path.join(save_dir, filename)

    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    return filepath


def take_active_window_screenshot(command):
    """
    Takes a screenshot of the currently active window and saves it using the command as filename.

    :param command: The voice command used to take the screenshot (used as filename).
    :return: Path of the saved screenshot.
    """
    save_dir = "Screenshots"
    os.makedirs(save_dir, exist_ok=True)

    filename = command.replace(" ", "_") + "_active.png"
    filepath = os.path.join(save_dir, filename)

    # Get active window
    active_window = gw.getActiveWindow()
    if active_window:
        bbox = (active_window.left, active_window.top, active_window.right, active_window.bottom)
        screenshot = pyautogui.screenshot(region=bbox)
        screenshot.save(filepath)
        return filepath
    else:
        return "No active window detected."

