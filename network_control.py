import os
import time
import pyautogui
from text_to_speech import speak


def open_bluetooth_settings():
    """Opens the Bluetooth settings window"""
    os.system("start ms-settings:bluetooth")
    time.sleep(2)  # Wait for settings to open


def toggle_bluetooth():
    """Toggles Bluetooth on/off using keyboard navigation."""
    speak("Opening Bluetooth settings.")
    open_bluetooth_settings()

    # Bring the window to focus and maximize it
    pyautogui.hotkey("win", "up")  # Maximize window
    time.sleep(1)

    # Navigate using keyboard
    pyautogui.press("tab", presses=1, interval=0.2)  # Move to toggle
    pyautogui.press("space")  # Toggle Bluetooth
    time.sleep(1)

    speak("Bluetooth toggled.")


def toggle_wifi(state):
    """Turn WiFi on or off"""
    if state == "on":
        os.system("netsh interface set interface Wi-Fi admin=enable")
        speak("WiFi is now on.")
    elif state == "off":
        os.system("netsh interface set interface Wi-Fi admin=disable")
        speak("WiFi is now off.")
    else:
        speak("Invalid command. Please say 'turn WiFi on' or 'turn WiFi off'.")
