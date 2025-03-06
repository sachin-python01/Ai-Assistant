import pvporcupine
import pyaudio
import struct

# Load Porcupine with the built-in "Jarvis" wake word
ACCESS_KEY = "vkNe8WrrvpW4O3pF2bJP7mgXgpfzXer9tWjMVvw3C3euieAfTxPhqQ=="  # Replace with your actual key

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[r"C:\Users\SACHIN\PycharmProjects\try17\jarvis.ppn"])

def detect_wake_word():
    """Continuously listens for the wake word."""
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for 'Jarvis'...")
    while True:
        pcm = struct.unpack_from("h" * porcupine.frame_length, stream.read(porcupine.frame_length))
        result = porcupine.process(pcm)
        if result >= 0:
            print("Wake word detected!")
            return True  # Wake word detected, return to start command recognition
