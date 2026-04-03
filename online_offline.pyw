import requests
import subprocess
import time
import socket
from datetime import datetime

def start():
    WEBHOOK_URL = "https://discord.com/api/webhooks/1489375155317899384/aR9eFwFcaY93DMU9jzO9Uo5sAbEo6zqRbCyEsb1x_dJp6dl4eCG177AKl7NANWTQdqxQ"
    hostname = socket.gethostname()

    def send(msg):
        try:
            requests.post(WEBHOOK_URL, json={"content": msg})
        except:
            pass

    def ping_test():
        try:
            result = subprocess.run(
                ["ping", "-n", "1", "1.1.1.1"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except:
            return False

    def http_test():
        try:
            requests.get("https://1.1.1.1", timeout=2)
            return True
        except:
            return False

    def is_online():
        return ping_test() and http_test()

    # -------------------------
    # INITIAL STATE
    # -------------------------
    online = is_online()
    last_state = online

    if online:
        send(f"🟢 {hostname} is online (startup)")
    else:
        send(f"🔴 {hostname} is offline (startup)")

    # -------------------------
    # MAIN LOOP
    # -------------------------
    heartbeat_interval = 2  # seconds
    last_heartbeat = time.time()

    while True:
        online = is_online()

        # State change detection
        if online and last_state != True:
            send(f"🟢 {hostname} connected to the internet")
            last_state = True

        if not online and last_state != False:
            send(f"🔴 {hostname} disconnected from the internet")
            last_state = False

        # Heartbeat
        if time.time() - last_heartbeat >= heartbeat_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send(f"💙 Heartbeat from {hostname} at {timestamp}")
            last_heartbeat = time.time()

        time.sleep(3)
