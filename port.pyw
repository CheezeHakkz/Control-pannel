import requests
import socket
import json
import time

def start():
    WEBHOOK_URL = "https://discord.com/api/webhooks/1489359841162952776/58Gf9bL3pFZHMacpAKSzKbjHNlZe8yU0Ld_oES_Q2CCn9lWA9b3z4godXv5xU3t5PnKC"  # replace with your working webhook

    def send_payload(payload):
        try:
            r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        except Exception as e:
            print("Request exception:", e)
            return None, str(e)
        print("HTTP", r.status_code, r.text)
        if r.status_code == 429:
            # Discord rate limit: try to parse Retry-After header or JSON
            retry = r.headers.get("Retry-After")
            if retry:
                try:
                    wait = float(retry)
                except:
                    wait = 1.0
            else:
                try:
                    j = r.json()
                    wait = j.get("retry_after", 1.0)
                except:
                    wait = 1.0
            print(f"Rate limited. Sleeping for {wait} seconds.")
        return r.status_code, r.text

    # quick connectivity test
    print("=== Webhook connectivity test ===")
    status, text = send_payload({"content": "webhook connectivity test from scanner script"})
    if status is None or status >= 400 and status != 429:
        print("Webhook test failed. Stop and verify the webhook URL in Discord integrations.")
    else:
        print("Webhook test OK or rate-limited but reachable.")

    # scan local ports
    target = "127.0.0.1"
    open_ports = []
    print("=== Scanning ports 20-1024 on", target, "===")
    for port in range(20, 1025):
        try:
            s = socket.socket()
            s.settimeout(0.08)
            s.connect((target, port))
            open_ports.append(port)
            s.close()
            print("Open:", port)
        except Exception:
            pass

    # prepare messages and chunk if necessary
    base = f"Open ports on {target}: "
    ports_text = ", ".join(str(p) for p in open_ports) if open_ports else "None"
    full_message = base + ports_text
    print("Message length:", len(full_message))

    MAX = 1900  # safe Discord content limit
    messages = []
    if len(full_message) <= MAX:
        messages = [full_message]
    else:
        # chunk ports list into multiple messages without breaking numbers
        prefix = base
        current = prefix
        for p in open_ports:
            addition = (", " if current != prefix else "") + str(p)
            if len(current) + len(addition) > MAX:
                messages.append(current)
                current = prefix + str(p)
            else:
                current += addition
        if current:
            messages.append(current)

    # send messages with small delay to avoid rate limits
    print(f"Sending {len(messages)} message(s) to webhook")
    for i, msg in enumerate(messages, 1):
        print(f"Sending chunk {i}/{len(messages)} (len={len(msg)})")
        status, text = send_payload({"content": msg})
        if status == 204:
            print("Chunk sent successfully.")
        elif status == 429:
            # already handled inside send_payload; retry this chunk once
            print("Retrying chunk after rate limit...")
            status, text = send_payload({"content": msg})
            if status == 204:
                print("Chunk sent after retry.")
            else:
                print("Failed after retry:", status, text)
        else:
            print("Send result:", status, text)
        time.sleep(1.0)  # small pause between messages

    print("Done.")
