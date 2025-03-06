from voice_recognition import recognize_speech
from text_to_speech import speak
from system_monitor import get_battery_status, get_cpu_usage, get_ram_usage
from network_control import toggle_wifi, toggle_bluetooth
from virtual_desktop import create_virtual_desktop, switch_virtual_desktop, close_virtual_desktop
from voice_mouse import move_mouse, click_mouse, right_click_mouse, double_click_mouse, scroll_mouse
from wake_word import detect_wake_word
from voice_mouse import start_scrolling, stop_scrolling
from screenshot_helper import take_screenshot, take_active_window_screenshot
from gemini_ai import ask_gemini, clear_memory  # ✅ Uses context-aware AI
from image_generator import generate_image
import scan_and_ask
from universal_app_control import open_application, close_all_applications, close_application, list_running_apps

active = False  # Keeps track of whether Jarvis is listening

pdf_directory = "C:\\Users\\Sachin\\Documents\\PDFs"

speak("Hello Sachin, how can I help you?")

while True:
    if not active:  # If inactive, wait for "Jarvis" wake word
        if detect_wake_word():
            active = True
            speak("I'm listening. How can I help you?")  # ✅ Non-blocking speak

    if active:  # When active, continuously listen for commands
        command = recognize_speech()

        if command:
            command = command.lower()

            if "exit" in command:
                speak("Goodbye!")
                break
            elif "sleep" in command:
                speak("Going to sleep mode. Say 'Jarvis' to wake me up.")
                active = False
            elif "battery" in command:
                get_battery_status()
            elif "cpu" in command:
                get_cpu_usage()
            elif "ram" in command:
                get_ram_usage()
            elif "turn wi-fi on" in command:
                toggle_wifi("on")
            elif "turn wi-fi off" in command:
                toggle_wifi("off")
            elif "turn bluetooth on" in command:
                toggle_bluetooth()
            elif "turn bluetooth off" in command:
                toggle_bluetooth()
            elif "new desktop" in command:
                create_virtual_desktop()
            elif "switch left" in command:
                switch_virtual_desktop("left")
            elif "switch right" in command:
                switch_virtual_desktop("right")
            elif "remove desktop" in command:
                close_virtual_desktop()
            elif "move mouse" in command:
                direction = command.replace("move mouse ", "").strip()
                move_mouse(direction)
            elif "stop mouse" in command:
                speak("Stopped moving mouse.")
                break  # Ensures the program keeps listening for new commands
            elif "click mouse" in command:
                click_mouse()
            elif "right click" in command:
                right_click_mouse()
            elif "double click" in command:
                double_click_mouse()
            elif "scroll up" in command:
                scroll_mouse(200)
            elif "scroll down" in command:
                scroll_mouse(-200)
            elif "scrolling up" in command:
                start_scrolling("up")
            elif "scrolling down" in command:
                start_scrolling("down")
            elif "stop scrolling" in command:
                stop_scrolling()
            elif "take screenshot" in command:
                filepath = take_screenshot(command)
                speak(f"Screenshot saved as {filepath}")
            elif "capture active window" in command:
                filepath = take_active_window_screenshot(command)
                if "No active window" in filepath:
                    speak("No active window detected.")
                else:
                    speak(f"Active window screenshot saved as {filepath}")

            # ✅ Context-Aware AI
            elif "ask ai" in command:
                prompt = command.replace("ask ai", "").strip()
                response = ask_gemini(prompt)  # ✅ Uses context-aware AI
                speak(response)
                print("AI:", response)

            # ✅ Generate Image
            elif "generate image" in command:
                prompt = command.replace("generate image", "").strip()
                if not prompt:
                    speak("What should I generate?")
                    prompt = recognize_speech()

                if prompt and prompt not in ["exit", "cancel", "stop"]:
                    generate_image(prompt)
                else:
                    speak("Image generation canceled.")


            # ✅ Scan and Ask AI
            elif "get answer" in command:
                scan_and_ask.process_text()

            # ✅ Clear AI Memory
            elif "forget everything" in command:
                speak("Forgetting all previous conversations.")
                print(clear_memory())  # Clears AI memory

            # Inside the voice command loop in `main.py`
            elif "open" in command:
                app_name = command.replace("open ", "").strip()
                open_application(app_name)

            elif "close" in command:
                app_name = command.replace("close ", "").strip()
                close_application(app_name)

            elif "list apps" in command:
                running_apps = list_running_apps()
                print("Running Applications:", ", ".join(running_apps))

            elif "close all app" in command:
                close_all_applications()

# PROBLEM FACING
# google search
# wikipedia search
# oepn new tab
#chrome basic automation
# close all application
# switch application
