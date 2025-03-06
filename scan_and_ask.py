import pyautogui
import time
import pyperclip
import requests
import win32com.client
import google.generativeai as genai
from text_to_speech import speak

# Set up Gemini API
API_KEY = "AIzaSyBTkOGKebyTrPNO-oS8aEBG8WGVlw5U6pw"  # Replace with your Gemini API Key
genai.configure(api_key=API_KEY)


def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error: Unable to fetch response."


def process_notepad():
    speak("Processing text from Notepad.")
    pyautogui.hotkey("ctrl", "a")  # Select all text
    pyautogui.hotkey("ctrl", "c")  # Copy
    time.sleep(1)  # Wait for clipboard update
    text = pyperclip.paste().strip()  # Get copied text

    if not text:
        speak("I couldn't detect any text in Notepad. Please try again.")
        return

    lines = text.split("\n")
    updated_text = []

    for line in lines:
        updated_text.append(line)  # Keep original question
        if "?" in line.strip():  # Identify question
            response = ask_gemini(line.strip())  # Get AI answer
            updated_text.append("AI Response: " + response)  # Add answer below

    final_output = "\n".join(updated_text)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")
    pyperclip.copy(final_output)  # Copy updated text to clipboard
    pyautogui.hotkey("ctrl", "v")  # Paste back into Notepad
    speak("AI responses have been added to Notepad.")


def process_word():
    try:
        speak("Processing text from Microsoft Word.")
        word = win32com.client.Dispatch("Word.Application")
        if word.Documents.Count == 0:
            speak("No Word document is open.")
            return

        doc = word.ActiveDocument
        selection = word.Selection.Text.strip()

        if selection:
            response = ask_gemini(selection)
            word.Selection.Collapse(0)  # Move cursor to end of selection
            word.Selection.TypeText("\n\nAI Response:\n" + response + "\n")
            speak("AI response added to Word.")
        else:
            speak("No text selected in Word. Please select a question and try again.")

    except Exception as e:
        speak("Error processing Word document. Please try again.")


def process_text():
    import pygetwindow as gw
    active_window = gw.getActiveWindow()
    active_window_title = active_window.title if active_window else ""

    if "Notepad" in active_window_title:
        process_notepad()
    elif "Word" in active_window_title or "Microsoft Word" in active_window_title:
        process_word()
    else:
        speak("Unsupported application. Please use Notepad or Word.")


# Main function call
if __name__ == "__main__":
    process_text()
