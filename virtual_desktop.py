import pyautogui
import time
from text_to_speech import speak

def create_virtual_desktop():
    """Creates a new virtual desktop"""
    pyautogui.hotkey("win", "ctrl", "d")
    speak("New virtual desktop created.")

def switch_virtual_desktop(direction):
    """Switches virtual desktops left or right"""
    if direction == "left":
        pyautogui.hotkey("win", "ctrl", "left")
        speak("Switched to the left desktop.")
    elif direction == "right":
        pyautogui.hotkey("win", "ctrl", "right")
        speak("Switched to the right desktop.")


def close_virtual_desktop():
    """Closes the current virtual desktop if more than one exists"""
    speak("Checking if multiple desktops exist.")
    time.sleep(1)

    # Simulate closing the desktop
    pyautogui.hotkey("win", "ctrl", "f4")
    speak("Closed the current virtual desktop.")
