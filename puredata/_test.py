from pythonosc.udp_client import SimpleUDPClient

PATH = "/Users/mike/Documents/GitHub/crowd-poetry/puredata/test.wav"
PD_ADDRESS = "127.0.0.1"
PD_PORT = 8000  # must match Pd's [netreceive]

client = SimpleUDPClient(PD_ADDRESS, PD_PORT)

print("Sending load command")
client.send_message("/loadsample", PATH)
