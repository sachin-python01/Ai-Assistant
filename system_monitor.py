import psutil
from text_to_speech import speak

def get_battery_status():
    """Get battery percentage and charging status"""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        charging = "charging" if battery.power_plugged else "not charging"
        speak(f"Your battery is at {percent} percent and is {charging}.")
    else:
        speak("I couldn't get battery information.")

def get_cpu_usage():
    """Get CPU usage percentage"""
    usage = psutil.cpu_percent(interval=1)
    speak(f"Your CPU usage is at {usage} percent.")

def get_ram_usage():
    """Get RAM usage percentage"""
    ram = psutil.virtual_memory()
    speak(f"Your RAM usage is at {ram.percent} percent.")
