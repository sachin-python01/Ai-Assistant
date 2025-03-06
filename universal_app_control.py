import os
import shutil
import subprocess
import psutil
import pyautogui
import time
from text_to_speech import speak

# Common application mappings for system apps
APP_MAPPING = {
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "word": "WINWORD.EXE",
    "excel": "EXCEL.EXE",
    "powerpoint": "POWERPNT.EXE",
    "cmd": "cmd.exe",
    "task manager": "Taskmgr.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "outlook": "OUTLOOK.EXE",
    "vlc": "vlc.exe",
    "spotify": "spotify.exe",
    "settings": "start ms-settings:",
    "control panel": "control",
    "camera": "start microsoft.windows.camera:"  # Fix for opening Camera
}


def get_running_processes():
    """Returns a set of currently running process names."""
    return {p.info['name'].lower() for p in psutil.process_iter(attrs=['name'])}


def open_application(app_name):
    """Opens an application by name and verifies if it actually opened."""
    app_name = app_name.lower()
    before_processes = get_running_processes()  # Get running processes before opening

    if app_name in APP_MAPPING:
        command = APP_MAPPING[app_name]
        os.system(command)  # Use os.system() for system apps
    else:
        app_path = shutil.which(app_name)
        if app_path:
            try:
                subprocess.Popen([app_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                speak(f"Failed to open {app_name}. Error: {str(e)}")
                return
        else:
            os.system(f"start {app_name}")  # Try as a general command

    time.sleep(2)  # Wait for the process to start
    after_processes = get_running_processes()

    if after_processes - before_processes:  # Check for new processes
        speak(f"Opened {app_name}.")
    else:
        speak(f"Failed to open {app_name}.")


def close_application(app_name):
    """Closes an application if it's running."""
    found = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if app_name.lower() in process.info['name'].lower():
            os.kill(process.info['pid'], 9)
            found = True
            speak(f"Closed {app_name}.")
            break

    if not found:
        speak(f"No running instance of {app_name} found.")


def list_running_apps():
    """Lists currently running applications."""
    running_apps = [p.info['name'] for p in psutil.process_iter(attrs=['name'])]
    return running_apps


def close_all_applications():
    """Force close all running applications except essential system processes."""
    system_processes = ["explorer.exe", "cmd.exe", "python.exe", "taskmgr.exe"]
    closed_apps = []

    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name']
            process_pid = process.info['pid']

            if process_name.lower() not in [p.lower() for p in system_processes]:
                os.system(f"taskkill /PID {process_pid} /F")
                closed_apps.append(process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Ignore processes that no longer exist or are inaccessible

    if closed_apps:
        speak(f"Closed applications: {', '.join(closed_apps)}")
    else:
        speak("No applications were closed.")


def switch_application():
    """Switches between running applications."""
    speak("Switching to the next application.")
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    pyautogui.keyUp("alt")
