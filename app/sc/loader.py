import time
import os
from pythonosc.udp_client import SimpleUDPClient

WATCH_DIR = "../python/audio_clips"
PD_ADDRESS = "127.0.0.1"
PD_PORT = 57120  # must match SuperCollider's UDP port

client = SimpleUDPClient(PD_ADDRESS, PD_PORT)
loaded_files = set()

print("Watching for new samples...")

while True:
    files = {f for f in os.listdir(WATCH_DIR) if f.endswith(".wav")}
    new_files = files - loaded_files

    for f in sorted(new_files):
        full_path = os.path.abspath(os.path.join(WATCH_DIR, f))
        print(f"Sending load command for: {full_path}")
        client.send_message("/loadsample", full_path)

    loaded_files.update(new_files)
    time.sleep(2)