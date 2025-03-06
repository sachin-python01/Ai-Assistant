import os
import requests
from PIL import Image
from text_to_speech import speak
from voice_recognition import recognize_speech

# Define the directory to save images
SAVE_DIR = "generated_images"
os.makedirs(SAVE_DIR, exist_ok=True)


# Function to generate image using the API
def generate_image(prompt=None):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    HEADERS = {"Authorization": "Bearer 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"}

    if prompt is None or prompt.strip() == "":  # Ask only if no prompt is given
        speak("What should I generate?")
        prompt = recognize_speech()
        if prompt in ["exit", "cancel", "stop"]:
            speak("Image generation canceled.")
            return None

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        try:
            image_data = response.content  # Get the image bytes
            if b"<html>" in image_data[:100]:  # Detect HTML errors
                speak("There was an issue generating the image. Please try a different prompt.")
                return None

            image_path = os.path.join(SAVE_DIR, "generated_image.png")
            with open(image_path, "wb") as file:
                file.write(image_data)

            speak(f"Image of {prompt} has been generated and saved.")
            image = Image.open(image_path)
            image.show()
            return image_path
        except Exception as e:
            speak("An error occurred while processing the image. Please try again.")
            return None
    else:
        speak(f"Error {response.status_code}: Unable to generate image. Please try again with a different prompt.")
        return None
