import pyautogui
import threading
import time
import queue
from text_to_speech import speak
from voice_recognition import recognize_speech

# Speech queue to handle voice commands sequentially
speech_queue = queue.Queue()


def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break  # Exit the loop if None is received
        speak(text)
        speech_queue.task_done()


# Start speech queue in a separate thread
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

moving = False  # Flag to track movement
current_direction = None  # Track the current direction
scrolling = False  # Track if scrolling is active
direction = None  # Track current scrolling direction


def listen_for_commands():
    """Continuously listen for new directions or stop command."""
    global moving, current_direction
    while moving:
        command = recognize_speech().lower()

        if "up" in command:
            current_direction = "up"
        elif "down" in command:
            current_direction = "down"
        elif "left" in command:
            current_direction = "left"
        elif "right" in command:
            current_direction = "right"
        elif "stop mouse" in command:
            moving = False  # Stop mouse movement
            speech_queue.put("Mouse movement stopped.")
            break  # Ensure thread exits without affecting main program


def move_mouse(initial_direction):
    """Moves the mouse continuously and allows real-time direction changes."""
    global moving, current_direction
    moving = True
    current_direction = initial_direction

    speech_queue.put(f"Moving mouse {current_direction}. Say a new direction or 'stop'.")

    # Start the command listener thread
    command_thread = threading.Thread(target=listen_for_commands, daemon=True)
    command_thread.start()

    while moving:
        x, y = pyautogui.position()

        if current_direction == "up":
            pyautogui.moveTo(x, y - 10, duration=0.1)
        elif current_direction == "down":
            pyautogui.moveTo(x, y + 10, duration=0.1)
        elif current_direction == "left":
            pyautogui.moveTo(x - 10, y, duration=0.1)
        elif current_direction == "right":
            pyautogui.moveTo(x + 10, y, duration=0.1)

        time.sleep(0.1)  # Smooth movement


def scroll_continuously():
    global scrolling, direction
    while scrolling:
        if direction == "up":
            pyautogui.scroll(50)
        elif direction == "down":
            pyautogui.scroll(-50)
        time.sleep(0.1)


def start_scrolling(new_direction):
    global scrolling, direction
    if not scrolling:
        scrolling = True
        direction = new_direction
        thread = threading.Thread(target=scroll_continuously, daemon=True)
        thread.start()
    else:
        direction = new_direction


def stop_scrolling():
    global scrolling
    scrolling = False


def click_mouse():
    """Click the mouse at the current position."""
    pyautogui.click()
    speech_queue.put("Clicked")


def right_click_mouse():
    """Right-click at the current position."""
    pyautogui.rightClick()
    speech_queue.put("Right click")


def double_click_mouse():
    """Double-click at the current position."""
    pyautogui.doubleClick()
    speech_queue.put("Double click")


def scroll_mouse(amount):
    """Scroll the mouse up or down."""
    pyautogui.scroll(amount)
    speech_queue.put(f"Scrolled {'up' if amount > 0 else 'down'}")
