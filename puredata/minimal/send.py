from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("127.0.0.1", 8000)
client.send_message("/text", "hello from python")
