import winreg

def start():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Control Panel\Keyboard",
        0,
        winreg.KEY_SET_VALUE
    )

    winreg.SetValueEx(key, "PrintScreenKeyForSnippingEnabled", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

    print("Snipping Tool PrintScreen override disabled.")
