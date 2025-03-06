import google.generativeai as genai
import threading

# 🔹 Configure the API Key
genai.configure(api_key="AIzaSyBf-IRqOkW6cUzmKMeDYCrSY-xo9gdUUv4")

# 🔹 Load the correct Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# 🔹 Chat history for context-awareness
chat_history = []
stop_flag = False  # Flag to stop response generation


def ask_gemini(prompt):
    """
    Ask Gemini AI with context-aware memory.
    """
    global chat_history, stop_flag
    stop_flag = False  # Reset stop flag before response starts

    # Add user question to history
    chat_history.append(f"User: {prompt}")

    # Generate full conversation context
    full_prompt = "\n".join(chat_history) + "\nAI:"

    try:
        response = model.generate_content(full_prompt)

        if stop_flag:
            return "Response stopped by user."

        # Extract AI response
        if hasattr(response, "text"):
            ai_response = response.text.strip()
            chat_history.append(f"AI: {ai_response}")  # Add response to memory
            return ai_response
        else:
            return "I couldn't generate a response."

    except Exception as e:
        return f"Error: {str(e)}"


def stop_response():
    """
    Stop the AI response generation.
    """
    global stop_flag
    stop_flag = True
    return "Stopping response..."


def extract_key_lines(response_text):
    """
    Extracts two important lines from the response.
    """
    lines = response_text.split(". ")  # Split into sentences
    important_lines = lines[:2] if len(lines) >= 2 else lines  # Take first two lines
    return "\n".join(important_lines)


def clear_memory():
    """
    Clear the chat history (reset context).
    """
    global chat_history
    chat_history = []
    return "Memory cleared."
